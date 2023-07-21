import tkinter as tk 
from configs import FontConfig, ModeConfig
from text_pad import TextPad
from query_frame import QueryFrame
from menus import Menu



class simple_editor(): 
    def __init__(self, mode_config=ModeConfig.ShBishMode()):
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


    def run(self): 
        self.root.title('Simple Editor')
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.mainloop()

    def set_font(self, font_config=FontConfig('Courier', 16)):
        self.text_pad.set_font(font_config)
        self.query_frame.set_font(font_config)

        self.font_family.set(font_config.family)
        self.font_size.set(font_config.size)
        

    def set_mode(self, mode_config): 
        self.root.configure(bg=mode_config.bg)
        self.query_frame.set_mode(mode_config)
        self.text_pad.set_mode(mode_config)

        self.set_font(mode_config.font_config)
        

if __name__ == "__main__":
    editor = simple_editor()
    editor.run()
