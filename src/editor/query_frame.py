import tkinter as tk 
from configs import FontConfig, ModeConfig


class QueryFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(row=0, column=3)
        self._create_query_frame()
        self.set_mode()
    
    def _create_query_frame(self):
        self._create_input_frame()
        self._create_output_frame()
        
        self.run_button = tk.Button(self.inputframe, text='Run')
        self.run_button.grid(row=1, column=0, sticky='nsew')

    def _create_input_frame(self):
        self.inputframe = tk.LabelFrame(self, text='?-', font=('Courier', 16))
        self.inputframe.grid(row=0, column=0, sticky='nsew', pady=10)
        self.input = tk.Entry(self.inputframe, width=80)
        self.input.grid(row=0, column=0, sticky='nsew')
    
    def _create_output_frame(self):
        self.outputframe = tk.LabelFrame(self, text='Output', font=('Courier', 16))
        self.outputframe.grid(row=1, column=0, sticky='nsew', pady=10) 
        self.output = tk.Text(self.outputframe)
        self.output.grid(row=0, column=0, sticky='nsew')

    def set_font(self, font_config=FontConfig('Courier', 16)):
        elems = [self.inputframe, self.outputframe,
                 self.output, self.input, 
                 self.run_button]
        for elem in elems:
            elem.config(font=(font_config.family, 
                              font_config.size))
        
    def set_mode(self, mode_config=ModeConfig.DarkMode()):
        elems = [self.inputframe, self.outputframe,
                 self.output, self.input, self.run_button]
        for elem in elems:
            elem.config(bg=mode_config.bg, 
                        fg=mode_config.fg)
        self.set_font(mode_config.font_config)
        self.config(bg=mode_config.bg)
