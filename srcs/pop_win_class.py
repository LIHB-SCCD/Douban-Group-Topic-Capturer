import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True


class pop_win(tk.Toplevel):
    def __init__(self, top=None,list_name = None):
        super().__init__()
        self.parent = top;

        #self.parent = self # 显式地保留父窗口
        '''This class configures and populates the selflevel window.
           self is the selflevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        self.geometry("505x755+500+142")
        self.minsize(180, 1)
        self.maxsize(2164, 1410)
        self.resizable(1, 1)
        self.title("列表窗口")
        self.configure(background="#d9d9d9")

        self.Scrolledlistbox1 = ScrolledListBox(self)
        self.Scrolledlistbox1.place(relx=0.02, rely=0.011, relheight=0.977
                , relwidth=0.515)
        self.Scrolledlistbox1.configure(background="white")
        self.Scrolledlistbox1.configure(cursor="xterm")
        self.Scrolledlistbox1.configure(disabledforeground="#a3a3a3")
        self.Scrolledlistbox1.configure(font="TkFixedFont")
        self.Scrolledlistbox1.configure(foreground="black")
        self.Scrolledlistbox1.configure(highlightbackground="#d9d9d9")
        self.Scrolledlistbox1.configure(highlightcolor="#d9d9d9")
        self.Scrolledlistbox1.configure(selectbackground="#c4c4c4")
        self.Scrolledlistbox1.configure(selectforeground="black")
        self.Scrolledlistbox1.configure(selectmode="extended")

        self.delete = tk.Button(self)
        self.delete.place(relx=0.574, rely=0.901, height=40, width=195)
        self.delete.configure(activebackground="#ececec")
        self.delete.configure(activeforeground="#000000")
        self.delete.configure(background="#d9d9d9")
        self.delete.configure(command=self.on_button_delete)
        self.delete.configure(disabledforeground="#a3a3a3")
        self.delete.configure(foreground="#000000")
        self.delete.configure(highlightbackground="#d9d9d9")
        self.delete.configure(highlightcolor="black")
        self.delete.configure(pady="0")
        self.delete.configure(text='''删除''')

        self.add = tk.Button(self)
        self.add.place(relx=0.574, rely=0.821, height=40, width=195)
        self.add.configure(activebackground="#ececec")
        self.add.configure(activeforeground="#000000")
        self.add.configure(background="#d9d9d9")
        self.add.configure(command=self.on_button_add)
        self.add.configure(disabledforeground="#a3a3a3")
        self.add.configure(foreground="#000000")
        self.add.configure(highlightbackground="#d9d9d9")
        self.add.configure(highlightcolor="black")
        self.add.configure(pady="0")
        self.add.configure(text='''添加''')

        self.Entry1 = tk.Entry(self)
        self.Entry1.place(relx=0.574, rely=0.768,height=24, relwidth=0.384)
        self.Entry1.configure(background="white")
        self.Entry1.configure(disabledforeground="#a3a3a3")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(foreground="#000000")
        self.Entry1.configure(insertbackground="black")

        #self.protocol("WM_DELETE_WINDOW", self.on_button_save_exit);

        self.__list_name = list_name;


        if (list_name == 'bad_author_list'):
            self.__the_list = top.dbf.get_bad_author_list()

        elif list_name == 'good_author_list':
            self.__the_list = top.dbf.get_good_author_list()

        elif list_name == 'bad_word_list':
            self.__the_list = top.dbf.get_bad_word_list()

        elif list_name == 'good_word_list':
            self.__the_list = top.dbf.get_good_word_list()
        else:
            pass;     
        self.update_list();
                            
    def on_button_save_exit(self):
        if (self.__list_name == 'bad_author_list'):
            self.parent.dbf.set_bad_author_list(self.__the_list,False);

        elif self.__list_name == 'good_author_list':
            self.parent.dbf.set_good_author_list(self.__the_list,False);

        elif self.__list_name == 'bad_word_list':
            self.parent.dbf.set_bad_word_list(self.__the_list,False);

        elif self.__list_name == 'good_word_list':
            self.parent.dbf.set_good_word_list(self.__the_list,False);
        else:
            pass;   



    def on_button_delete(self):

        selected = self.Scrolledlistbox1.curselection();
        for idx in selected:
            item = self.Scrolledlistbox1.get(idx);
            #print(item);
            #strs = item;
            self.__the_list.remove(item);
        self.update_list();

    def on_button_add(self):
        text = self.Entry1.get();
        self.__the_list.append(text);
        self.update_list();
        pass;

    def update_list(self):
        #len_list = self.Scrolledlistbox1.size();
        #print(len_list);
        self.Scrolledlistbox1.delete(0,1008611);
        for i in range(0,len(self.__the_list)) :
            word = self.__the_list[i];
            self.Scrolledlistbox1.insert(i,word)
        self.on_button_save_exit();

# The following code is added to facilitate the Scrolled widgets you specified.
class AutoScroll(object):
    '''Configure the scrollbars for a widget.'''
    def __init__(self, master):
        #  Rozen. Added the try-except clauses so that this class
        #  could be used for scrolled entry widget for which vertical
        #  scrolling is not supported. 5/7/14.
        try:
            vsb = ttk.Scrollbar(master, orient='vertical', command=self.yview)
        except:
            pass
        hsb = ttk.Scrollbar(master, orient='horizontal', command=self.xview)
        try:
            self.configure(yscrollcommand=self._autoscroll(vsb))
        except:
            pass
        self.configure(xscrollcommand=self._autoscroll(hsb))
        self.grid(column=0, row=0, sticky='nsew')
        try:
            vsb.grid(column=1, row=0, sticky='ns')
        except:
            pass
        hsb.grid(column=0, row=1, sticky='ew')
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure(0, weight=1)
        # Copy geometry methods of master  (taken from ScrolledText.py)
        if py3:
            methods = tk.Pack.__dict__.keys() | tk.Grid.__dict__.keys() \
                  | tk.Place.__dict__.keys()
        else:
            methods = tk.Pack.__dict__.keys() + tk.Grid.__dict__.keys() \
                  + tk.Place.__dict__.keys()
        for meth in methods:
            if meth[0] != '_' and meth not in ('config', 'configure'):
                setattr(self, meth, getattr(master, meth))

    @staticmethod
    def _autoscroll(sbar):
        '''Hide and show scrollbar as needed.'''
        def wrapped(first, last):
            first, last = float(first), float(last)
            if first <= 0 and last >= 1:
                sbar.grid_remove()
            else:
                sbar.grid()
            sbar.set(first, last)
        return wrapped

    def __str__(self):
        return str(self.master)

def _create_container(func):
    '''Creates a ttk Frame with a given master, and use this new frame to
    place the scrollbars and the widget.'''
    def wrapped(cls, master, **kw):
        container = ttk.Frame(master)
        container.bind('<Enter>', lambda e: _bound_to_mousewheel(e, container))
        container.bind('<Leave>', lambda e: _unbound_to_mousewheel(e, container))
        return func(cls, container, **kw)
    return wrapped

class ScrolledListBox(AutoScroll, tk.Listbox):
    '''A standard Tkinter Listbox widget with scrollbars that will
    automatically show/hide as needed.'''
    @_create_container
    def __init__(self, master, **kw):
        tk.Listbox.__init__(self, master, **kw)
        AutoScroll.__init__(self, master)
    def size_(self):
        sz = tk.Listbox.size(self)
        return sz

import platform
def _bound_to_mousewheel(event, widget):
    child = widget.winfo_children()[0]
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        child.bind_all('<MouseWheel>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-MouseWheel>', lambda e: _on_shiftmouse(e, child))
    else:
        child.bind_all('<Button-4>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Button-5>', lambda e: _on_mousewheel(e, child))
        child.bind_all('<Shift-Button-4>', lambda e: _on_shiftmouse(e, child))
        child.bind_all('<Shift-Button-5>', lambda e: _on_shiftmouse(e, child))

def _unbound_to_mousewheel(event, widget):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        widget.unbind_all('<MouseWheel>')
        widget.unbind_all('<Shift-MouseWheel>')
    else:
        widget.unbind_all('<Button-4>')
        widget.unbind_all('<Button-5>')
        widget.unbind_all('<Shift-Button-4>')
        widget.unbind_all('<Shift-Button-5>')

def _on_mousewheel(event, widget):
    if platform.system() == 'Windows':
        widget.yview_scroll(-1*int(event.delta/120),'units')
    elif platform.system() == 'Darwin':
        widget.yview_scroll(-1*int(event.delta),'units')
    else:
        if event.num == 4:
            widget.yview_scroll(-1, 'units')
        elif event.num == 5:
            widget.yview_scroll(1, 'units')

def _on_shiftmouse(event, widget):
    if platform.system() == 'Windows':
        widget.xview_scroll(-1*int(event.delta/120), 'units')
    elif platform.system() == 'Darwin':
        widget.xview_scroll(-1*int(event.delta), 'units')
    else:
        if event.num == 4:
            widget.xview_scroll(-1, 'units')
        elif event.num == 5:
            widget.xview_scroll(1, 'units')
