"""
Contains various menus classes for the editor
"""

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from typing import List
from src.editor.configs import FontConfig, ModeConfig


class ModeMenu(tk.Menu):
    """
    Represents the mode menu
    """
    MODES: List[ModeConfig] = [ModeConfig.dark_mode(),
                               ModeConfig.light_mode(),
                               ModeConfig.sh_bish_mode()]

    def __init__(self, master: tk.Frame, root: 'simple_editor'):
        super().__init__(master,
                         tearoff=0)
        self.root = root
        self.add_modes()

    def add_modes(self):
        """
        Adds the modes to the menu
        """
        for mode in ModeMenu.MODES:
            self.add_command(label=mode.name,
                             command=lambda mode=mode:
                             self.root.set_mode(mode))

class FileMenu(tk.Menu):
    """
    Represents the file menu
    """
    FILE_TYPES = [('Prolog Files', '*.pl'),
                  ('Text Files', '*.*')]

    def __init__(self, master: tk.Frame, root: 'simple_editor') -> None:
        super().__init__(master,
                         tearoff=0)
        self.root = root
        self.add_commands()
        self.key_bindings()

    def key_bindings(self) -> None:
        """
        Sets the key bindings relevant for saving
        """
        self.root.root.bind("<Control-s>", self.save)

    def add_commands(self) -> None:
        """
        Adds the commands to the menu
        """
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

    def save_as(self) -> None:
        """
        Saves the file as
        """
        filepath: str = asksaveasfilename(filetypes=FileMenu.FILE_TYPES)
        if not filepath:
            return
        self.root.text_pad.save_as(filepath)

    def save(self, event=None) -> None:
        """
        Saves the file
        """
        if not self.root.text_pad.filepath:
            self.save_as()
        else:
            self.root.text_pad.save_as(self.root.text_pad.filepath)

    def new(self) -> None:
        """
        Creates a new file
        """
        if not self.root.text_pad.empty():
            self.save()

        self.root.text_pad.text_area.delete('1.0', tk.END)
        self.root.text_pad.filepath = None

    def open(self) -> None:
        """
        Opens a file
        """
        if not self.root.text_pad.empty():
            self.save()
        filepath = askopenfilename(filetypes=FileMenu.FILE_TYPES)
        if not filepath:
            return
        self.root.text_pad.open(filepath)

    def exit(self) -> None:
        """
        Exits the app
        """
        if not self.root.text_pad.empty():
            self.save()
        self.root.root.quit()


class FontWindow(tk.Toplevel):
    """
    Represents the font window, 
    which opens when the user clicks on the font option
    """
    def __init__(self, master: 'simple_editor') -> None:
        super().__init__(master.root)
        self.root = master
        self.__configure()

    def __configure(self) -> None:
        self.title('Font Selection')
        self.rowconfigure(3, weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.__font_family()
        self._font_size()
        self._apply_button()


        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

    def __font_family(self) -> None:
        family_label = tk.Label(self, text='Font Family:')
        family_label.grid(row=1, column=0, sticky='nsew')

        family_options = tk.OptionMenu(self,
                                       self.root.font_family,
                                       *FontConfig.FONT_FAMILY)

        family_options.grid(row=1, column=1, sticky='nsew')

    def _font_size(self) -> None:
        size_label = tk.Label(self, text='Size: ')
        size_label.grid(row=0, column=0, sticky='nsew')

        size_spinbox = tk.Spinbox(self,
                                  from_=FontConfig.FONT_SIZE[0],
                                  to=FontConfig.FONT_SIZE[1],
                                  textvariable=self.root.font_size)
        size_spinbox.grid(row=0, column=1, sticky='nsew')

    def _apply_button(self) -> None:
        apply_button = tk.Button(self, text='Apply',
                                 command=lambda:
                                 self.root.set_font(FontConfig(self.root.font_family.get(),
                                                               self.root.font_size.get())))

        apply_button.grid(row=3, column=0, columnspan=2, sticky='nsew')



class Menu():
    """
    Represents the menu bar
    """
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
        """
        Creates the file menu
        """
        self.menus['file'] = FileMenu(self.menu_bar,
                                      self.master)
        self.menu_bar.add_cascade(label='File',
                                  menu=self.menus['file'])

    def preferences(self):
        """
        Creates the preferences menu
        """
        self.menus['preferences'] = tk.Menu(self.menu_bar,
                                            tearoff=0)
        self.menus['preferences'].add_command(label='Font',
                                              command=lambda: FontWindow(self.master))
        self.menus['preferences'].add_cascade(label='Mode',
                                              menu=ModeMenu(self.menus['preferences'],
                                                            self.master))

        self.menu_bar.add_cascade(label='Preferences',
                                  menu=self.menus['preferences'])
   