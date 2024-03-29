"""Networking."""

import logging
import os
import socket
from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Callable, ClassVar, Final, Optional, Union


class BaseServer(metaclass=ABCMeta):

    # system/platform information
    _uname = os.uname()
    os_name: ClassVar[str] = _uname.sysname
    os_version: ClassVar[str] = _uname.release
    os_version_info: ClassVar[tuple[str, ...]] = tuple(os_version.split('.'))

    if os_name == 'Linux':
        assert socket.SOMAXCONN == int(
            Path('/proc/sys/net/core/somaxconn').read_text().strip()
        )

    def __init__(
        self,
        reuse_address: bool,
        logger_name: str,
    ):
        self.logger = logging.getLogger(logger_name)
        self.socket: Optional[socket.SocketType]
        self.reuse_address = reuse_address
        self.max_recv_buf_size: Union[int, None] = None
        self.max_send_buf_size: Union[int, None] = None

    def bind(self):
        assert self.socket is not None

        if self.reuse_address:
            # The `SO_REUSEADDR` flag tells the kernel to reuse a local socket in
            # `TIME_WAIT` state, without waiting for its natural timeout to expire.
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.socket.bind(self.server_address)
        self.server_address = self.socket.getsockname()

        self.post_bind()

    def post_bind(self):
        assert self.socket is not None

        self.recv_buf_size = self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
        self.send_buf_size = self.socket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)

    def close(self):
        if self.socket is not None:
            self.socket.close()

    @abstractmethod
    def get_max_buf_size(self):
        pass

    def set_buffer_size(self):
        """Set recv/send buffer size."""
        assert self.socket is not None

        self.get_max_buf_size()

        for pair in (
            (self.recv_buf_size, self.max_recv_buf_size, 'recv', socket.SO_RCVBUF),
            (self.send_buf_size, self.max_send_buf_size, 'send', socket.SO_SNDBUF),
        ):
            if pair[0] is not None:
                if pair[1] and pair[0] > pair[1]:
                    self.logger.warning(
                        f'invalid {pair[2]} buf ({pair[0]}): '
                        f'exceeds max value ({pair[1]}).'
                    )
                    # kernel do this already!
                    # pair[0] = min(pair[0], pair[1])
                self.socket.setsockopt(socket.SOL_SOCKET, pair[3], pair[0])

    def show_info(self, extras: Optional[Iterable[str]] = None):
        assert self.socket is not None

        server_info_msgs = [
            'running',
            f'server address: {self.server_address}',
            f'os: {self.os_name} ({self.os_version})',
            f'reuse address: {self.reuse_address}',
            f'recv buffer size: {self.recv_buf_size} (max={self.max_recv_buf_size})',
            f'send buffer size: {self.send_buf_size} (max={self.max_send_buf_size})',
        ]
        if extras:
            server_info_msgs.extend(extras)

        self.logger.debug('\n'.join(server_info_msgs))

    def __enter__(self):
        return self

    def __exit__(self, *args: Any):
        self.close()


class BaseTCPServer(BaseServer):
    socket_type: Final[socket.SocketKind] = socket.SOCK_STREAM

    def __init__(
        self,
        handle_request: Callable[[socket.socket, tuple[str, int], Any], None],
        reuse_address: bool,
        accept_queue_size: Optional[int],
        recv_buf_size: Optional[int],
        send_buf_size: Optional[int],
        logger_name: str,
    ):
        super().__init__(reuse_address, logger_name)
        self.handle_request = handle_request

        if accept_queue_size is None:
            self.accept_queue_size = None
        else:
            self.accept_queue_size = min(accept_queue_size, socket.SOMAXCONN)

        self.recv_buf_size = recv_buf_size
        self.send_buf_size = send_buf_size

    def listen(self):
        # Because of the 3-way handshake used by TCP, an incoming connection goes
        # through an intermediate state `SYN RECEIVED` before it reaches the
        # `ESTABLISHED` state and can be returned by the `accept()` syscall to the
        # application. This means that a TCP/IP stack has two options to implement the
        # backlog queue for a socket in `LISTEN` state:
        #
        # 1: The implementation uses a single queue, the size of which is determined by
        # the `backlog` argument of the `listen()` syscall. When a `SYN`` packet is
        # received, it sends back a `SYN`/`ACK` packet and adds the connection to the
        # queue. When the corresponding `ACK` is received, the connection changes its
        # state to `ESTABLISHED` and becomes eligible for handover to the application.
        # This means that the queue can contain connections in two different state:
        # `SYN RECEIVED` and `ESTABLISHED`. Only connections in the latter state can be
        # returned to the application by the `accept()` syscall.
        #
        # 2: The implementation uses two queues, a `SYN` queue(or incomplete connection
        # queue) and an accept queue (or complete connection queue). Connections in
        # state `SYN RECEIVED` are added to the `SYN` queue and later moved to the
        # accept queue when their state changes to `ESTABLISHED`, i.e. when the `ACK`
        # packet in the 3-way handshake is received. As the name implies, the `accept()`
        # call is then implemented simply to consume connections from the accept queue.
        # In this case, the `backlog` argument of the `listen()` syscall determines the
        # size of the accept queue.
        #
        # Historically, BSD derived TCP implementations use the first approach. That
        # choice implies that when the maximum `backlog` is reached, the system will no
        # longer send back `SYN`/`ACK` packets in response to `SYN` packets. Usually
        # the TCP implementation will simply drop the `SYN` packet (instead of
        # responding with a `RST` packet) so that the client will retry.
        #
        # On Linux, things are different, as mentioned in the man page of the `listen()`
        # syscall:
        # The behavior of the `backlog` argument on TCP sockets changed with Linux 2.2.
        # Now it specifies the queue length for completely established sockets waiting
        # to be accepted, instead of the number of incomplete connection requests.
        # This means that current Linux versions use the second option with two
        # distinct queues: a `SYN` queue with a size specified by a system wide setting
        # and an accept queue with a size specified by the application.
        #
        # The maximum length of the `SYN` queue for incomplete sockets can be set using:
        #     /proc/sys/net/ipv4/tcp_max_syn_backlog
        # or
        #     sysctl -w net.ipv4.tcp_max_syn_backlog=<N>
        # or make the change permanently in `/etc/sysctl.conf`.
        #
        # The maximum length of the accept queue for completed sockets can be set using:
        #     cat /proc/sys/net/core/somaxconn
        # or
        #     sysctl net.core.somaxconn
        # You can change the value to N.
        #      sudo sysctl -w net.core.somaxconn=<N>
        # or make the change permanently in `/etc/sysctl.conf`.

        assert self.socket is not None

        # The `backlog` argument of `listen()` must be less than it.
        if self.accept_queue_size is None:
            self.socket.listen()
        else:
            self.socket.listen(self.accept_queue_size)

    def get_max_buf_size(self):
        assert self.socket is not None

        # Get max TCP (IPv4) recv/send buffer size in system (Linux)
        # - read(recv): /proc/sys/net/ipv4/tcp_rmem
        # - write(send): /proc/sys/net/ipv4/tcp_wmem
        if self.os_name == 'Linux' and self.socket.family is socket.AF_INET:
            self.max_recv_buf_size = int(
                Path('/proc/sys/net/ipv4/tcp_rmem')
                .read_text()
                .strip()
                .split()[2]
                .strip()
            )
            self.max_send_buf_size = int(
                Path('/proc/sys/net/ipv4/tcp_wmem')
                .read_text()
                .strip()
                .split()[2]
                .strip()
            )

    def run(self):
        assert self.socket is not None

        extra_info = [
            f'accept queue size: {self.accept_queue_size} (max={socket.SOMAXCONN})'
        ]
        if self.os_name == 'Linux' and self.os_version_info >= (
            '2',
            '2',
            '0',
        ):  # Linux 2.2+
            if self.socket.family is socket.AF_INET:
                max_syn_queue_size = int(
                    Path('/proc/sys/net/ipv4/tcp_max_syn_backlog').read_text().strip()
                )
                extra_info.append(f'max syn queue size: {max_syn_queue_size}')
        self.show_info(extra_info)

        while True:
            try:
                request, client_address = self.socket.accept()  # type: ignore
            except OSError as err:
                self.logger.error(err)
                raise

            self.logger.debug(f'accept request from: {client_address}')
            try:
                self.handle_request(request, client_address, self)  # type: ignore
            except (OSError, RuntimeError) as err:
                self.logger.error(err)
            finally:
                # explicitly shutdown.
                # socket.close() merely releases
                # the socket and waits for GC to perform the actual close.
                request.shutdown(socket.SHUT_WR)  # type: ignore
                request.close()  # type: ignore
                self.logger.debug(f'client closed: {client_address}')


class BaseUDPServer(BaseServer):
    socket_type: Final[socket.SocketKind] = socket.SOCK_DGRAM

    def __init__(
        self,
        handle_request: Callable[[BaseServer], None],
        reuse_address: bool,
        recv_buf_size: Optional[int],
        send_buf_size: Optional[int],
        logger_name: str,
    ):
        super().__init__(reuse_address, logger_name)
        self.handle_request = handle_request

        # Recv/Send buffer size
        self.recv_buf_size = recv_buf_size
        self.send_buf_size = send_buf_size

    def get_max_buf_size(self):
        assert self.socket is not None

        # Get max UDP recv/send buffer size in system (Linux)
        # - read(recv): /proc/sys/net/core/rmem_max
        # - write(send): /proc/sys/net/core/wmem_max
        if self.os_name == 'Linux':
            self.max_recv_buf_size = int(
                Path('/proc/sys/net/core/rmem_max').read_text().strip()
            )
            self.max_send_buf_size = int(
                Path('/proc/sys/net/core/wmem_max').read_text().strip()
            )

    def run(self):
        assert self.socket is not None
        self.show_info()

        while True:
            try:
                self.handle_request(self)
            except (OSError, RuntimeError) as err:
                self.logger.error(err)

    def post_bind(self):
        super().post_bind()


class TCPServer(BaseTCPServer):
    """Extend the Python standard TCP (both IPv4 & IPv6) server.

    Usage:
        from handy.net import TCPServer, echo_request

        with TCPServer(None, 9999, echo_request) as srv:
            srv.run()
    """

    def __init__(  # noqa: C901
        self,
        host: Union[str, None],
        port: Union[int, str, None],
        handle_request: Callable[[socket.socket, tuple[str, int], BaseServer], None],
        address_family: socket.AddressFamily = socket.AF_UNSPEC,
        address_info: socket.AddressInfo = socket.AI_PASSIVE,
        no_dns: bool = False,
        reuse_address: bool = True,
        accept_queue_size: int = 0,
        recv_buf_size: Optional[int] = None,
        send_buf_size: Optional[int] = None,
        logger_name: str = 'handy.TCPServer',
    ):
        super().__init__(
            handle_request,
            reuse_address,
            accept_queue_size,
            recv_buf_size,
            send_buf_size,
            logger_name,
        )

        if no_dns:
            address_info |= socket.AI_NUMERICHOST

        for res in socket.getaddrinfo(
            host,
            port,
            address_family,
            self.socket_type,
            socket.IPPROTO_IP,
            address_info,
        ):
            af, socktype, proto, _, server_address = res
            assert socktype == socket.SOCK_STREAM
            try:
                self.socket = socket.socket(af, socktype, proto)
            except OSError:
                self.socket = None
                continue

            address_family = af
            self.server_address = server_address

            try:
                self.set_buffer_size()
                self.bind()
                self.listen()
            except OSError:
                self.close()
                self.socket = None
                continue
            break

        if self.socket is None:
            raise RuntimeError('could not open socket')

        if address_family is socket.AF_INET:
            if host in (None, '', '0.0.0.0'):
                self.host_address = socket.INADDR_ANY
            elif host in ('localhost', '127.0.0.1'):
                self.host_address = socket.INADDR_LOOPBACK
            elif host == '<broadcast>':
                self.host_address = socket.INADDR_BROADCAST
        elif address_family is socket.AF_INET6:
            if host is None and address_info & socket.AI_PASSIVE:
                self.host_address = socket.INADDR_ANY  # IN6ADDR_ANY_INIT
            elif host is None and not (address_info & socket.AI_PASSIVE):
                self.host_address = socket.INADDR_LOOPBACK  # IN6ADDR_LOOPBACK_INIT


class TCPServerIPv4(BaseTCPServer):
    """Extend the Python standard TCP (IPv4) server.

    Usage:
        from handy.net import TCPServerIPv4, echo_request

        with TCPServerIPv4(('', 0), echo_request) as srv:
            srv.run()
    """

    def __init__(
        self,
        server_address: tuple[str, int],
        handle_request: Callable[[socket.socket, tuple[str, int], BaseServer], None],
        reuse_address: bool = True,
        accept_queue_size: Optional[int] = None,
        recv_buf_size: Union[int, None] = None,
        send_buf_size: Union[int, None] = None,
        logger_name: str = 'handy.TCPServerIPv4',
    ):
        super().__init__(
            handle_request,
            reuse_address,
            accept_queue_size,
            recv_buf_size,
            send_buf_size,
            logger_name,
        )
        self.socket = socket.socket(socket.AF_INET, self.socket_type)

        host, _ = server_address
        if host in ('localhost', '127.0.0.1'):
            self.host_address = socket.INADDR_LOOPBACK
        elif host in ('', '0.0.0.0'):
            self.host_address = socket.INADDR_ANY
        elif host == '<broadcast>':
            self.host_address = socket.INADDR_BROADCAST
        self.server_address = server_address

        try:
            self.set_buffer_size()
            self.bind()
            self.listen()
        except OSError as err:
            self.logger.error(err)
            self.close()
            raise


class UDPServerIPv4(BaseUDPServer):
    """Extend the Python standard UDP (IPv4) server.

    Usage:
        from handy.net import UDPServerIPv4, echo_request

        with UDPServerIPv4(('', 0), echo_request) as srv:
            srv.run()
    """

    def __init__(
        self,
        server_address: tuple[str, int],
        handle_request: Callable[[BaseServer], None],
        reuse_address: bool = True,
        recv_buf_size: Optional[int] = None,
        send_buf_size: Optional[int] = None,
        logger_name: str = 'handy.UDPServerIPv4',
    ):
        super().__init__(
            handle_request,
            reuse_address,
            recv_buf_size,
            send_buf_size,
            logger_name,
        )
        self.socket = socket.socket(socket.AF_INET, self.socket_type)

        host, _ = server_address
        if host in ('localhost', '127.0.0.1'):
            self.host_address = socket.INADDR_LOOPBACK
        elif host in ('', '0.0.0.0'):
            self.host_address = socket.INADDR_ANY
        elif host == '<broadcast>':
            self.host_address = socket.INADDR_BROADCAST
        self.server_address = server_address

        try:
            self.set_buffer_size()
            self.bind()
        except OSError as err:
            self.logger.error(err)
            self.close()
            raise


def echo_request_tcp(
    request: socket.socket,
    client_address: tuple[str, int],
    server: BaseServer,
):
    raw_data = request.recv(1024)
    if raw_data:
        data = raw_data.decode('utf-8')
        server.logger.debug(f'received data from {client_address}: {data}')
        request.sendall(raw_data)
        server.logger.debug(f'sending data to {client_address}: {data}')
    else:
        server.logger.debug(f'no data from {client_address}')


def echo_request_udp(server: BaseServer):
    assert server.socket is not None
    raw_data, client_address = server.socket.recvfrom(1024)
    if raw_data:
        data = raw_data.decode('utf-8')
        server.logger.debug(f'received data from {client_address}: {data}')
        server.socket.sendto(raw_data, client_address)
        server.logger.debug(f'sending data to {client_address}: {data}')
    else:
        server.logger.debug(f'no data from {client_address}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # with TCPServer(
    #     None,
    #     9999,
    #     echo_request,
    #     address_family=socket.AF_INET,
    #     no_dns=True,
    # ) as server:
    #     server.run()

    # Port 0 means to select an arbitrary unused port
    # with TCPServerIPv4(('', 0), echo_request_tcp) as server:
    #     server.run()

    # Port 0 means to select an arbitrary unused port
    with UDPServerIPv4(('', 0), echo_request_udp) as server:
        server.run()
