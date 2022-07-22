import os
import socket

import pytest

from src.handy.net.tcpserver import TCPServer, TCPServerIPv4, echo_request


class TestNet:
    @pytest.fixture
    def os_name(self):
        return os.uname().sysname

    @pytest.fixture
    def port(self):
        return 0

    def test_TCPServer(self, os_name: str, port: int):
        server = TCPServer(None, port, echo_request, no_dns=True)
        assert server.socket_type is socket.SOCK_STREAM
        sock = server.socket
        assert sock is not None
        if socket.has_ipv6:
            assert sock.family is socket.AF_INET6
        else:
            assert sock.family is socket.AF_INET
        if os_name == 'Linux':
            assert hasattr(server, 'max_recv_buf_size')
            assert hasattr(server, 'max_send_buf_size')
            assert isinstance(server.max_recv_buf_size, int)
            assert isinstance(server.max_send_buf_size, int)
        else:
            assert not hasattr(server, 'max_receive_buf_size')
            assert not hasattr(server, 'max_send_buf_size')
        server.close()

    def test_TCPServerIPv4(self, os_name: str, port: int):
        server = TCPServerIPv4(('localhost', port), echo_request)
        assert server.socket_type == socket.SOCK_STREAM
        sock = server.socket
        assert sock is not None
        assert sock.family is socket.AF_INET
        if os_name == 'Linux':
            assert hasattr(server, 'max_recv_buf_size')
            assert hasattr(server, 'max_send_buf_size')
            assert isinstance(server.max_recv_buf_size, int)
            assert isinstance(server.max_send_buf_size, int)
        else:
            assert not hasattr(server, 'max_receive_buf_size')
            assert not hasattr(server, 'max_send_buf_size')
        server.close()
