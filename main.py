from tkinter import Tk, Button, Frame, Label, Entry, Scrollbar, Canvas
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
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
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
        self.page.grid(row=0, column=0)
        self.page.grid_rowconfigure(0, weight=1)
        self.page.grid_columnconfigure(0, weight=1)
        #Label(self.page).grid(row=0, column=0, sticky="NESW")
        Label(self.page, text="Menu").grid(row=1, sticky="NESW")
        
        pages = ["dictionary", "stats", "game"]
        self.page_buttons = []
        row = 2
        for page in pages:
            button = Button(self.page, text=page.capitalize(),
                            command=lambda p=page: self.open_page(p.capitalize()))
            button.grid(row=row, sticky="NEW", pady=10)
            self.page_buttons.append(button)
            row+= 1
            
        self.current_frame = self.page
        
    def open_page(self, page):
        print(page)
        self.root.title(page)
        #self.current_frame.destroy() change this after slides have been created
        if page == "Dictionary":
            self.current_frame.destroy()
            self.current_frame = Dictionary(self.root)
            self.current_frame.grid(row=0)
            self.current_frame.grid_rowconfigure(0, weight=1)
            self.current_frame.grid_columnconfigure(0, weight=1)
        elif page == "Stats":
            print('here')
        return
    
    
    def set_window(self, window, w, h):
        window.geometry('%dx%d+400+300'% (w, h))
#Most likely redundant
class MenuPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.root = master
        Label(self.root)
        Label.grid(row=0, sticky="W")
        Label(self.root, text="Menu")
        Label.grid(row=1, sticky="W", pady=10)
        
        pages = ["dictionary", "stats", "game"]
        self.page_buttons = []
        row = 2
        for page in pages:
            button = Button(self.page, text=page.capitalize(), command=lambda p=page: self.open_page(p))
            button.grid(row=row, sticky="W", pady=10)
            self.page_buttons.append(button)
            row+= 1

#needs to be updated with controller 
class Dictionary(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.vframe = VerticalScrolledFrame(master)
        self.vframe.pack()
        self.root = master
        self.root.title("Dictionary")
        self.searchbar = None
        
        Label(self, text="Dict").grid(row=1, sticky="W", pady=10)
        Label(self, text="Search: ").grid(row=2, column=0,  sticky="W", pady=10)
        self.searchbar = Entry(
            self, width=20).grid(row=2, column=1,  sticky="W", pady=10)
        
        #self.search_results(self, master)
        
    #def create_page(self):
        #Label(self).grid(row=0, sticky="W")
        #Label(self, text="Dictionary").grid(row=1, sticky="W", pady=10)
        
    def search_results(self, frame, master):
        view_frame = Frame(frame, bg="white", width=200, height=200)
        #view_frame.grid_rowconfigure(0, weight=1)
        #view_frame.grid_columnconfigure(0, weight=1)
        #view_frame.grid(
        #    row=3, sticky="EW", columnspan=2)
        
        canvas = Canvas(view_frame)
        #canvas.pack(fill="both", expand=1)
        
        dict_list = ["yes","no","me", "yes","no","me", "yes","no","me"]
        
        vscrollbar = Scrollbar(view_frame, orient="vertical", command=canvas.yview)
        sec_frame = Frame(canvas)
        #vscrollbar.pack(side = "right", fill = "y")
        #vscrollbar.config()
        
        canvas.bind('<Configure>',
                    lambda e: canvas.configure(scrollregion = canvas.bbox("all")))
        
        canvas.create_window((0,0), window=sec_frame, anchor="nw")
        canvas.configure(yscrollcommand=vscrollbar.set)
        
        self.options = []
        row = 0
        #but = Button(view_frame, text="hello")
        #but.pack()
        for option in dict_list:
            button = Button(sec_frame, text=option.capitalize() )
            #button.grid(row=row, sticky="W", pady=10)
            button.pack()
            self.options.append(button)
            row+= 1
        
        view_frame.grid(row=3)
        
        #vscrollbar.pack(side = "right", fill = "y")
        vscrollbar.grid(row = 1, column=1, sticky = "N")
        sec_frame.grid(row=3)
        #canvas.pack(fill="both", expand=1)
        canvas.grid(row=3)
        
        
    def open_page(self, o):
        return
        
class VerticalScrolledFrame(Frame):
    def __init__(self, master):
        vscrollbar = Scrollbar(master, orient="vertical")
        vscrollbar.pack(side = "right", fill = "y")
        canvas = Canvas(master, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        vscrollbar.config(command=canvas.yview)
        
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)
        
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0,0, window=interior, anchor="nw")
        
        def _configure_interior(event):
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            
            if interior.winfo_reqwidth() != canvas.winfo_width():
                
                canvas.config(width=interior.winfo_reqwidth())
        interior('<Configure>', _configure_interior)
        
        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo.screenheight()

def main():
    app = App()

if __name__ == "__main__":
    app = App()
    #app.mainloop()