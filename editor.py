"""
Module to represent the main editor
Also the starting point of the app
"""

import tkinter as tk

from src.editor.configs import FontConfig, ModeConfig
from src.editor.text_pad import TextPad
from src.editor.query_frame import QueryFrame
from src.editor.menus import Menu

from src.interpreter.interpreter import Interpreter


class SimpleEditor():
    """
    The main class for the app
    """
    NAME: str = 'Swish Bish Prolog'

    def __init__(self,
                 mode_config: ModeConfig = ModeConfig.sh_bish_mode()) -> None:
        self.root = tk.Tk()
        self.root.configure(bg='green')
        self.root.attributes('-zoomed', True)

        self.query_frame = QueryFrame(self.root)
        self.number_bar = tk.Text(self.root, width=3)
        self.number_bar.grid(row=0, column=0, sticky='nsew')

        self.text_pad = TextPad(self.root)

        self.font_family = tk.StringVar()
        self.font_size = tk.IntVar()

        self.font_family.set(mode_config.font_config.family)
        self.font_size.set(mode_config.font_config.size)

        self.set_mode(mode_config)
        self.menu = Menu(self)

        self.query_frame.run_button.config(command=self.run_query)

        self.key_bindings()

    def key_bindings(self) -> None:
        """
        Binds the keypress event to the text area
        """
        self.root.bind("<Control-s>", self.menu.menus['file'].save)
        self.root.bind("<Control-v>", self.text_pad.update_number_bar())
        self.root.bind("<Control-Return>", self.run_query)
    
    def run(self) -> None:
        """
        Runs the app
        """
        self.root.title(SimpleEditor.NAME)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.mainloop()

    def set_font(self,
                 font_config: FontConfig = FontConfig('Courier', 16)) -> None:
        """
        Sets the font of the editor
        """
        self.text_pad.set_font(font_config)
        self.query_frame.set_font(font_config)

        self.font_family.set(font_config.family)
        self.font_size.set(font_config.size)


    def set_mode(self,
                 mode_config: ModeConfig) -> None:
        """
        Sets the mode of the editor
        """
        self.root.configure(bg=mode_config.bg)
        self.query_frame.set_mode(mode_config)
        self.text_pad.set_mode(mode_config)

        self.set_font(mode_config.font_config)


    def run_query(self, event=None) -> None:
        """
        Takes the query from the query frame and runs it
        """
        query: str = self.query_frame.get_query()
        src: str = self.text_pad.get_src()

        intr: Interpreter = Interpreter()
        try:
            intr.load_base_direct(src)
        except Exception as e:
            self.query_frame.set_text(str(e))
            return

        try:
            res = str(intr.answer(query))
            self.query_frame.set_text(res)
        except Exception as e:
            self.query_frame.set_text(str(e))


if __name__ == "__main__":
    editor: SimpleEditor = SimpleEditor()
    editor.run()
