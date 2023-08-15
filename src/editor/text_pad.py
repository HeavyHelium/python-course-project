"""
Represents the typing area of the editor
"""
import tkinter as tk
from src.editor.configs import FontConfig, ModeConfig


class TextPad():
    """
    Represents the typing area of the editor
    """
    def __init__(self, master: tk.Frame) -> None:
        self.text_area: tk.Text = tk.Text(master)
        self.text_area.grid(row=0, column=1, sticky='nsew')
        self.number_bar: tk.Text = tk.Text(master, width=3)
        self.number_bar.grid(row=0, column=0, sticky='nsew')

        self.filepath: str = None

        self.scrollbar: tk.Scrollbar = tk.Scrollbar(master)
        self.scrollbar.grid(row=0, column=2, sticky='nsew')

        self.scrollbar['command'] = self.on_scroll
        self.text_area['yscrollcommand'] = self.on_textscroll
        self.number_bar['yscrollcommand'] = self.on_textscroll

        self.key_bindings()

    def key_bindings(self) -> None:
        """
        Binds the keypress event to the text area
        """
        self.text_area.bind('<KeyPress>', self.on_keypress)

    def on_keypress(self, event=None):
        """
        Updates the line numbers when a key is pressed
        """
        #print(f"Pressed {event.keysym}")
        self.update_number_bar()

    def on_scroll(self, *args) -> None:
        """
        Scrolls the text area and the number bar
        """
        self.text_area.yview(*args)
        self.number_bar.yview(*args)

    def on_textscroll(self, *args):
        """
        Scrolls the scrollbar
        """
        self.scrollbar.set(*args)
        self.on_scroll('moveto', args[0])

    def set_font(self, font_config=FontConfig('Courier', 16)):
        """
        Sets the font of the text area
        """
        elements = [self.number_bar, self.text_area]
        for elem in elements:
            elem.config(font=(font_config.family,
                              font_config.size))

    def set_mode(self, mode_config=ModeConfig.dark_mode()) -> None:
        """
        Sets the mode of the text area
        """
        elements = [self.number_bar, self.text_area]
        for elem in elements:
            elem.config(bg=mode_config.bg,
                        fg=mode_config.fg)
        self.set_font(mode_config.font_config)

    def get_line_numbers(self) -> None:
        """
        Returns the line numbers of the text area
        """
        line, _ = self.text_area.index('end').split('.')
        return list(range(1, int(line)))

    def update_number_bar(self) -> None:
        """
        Updates the line numbers of the text area
        """
        line_numbers = self.get_line_numbers()
        line_numbers = '\n'.join(str(x) for x in line_numbers)
        self.number_bar.delete('1.0', tk.END)
        self.number_bar.insert('1.0', line_numbers)

    def save_as(self, filepath) -> None:
        """
        Saves the text area to a file
        """
        with open(filepath, 'w') as f:
            f.write(self.text_area.get('1.0', tk.END))
        self.filepath = filepath

    def get_src(self) -> str:
        """
        Returns the text in the text area
        """
        return self.text_area.get('1.0', tk.END)

    def empty(self) -> bool:
        """
        Returns True if the text area is empty
        """
        return self.text_area.get('1.0', tk.END) == '\n'

    def open(self, filepath) -> None:
        with open(filepath, 'r') as f:
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert('1.0', f.read())
        self.filepath = filepath
        self.update_number_bar()

