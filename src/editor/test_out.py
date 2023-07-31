import tkinter as tk 
from tkinter.filedialog import askopenfilename, asksaveasfilename

class FileMenu(tk.Menu):
    def __init__(self, master_menu): 
        super().__init__(master_menu, tearoff=0)
        master_menu.add_cascade(label='File', menu=self)
        self.master_menu = master_menu
        self.filepath = None
        self.add_command(label='Open', 
                         command=self.open_file)
        self.add_command(label='Save', 
                         command=self.save_file)
        self.add_command(label='Save As', 
                         command=self.save_as)
        self.add_command(label='Exit', 
                         command=self.exit)
        
    def open_file(self): 
        filepath = askopenfilename(
            filetypes=[('Text Files', '*.txt'), 
                       ('All Files', '*.*')])
        if not filepath: 
            print(42)
            return
        self.master_menu.text_area.delete(1.0, tk.END) # it is assumed that the master has a text_area attribute
        with open(filepath, 'r') as file: 
            self.master_menu.text_area.insert(1.0, file.read())
        self.master_menu.title(f'Simple Editor - {filepath}')
        self.filepath = filepath

    def save_as(self): 
        filepath = asksaveasfilename(
            defaultextension='pl', 
            filetypes=[('Prolog', '*.pl'), 
                       ('All Files', '*.*')])
        if not filepath: 
            return
        with open(filepath, 'w') as file: 
            file.write(self.master.text_area.get(1.0, tk.END))
        self.master_menu.title(f'Simple Editor - {filepath}')
        self.filepath = filepath

    def save_file(self):
        if not self.filepath: 
            self.save_as()
        else: 
            with open(self.filepath, 'w') as file: 
                file.write(self.master.text_area.get(1.0, tk.END))
    

    def exit(self):
        self.master.quit()


class simple_editor():
    def __init__(self): 
        self.app = tk.Tk()
        self.app.attributes('-zoomed', True)
        self.menu = tk.Menu(self.app)
        self.app.config(menu=self.menu)
        fm = FileMenu(self.menu)
        self.text_area = tk.Text(self.app, 
                                    font=('Courier', 16), 
                                    wrap=tk.WORD)
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.app.title('Simple Editor')

        self.app.mainloop()
        


import tkinter as tk

class InhEditor(tk.Frame):
    def __init__(self, master): 
        super().__init__(master)
        self.master = master
        self.master.attributes('-zoomed', True)
        self.menu = tk.Menu(self)
        file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label='File', menu=file_menu)
        self.text_area = tk.Text(self, font=('Courier', 16), wrap=tk.WORD)
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.master.config(menu=self.menu)
        self.master.title('Simple Editor')


if __name__ == "__main__":
    root = tk.Tk()
    editor = InhEditor(root)
    root.mainloop()




"""
 class Menu(): 
    def __init__(self, master_window):
        self.master = master_window
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)
        self.menus = {}
        self.create_file_menu()

    def create_file_menu(self): 
        self.menus['file'] = tk.Menu(self.menu_bar, tearoff=0)
        self.menus['file'].add_command(label='New', 
                                       command=self.master.new_file)
        self.menus['file'].add_command(label='Open', 
                                       command=self.master.open_file)
        self.menus['file'].add_command(label='Save',
                                        command=self.master.save_file)
        self.menus['file'].add_command(label='Save As',
                                        command=self.master.save_file_as)
        
        self.menus['file'].add_separator()
        self.menus['file'].add_command(label='Exit',    
                                        command=self.master.exit)
        self.menu_bar.add_cascade(label='File', menu=self.menus['file'])

    
    
"""