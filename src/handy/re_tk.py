"""Basic Perl-compitable regular expression (PCRE) demonstration facility with TK.

The original script is from CPython.
<https://github.com/python/cpython/blob/master/Tools/demo/redemo.py>
"""

import re
import tkinter
from typing import Pattern, Union


class ReTK:
    """Regular expression facility with TK-GUI."""

    def __init__(
        self,
        tk: tkinter.Tk,
        width: int = 60,
        height: int = 40,
        string_background: str = 'orange',
        string_hit_background: str = 'green',
        status_background: str = 'red',
    ):
        self.tk = tk
        self.string_background = string_background
        self.string_hit_background = string_hit_background
        self.status_background = status_background

        self.prompt_display = tkinter.Label(
            self.tk,
            anchor=tkinter.W,
            text='Enter a Perl-compitable regular expression (PCRE):',
        )
        self.prompt_display.pack(side=tkinter.TOP, fill=tkinter.X)

        self.regex_display = tkinter.Entry(self.tk)
        self.regex_display.pack(fill=tkinter.X)
        self.regex_display.focus_set()

        self.addoptions()

        self.status_display = tkinter.Label(self.tk, text='', anchor=tkinter.W)
        self.status_display.pack(side=tkinter.TOP, fill=tkinter.X)

        self.label_display = tkinter.Label(
            self.tk, anchor=tkinter.W, text='Enter a string to search:'
        )
        self.label_display.pack(fill=tkinter.X)
        self.label_display.pack(fill=tkinter.X)

        self.showframe = tkinter.Frame(self.tk)
        self.showframe.pack(fill=tkinter.X, anchor=tkinter.W)

        self.showvar = tkinter.StringVar(self.tk)
        self.showvar.set('first')

        self.show_first_radio = tkinter.Radiobutton(
            self.showframe,
            text='Highlight first match',
            variable=self.showvar,
            value='first',
            command=self.re_compile,
        )
        self.show_first_radio.pack(side=tkinter.LEFT)

        self.show_all_radio = tkinter.Radiobutton(
            self.showframe,
            text='Highlight all matches',
            variable=self.showvar,
            value='all',
            command=self.re_compile,
        )
        self.show_all_radio.pack(side=tkinter.LEFT)

        self.string_display = tkinter.Text(self.tk, width=width, height=height)
        self.string_display.pack(fill=tkinter.BOTH, expand=True)
        self.string_display.tag_configure('hit', background=self.string_background)

        self.group_label = tkinter.Label(self.tk, text='Groups:', anchor=tkinter.W)
        self.group_label.pack(fill=tkinter.X)

        self.group_list = tkinter.Listbox(self.tk)
        self.group_list.pack(expand=True, fill=tkinter.BOTH)

        self.regex_display.bind('<Key>', self.re_compile)
        self.string_display.bind('<Key>', self.re_evaluate)

        self.compiled: Union[Pattern[str], None] = None
        self.re_compile()

        tags = self.regex_display.bindtags()
        self.regex_display.bindtags(tags[1:] + tags[:1])

        tags = self.string_display.bindtags()
        self.string_display.bindtags(tags[1:] + tags[:1])

    def addoptions(self):
        self.frames: list[tkinter.Frame] = []
        self.boxes: list[tkinter.Checkbutton] = []
        self.vars: list[tkinter.IntVar] = []
        for name in ('IGNORECASE', 'MULTILINE', 'DOTALL', 'VERBOSE'):
            frame = None
            if len(self.boxes) % 3 == 0:
                frame = tkinter.Frame(self.tk)
                frame.pack(fill=tkinter.X)
                self.frames.append(frame)

            var = tkinter.IntVar()
            self.vars.append(var)

            box = tkinter.Checkbutton(
                frame,
                variable=var,
                text=name,
                offvalue=0,
                onvalue=getattr(re, name).value,
                command=self.re_compile,
            )
            box.pack(side=tkinter.LEFT)
            self.boxes.append(box)

    def getflags(self):
        flags = 0
        for var in self.vars:
            flags = flags | var.get()
        return flags

    def re_compile(self, event: Union[object, None] = None):
        try:
            self.compiled = re.compile(self.regex_display.get(), self.getflags())
            self.status_display.config(
                text='', background=self.prompt_display['background']
            )
        except re.error as msg:
            self.compiled = None
            self.status_display.config(
                text=f're.error: {msg}', background=self.status_background
            )
        self.re_evaluate()

    def re_evaluate(self, event: Union[object, None] = None):
        try:
            self.string_display.tag_remove('hit', '1.0', tkinter.END)
        except tkinter.TclError:
            pass
        try:
            self.string_display.tag_remove('hit0', '1.0', tkinter.END)
        except tkinter.TclError:
            pass
        self.group_list.delete(0, tkinter.END)
        if not self.compiled:
            return
        self.string_display.tag_configure('hit', background=self.string_hit_background)
        self.string_display.tag_configure('hit0', background=self.string_background)
        text = self.string_display.get('1.0', tkinter.END)
        last = 0
        nmatches = 0
        while last <= len(text):
            m = self.compiled.search(text, last)
            if m is None:
                break
            first, last = m.span()
            if last == first:
                last = first + 1
                tag = 'hit0'
            else:
                tag = 'hit'
            pfirst = f'1.0 + {first} chars'
            plast = f'1.0 + {last} chars'
            self.string_display.tag_add(tag, pfirst, plast)
            if nmatches == 0:
                self.string_display.yview_pickplace(pfirst)
                groups = list(m.groups())
                groups.insert(0, m.group())
                for i in range(len(groups)):
                    self.group_list.insert(tkinter.END, f'{i:=2}: {groups[i]}')
            nmatches = nmatches + 1
            if self.showvar.get() == 'first':
                break

        if nmatches == 0:
            self.status_display.config(
                text='(no match)', background=self.status_background
            )
        else:
            self.status_display.config(text='')


if __name__ == '__main__':
    tk = tkinter.Tk(className='re-tk: tiny TK-GUI for RE')
    ReTK(tk)
    tk.protocol('WM_DELETE_WINDOW', tk.quit)
    tk.mainloop()
