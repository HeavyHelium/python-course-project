import tkinter as tk 
from tkinter.filedialog import askopenfilename, asksaveasfilename
from configs import FontConfig, ModeConfig


class ModeMenu(tk.Menu): 
    MODES = [ModeConfig.DarkMode(), 
             ModeConfig.LightMode(), 
             ModeConfig.ShBishMode()]
    
    def __init__(self, master, root):
        super().__init__(master, 
                         tearoff=0)
        self.root = root
        self.add_modes()
    
    def add_modes(self):
        for mode in ModeMenu.MODES:
            self.add_command(label=mode.name, 
                             command=lambda mode=mode: 
                             self.root.set_mode(mode))

class FileMenu(tk.Menu):
    FILE_TYPES = [('Prolog Files', '*.pl'), 
                  ('Text Files', '*.txt')]
    
    def __init__(self, master, root):
        super().__init__(master, 
                         tearoff=0)
        self.root = root
        self.add_commands()

    def add_commands(self):
        self.add_command(label='New', 
                         command=self.new)
        self.add_command(label='Open', 
                         command=self.open)
        self.add_command(label='Save', 
                         command=self.save)
        self.add_command(label='Save As', 
                         command=self.save_as)
        self.add_separator()
        self.add_command(label='Exit', 
                         command=self.exit) 

    def save_as(self): 
        filepath = asksaveasfilename(filetypes=FileMenu.FILE_TYPES)
        if not filepath: 
            return
        self.root.text_pad.save_as(filepath)

    def save(self): 
        if not self.root.text_pad.filepath: 
            self.save_as()
        else:
            self.root.text_pad.save_as(self.root.text_pad.filepath)

    def new(self): 
        if not self.root.text_pad.empty():
            self.save()
        self.root.text_pad.text_area.delete('1.0', tk.END)
        self.root.text_pad.filepath = None

    def open(self): 
        if not self.root.text_pad.empty():
            self.save()
        filepath = askopenfilename(filetypes=FileMenu.FILE_TYPES)
        if not filepath: 
            return
        self.root.text_pad.open(filepath)

    def exit(self): 
        if not self.root.text_pad.empty():
            self.save()
        self.root.root.quit()


class FontWindow(tk.Toplevel):
    def __init__(self, master): 
        super().__init__(master.root)
        self.root = master
        self.__configure()
        
    def __configure(self): 
        self.title('Font Selection')
        self.rowconfigure(3, weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.__font_family()
        self._font_size()
        self._apply_button()
        

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
    
    def __font_family(self): 
        family_label = tk.Label(self, text='Font Family:')
        family_label.grid(row=1, column=0, sticky='nsew')

        family_options = tk.OptionMenu(self,
                                       self.root.font_family,
                                       *FontConfig.FONT_FAMILY)
        
        family_options.grid(row=1, column=1, sticky='nsew')

    def _font_size(self): 
        size_label = tk.Label(self, text='Size: ')
        size_label.grid(row=0, column=0, sticky='nsew')

        size_spinbox = tk.Spinbox(self,
                                  from_=FontConfig.FONT_SIZE[0],
                                  to=FontConfig.FONT_SIZE[1], 
                                  textvariable=self.root.font_size)
        size_spinbox.grid(row=0, column=1, sticky='nsew')

    def _apply_button(self): 
        apply_button = tk.Button(self, text='Apply',
                                 command=lambda: 
                                 self.root.set_font(FontConfig(self.root.font_family.get(), 
                                                                 self.root.font_size.get())))        

        apply_button.grid(row=3, column=0, columnspan=2, sticky='nsew')



class Menu(): 
    def __init__(self, master_window):
        self.master = master_window
        self.menu_bar = tk.Menu(self.master.root, 
                                tearoff=0)
        self.master.root.config(menu=self.menu_bar)
        self.menus = {}
        self.__create_menus()

    def __create_menus(self): 
        self.file()
        self.preferences()

    def file(self): 
        self.menus['file'] = FileMenu(self.menu_bar,
                                      self.master)
        self.menu_bar.add_cascade(label='File', 
                                  menu=self.menus['file'])

    def preferences(self): 
        self.menus['preferences'] = tk.Menu(self.menu_bar, 
                                            tearoff=0)
        self.menus['preferences'].add_command(label='Font', 
                                              command=lambda: FontWindow(self.master))
        self.menus['preferences'].add_cascade(label='Mode', 
                                              menu=ModeMenu(self.menus['preferences'], 
                                                            self.master)) 
        
        self.menu_bar.add_cascade(label='Preferences', 
                                  menu=self.menus['preferences'])
   