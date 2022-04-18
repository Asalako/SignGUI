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
        self.root.title("Main Menu")
        self.root.resizable(False, False)
        self.set_window(self.root, 400, 300)
        self.current_frame=None
        
        self.page_buttons = None
        self.pages = {
            "menu": 1,
            "dictionary": Dictionary,
            "stats": 3,
            "game": 4
            }
        
        #MenuPage(self.root)
        self.create_page()
    
    def create_page(self):
        #center_col=1
        
        self.page = Frame(self.root)
        self.page.pack()
        Label(self.page).grid(row=0, stick="W")
        Label(self.page, text="Menu").grid(row=1, stick="W", pady=10)
        
        pages = ["dictionary", "stats", "game"]
        self.page_buttons = []
        row = 2
        for page in pages:
            button = Button(self.page, text=page.capitalize(), command=lambda p=page: self.open_page(p.capitalize()) ).grid(row=row, stick="W", pady=10)
            self.page_buttons.append(button)
            row+= 1
            
        self.current_frame = self.page
        
    def open_page(self, page):
        print(page)
        self.root.title(page)
        #self.current_frame.destroy()
        if page == "Dictionary":
            self.current_frame.destroy()
            self.current_frame = Dictionary(self.root)
            self.current_frame.pack()
        elif page == "Stats":
            print('here')
        return
    
    
    def set_window(self, window, w, h):
        window.geometry('%dx%d+400+300'% (w, h))

class MenuPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.root = master
        Label(self.root).grid(row=0, stick="W")
        Label(self.root, text="Menu").grid(row=1, stick="W", pady=10)
        
        pages = ["dictionary", "stats", "game"]
        self.page_buttons = []
        row = 2
        for page in pages:
            button = Button(self.page, text=page.capitalize(), command=lambda p=page: self.open_page(p) ).grid(row=row, stick="W", pady=10)
            self.page_buttons.append(button)
            row+= 1

#needs to be updated with controller 
class Dictionary(Frame):
   def __init__(self, master):
        Frame.__init__(self, master)
        self.root = master
        self.root.title("Dictionary")
        self.searchbar = None
        dict_list = ["yes","no","me"]
        
        print('here')
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