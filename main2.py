from tkinter import Tk, Button, Frame, Label
from threading import Thread

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        Main(self)
        
        self.mainloop()
        #self.current_frame = None
        #self.page_frame = {
        #    "menu": MainMenu,
        #    }
    
    
    def set_window(self, window, w, h):
        window.geometry('%dx%d+400+300'% (w, h))


class Main():
    def __init__(self, master):
        self.root = master
        #self.root.title("Main Menu")
        self.root.resizable(False, False)
        #self.set_window(self.root, 400, 300)
        self.current_frame=None
        
        container = Frame(self.root)
        #container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for frame_page in (MenuPage, Dictionary):
            page_name = frame_page.__name__
            frame = frame_page(container, self.root)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="W")
        
        self.page_buttons = None
        self.pages = {
            "MenuPage": 1,
            "Dictionary": Dictionary,
            "Stats": 3,
            "Game": 4
            }
        self.show_frame("Dictionary")
        #self.create_page()
    
    def show_frame(self, page_name):
        self.root.title(page_name)
        frame = self.frames[page_name]
        frame.tkraise()
    
    def create_page(self):
        center_col=1
        self.page = Frame(self.root)
        self.page.pack()
        Label(self.page).grid(row=0, stick="W")
        Label(self.page, text="Menu").grid(row=1, stick="W", pady=10)
        
        pages = ["dictionary", "stats", "game"]
        self.page_buttons = []
        row = 2
        for page in pages:
            but = Button(self.page, text=page.capitalize(), command=self.open_page(page) ).grid(row=row, stick="W", pady=10)
            page_buttons.append(page_buttons)
            row+= 1
        
    #def open_page(self, page):

    
    def set_window(self, window, w, h):
        window.geometry('%dx%d+400+300'% (w, h))

class MenuPage(Frame):
    def __init__(self, container, master):
        Frame.__init__(self, master)
        self.root = master
        Label(self).grid(row=0, stick="W")
        Label(self, text="Menu").grid(row=1, stick="W", pady=10)
        
        pages = ["dictionary", "stats", "game"]
        self.page_buttons = []
        row = 2
        for page in pages:
            but = Button(self, text=page.capitalize(), command=lambda: self.root.show_frame(page) ).grid(row=row, stick="W", pady=10)
            self.page_buttons.append(but)
            row+= 1

#needs to be updated with controller 
class Dictionary(Frame):
   def __init__(self, container, master):
        Frame.__init__(self, master)
        self.root = master
        self.root.title("Dictionary")
        self.searchbar = None
        dict_list = ["yes","no","me"]
        
        Label(self, text="Dict").grid(row=1, stick="W", pady=10)
        
    #def create_page(self):
        #Label(self).grid(row=0, stick="W")
        #Label(self, text="Dictionary").grid(row=1, stick="W", pady=10)
        
        
        
def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo.screenheight()

def main():
    app = App()

if __name__ == "__main__":
    app = App()
    #app.mainloop()