from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename

from configs import FontConfig, ModeConfig


"""
TODO: 
* refactor
* fix numbering after window limit
* ?add syntax highlighting
* shortcut keys
* autosave 
* undo, redo
"""

class Editor:
    MODES = [ModeConfig.LightMode(),
             ModeConfig.DarkMode(),
             ModeConfig.ShBishMode()]

    def __init__(self, name, mode_config=ModeConfig.ShBishMode()):
        self.name = name
        self.window = Tk()
        self.window.title(self.name)

        self.font_family = StringVar(self.window)
        self.font_size = StringVar(self.window)
        self.line_count = 1

        self.create_widgets()
        self.bind_keys()

        self.set_mode(mode_config)

    def apply_font(self, font_config):
        # Set the font and its size in the text area
        self.txt.config(font=(font_config.family, 
                              font_config.size))
        self.line_number_bar.config(font=(font_config.family, 
                                          font_config.size))

    def set_mode(self, mode_config):
        self.window.configure(bg=mode_config.bg)
        self.txt.configure(bg=mode_config.bg, 
                           fg=mode_config.fg)
        
        self.line_number_bar.configure(bg=mode_config.bg, 
                                       fg=mode_config.fg)

        self.apply_font(mode_config.font_config)

        self.font_family.set(mode_config.font_config.family)
        self.font_size.set(str(mode_config.font_config.size))

    def bind_keys(self):
        self.txt.bind("<Return>", 
                      self.handle_return)
        self.txt.bind("<BackSpace>", 
                      self.handle_backspace)
        self.txt.bind("<Configure>", 
                      self.update_line_numbers)
        self.txt.bind("<MouseWheel>", 
                      self.scroll_text)

    def handle_return(self, event):
        self.line_count += 1
        self.update_line_numbers()

    def handle_backspace(self, event):
        content = self.txt.get("1.0", "end-1c")
        newline_count = content.count('\n')
        self.line_count = newline_count + 1 if len(content) > 1 else 1
        self.update_line_numbers()

    def create_widgets(self):
        self.__create_text_area()
        self.__create_line_number_bar()
        self.__create_menu()
        self.__create_scrollbar()

        self.txt.bind('<Key>', 
                      self.update_line_numbers)
        self.txt.bind('<Button-1>', 
                      self.update_line_numbers)
        self.txt.bind('<MouseWheel>',
                      self.update_line_numbers)

    def __create_text_area(self):
        self.txt = Text(self.window)
        self.txt.grid(row=0, 
                      column=1, 
                      sticky='nsew')

    def __create_menu(self):
        menu_bar = Menu(self.window)
        self.window.config(menu=menu_bar)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Open', 
                              command=self.open_file)
        file_menu.add_command(label='Save as', 
                              command=self.save_file)

        menu_bar.add_cascade(label='File', 
                             menu=file_menu)

        pref_menu = Menu(menu_bar, 
                         tearoff=0)
        menu_bar.add_cascade(label='Preferences', 
                             menu=pref_menu)

        pref_menu.add_command(label='Font', 
                              command=self.open_font_window)
        mode_menu = Menu(pref_menu, 
                         tearoff=0)

        for mode in Editor.MODES:
            mode_menu.add_command(label=mode.name, 
                                  command=lambda mode=mode: self.set_mode(mode))

        pref_menu.add_cascade(label='Mode', 
        menu=mode_menu)

    def open_font_window(self):
        # Open a new window for font selection
        font_window = Toplevel(self.window)
        font_window.title("Font Selection")
        font_window.rowconfigure(3, weight=1)
        font_window.columnconfigure((0, 1), weight=1)

        # Label and spinbox for selecting the font size
        size_label = Label(font_window, 
                           text="Font Size:")
        size_label.grid(row=0, 
                        column=0, 
                        sticky='e')
        size_spinbox = Spinbox(font_window, 
                               from_=FontConfig.FONT_SIZE[0], 
                               to=FontConfig.FONT_SIZE[-1],
                               textvariable=self.font_size)
        size_spinbox.grid(row=0, 
                          column=1, 
                          sticky='w')

        # Label and drop-down menu for selecting the font family
        family_label = Label(font_window, 
                             text="Font Family:")
        family_label.grid(row=1, 
                          column=0, 
                          sticky='e')
        family_optionmenu = OptionMenu(font_window, 
                                       self.font_family, 
                                       *FontConfig.FONT_FAMILY)
        family_optionmenu.grid(row=1, 
                               column=1, 
                               sticky='w')

        # Button to apply the selected font
        apply_button = Button(font_window, 
                              text="Apply",
                              command=lambda: self.apply_font(FontConfig(self.font_family.get(),
                                                                          self.font_size.get())))
        apply_button.grid(row=3, 
                          column=0, 
                          columnspan=2, 
                          sticky='nsew')

        # Configure resizing behaviour
        font_window.grid_rowconfigure(2, weight=1)
        font_window.grid_columnconfigure((0, 1), weight=1)

    def __create_scrollbar(self):
        self.scrollbar = Scrollbar(self.window, 
                                   command=self.scroll_text)
        self.scrollbar.grid(row=0, 
                            column=2, 
                            sticky='ns')
        self.txt.configure(yscrollcommand=self.scrollbar.set)

    def __create_line_number_bar(self):
        self.line_number_bar = Text(self.window, 
                                    width=3)
        self.line_number_bar.grid(row=0, 
                                  column=0, 
                                  sticky='ns')
        self.line_number_bar.configure(state="disabled")

    def scroll_text(self, *args):
        # Synchronize the scrollbar with text area scrolling
        self.line_number_bar.yview_moveto(*args)
        self.txt.yview_moveto(*args[0])

    def open_file(self):
        filepath = askopenfilename(filetypes=[("Prolog Files", "*.pl"), 
                                              ("All Files", "*.*")])
        if not filepath:
            return
        self.txt.delete(1.0, END)
        with open(filepath, "r", encoding='utf-8') as input_file:
            text = input_file.read()
            self.txt.insert(END, text)
        self.window.title(f"{self.name} - {filepath}")
        self.update_line_numbers()

    def save_file(self):
        filepath = asksaveasfilename(defaultextension="pl", 
                                     filetypes=[("Prolog Files", "*.pl"), 
                                                ("All Files", "*.*")])
        if not filepath:
            return
        with open(filepath, "w", encoding='utf-8') as output_file:
            text = self.txt.get(1.0, END)
            output_file.write(text)
        self.window.title(f"{self.name} - {filepath}")

    def update_line_numbers(self, *args):
        self.line_number_bar.configure(state="normal")
        self.line_number_bar.delete(1.0, END)

        line_numbers_text = '\n'.join(str(i) for i 
                                      in range(1, self.line_count + 1))

        self.line_number_bar.insert(END, 
                                    line_numbers_text)
        self.line_number_bar.configure(state="disabled")

    def run(self):
        self.window.geometry("800x600")
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.attributes('-zoomed', True)
        self.window.mainloop()


if __name__ == "__main__":
    editor = Editor("SWISH BISH Prolog")
    editor.run()
