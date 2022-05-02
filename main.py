from tkinter import Tk, Button, Frame, Label, Entry, Scrollbar, Canvas, Listbox
from PIL import ImageTk, Image
from threading import Thread
import app
import os, cv2, csv, itertools, copy, random
import numpy as np
import mediapipe as mp
from model import KeyPointClassifier


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

#edit this to run at main
class Main():
    def __init__(self, master):
        self.root = master
        self.root.title("Main Menu")
        self.root.resizable(True, True)
        self.set_window(self.root, 800, 600)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.current_frame=None
        self.page_buttons = None
        self.pages = {
            "Menu": MenuPage,
            "Dictionary": Dictionary,
            "Stats": StatsPage,
            "Game": GameFrame
            }
        
        #self.vertical_scroll()
        #MenuPage(self.root)
        self.create_page()
    
    def vertical_scroll(self):
        frame = Frame(self.root)
        frame.pack(fill="both", expand=1)
        
        canvas = Canvas(frame)
        canvas.pack(side="left", fill="both", expand=1)
        
        vscrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
        vscrollbar.pack(side="right", fill="y")
        
        canvas.configure(yscrollcommand=vscrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))
        
        self.secframe = Frame(canvas)
        canvas.create_window((0,0), window=self.secframe, anchor="nw")
        
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
            self.root.title("Dictionary")
            self.current_frame = self.pages["Dictionary"](self.root, self)
            self.current_frame.pack()
            #self.current_frame.grid(row=0)
            #self.current_frame.grid_rowconfigure(0, weight=1)
            #self.current_frame.grid_columnconfigure(0, weight=1)
        elif page == "Stats":
            self.current_frame.destroy()
            self.root.title("Stats")
            self.current_frame = self.pages["Stats"](self.root)
            self.current_frame.pack()
        elif page == "Game":
            self.current_frame.destroy()
            self.root.title("Game")
            self.current_frame = self.pages["Game"](self.root)
            self.current_frame.pack()
        return
    
    
    def set_window(self, window, w, h):
        window.geometry('%dx%d+400+300'% (w, h))
#Most likely redundant
class MenuPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.root = master
        Label(self)
        Label.grid(row=0, sticky="W")
        Label(self, text="Menu")
        Label.grid(row=1, sticky="W", pady=10)
        
        pages = ["dictionary", "stats", "game"]
        self.page_buttons = []
        row = 2
        for page in pages:
            button = Button(self, text=page.capitalize(),
                            command=lambda p=page: self.root.open_page(p))
            button.grid(row=row, sticky="W", pady=10)
            self.page_buttons.append(button)
            row+= 1

#needs to be updated with controller 
class Dictionary(Frame):
    def __init__(self, master, main):
        Frame.__init__(self, master)
        #self.scrollframe = Main.secframe
        self.root = master
        self.main = main
        self.searchbar = None
        self.results = None
        self.dict_list = None
        self.sel_button = None
        
        self.create_page()

    def create_page(self):
        self.results = Listbox(self)
        Label(self, text="Dict").grid(row=1, column=1, sticky="W", pady=10)
        Label(self, text="Search: ").grid(row=2, column=0,  sticky="W", pady=10)
        self.searchbar = Entry(
            self, width=20).grid(row=2, column=1,  sticky="W", pady=10)
        
        #self.search_results()
        
        #sort the options in alphabetical
        self.dict_list = ["close","good","i love you", "maybe", "ok" ,
                     "open", "peace", "point", "victory", "zero"]
        
        for option in self.dict_list:
            self.results.insert("end",option)
            
        self.results.grid(row=3, column=1,  sticky="W", pady=1)
        
        self.sel_button = Button(self, text="Select Option",
                                 command=self.open_page)
        self.sel_button.grid(row=4, column=1,  sticky="W", pady=1)

    def open_page(self):
        option = self.results.get("anchor")
        if option == "":
            return
        #self.root.title(option)
        #self.current_frame.destroy() change this after slides have been created
        self.destroy()
        self.root.title("Viewer")
        self.root.current_frame = ViewerFrame(self.root, self, self.dict_list, option)
        self.root.current_frame.pack()
        #self.current_frame.grid(row=0, column=0)
        #self.current_frame.grid(row=0)
        #self.current_frame.grid_rowconfigure(0, weight=1)
        #self.current_frame.grid_columnconfigure(0, weight=1)
        return

    def select_result(self):
        value = self.results.get("anchor")
        print (value)

    #def create_page(self):
        #Label(self).grid(row=0, sticky="W")
        #Label(self, text="Dictionary").grid(row=1, sticky="W", pady=10)
        
    def search_results(self):
        
        dict_list = ["yes","no","me", "yes","no","me", "yes","no","me"]
        
        self.options = []
        row = 0
        #but = Button(view_frame, text="hello")
        #but.pack()
        for option in dict_list:
            button = Button(self.view_frame, text=option.capitalize() )
            #button.grid(row=row, sticky="W", pady=10)
            button.pack()
            self.options.append(button)
            row+= 1
        
        #view_frame.grid(row=3)
        

class StatsPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.root = master
        user = "random".capitalize()
        Label(self, text="Stats").grid(row=1, sticky="W", pady=10)
        Label(self, text="Name: " + user).grid(row=1, sticky="W", pady=10)
        pass

class GameFrame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.root = master
        self.score = 0
        self.back_button = None
        self.camera_lbl = None
        self.canvas = None
        self.score_label = None
        self.gesture_label = Label()
        self.feedback_label = None
        self.thumb_label = None
        self.index_label = None
        self.middle_label = None
        self.ring_label = None
        self.pinky_label = None
        self.job = None
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 400)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode='store_true',
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
        )

        self.keypoint_classifier = KeyPointClassifier()
        with open('model/keypoint_classifier/keypoint_classifier_label.csv',
                  encoding='utf-8-sig') as f:
            keypoint_classifier_labels = csv.reader(f)
            self.keypoint_classifier_labels = [
                row[0] for row in keypoint_classifier_labels
            ]
        self.questions = self.keypoint_classifier_labels.copy()
        random.shuffle(self.questions)
        self.answer = ""
        self.predictions = []
        self.pred = None
        self.feedback = {}
        self.ret = None
        self.image = None
        self.input_hand = None
        self.results = None
        self.results2 = None
        self.finger_diff = None

        #self.select_question()
        self.create_page()
        self.select_question()

    def create_page(self):
        self.score = 0
        Label(self, text="Game").grid(row=0, column=1, pady=10)
        self.score_label = Label(self, text="Score: %d" % self.score)
        self.score_label.grid(row=0, column=0, sticky="w", pady=10)

        self.gesture_label = Label(self, text="Gesture:")
        self.gesture_label.grid(row=0, column=2, pady=10)

        feedback_col = 1
        #can probs removed self
        self.feedback_label = Label(self, text="Feedback:")
        self.feedback_label.grid(row=2, column=feedback_col, pady=10)

        self.thumb_label = Label(self, text="")
        self.thumb_label.grid(row=3, column=feedback_col, pady=10)

        self.index_label = Label(self, text="")
        self.index_label.grid(row=4, column=feedback_col, pady=10)

        self.middle_label = Label(self, text="")
        self.middle_label.grid(row=5, column=feedback_col, pady=10)

        self.ring_label = Label(self, text="")
        self.ring_label.grid(row=6, column=feedback_col, pady=10)

        self.pinky_label = Label(self, text="")
        self.pinky_label.grid(row=7, column=feedback_col, pady=10)

        self.temp()
        self.img = Image.fromarray(self.debug_image)
        self.photo = ImageTk.PhotoImage(self.img)
        
        self.canvas = Canvas(self, width=self.photo.width(), height=self.photo.height())
        self.canvas.grid(row=1, column=1, columnspan=2)
        self.canvas.create_image((0,0), image=self.photo, anchor='nw')

        #while True:
            #self.frame = self.cap.read()[1]
            #self.simg = cv2.resize(self.img, (0,0), fx=0.25, fy=0.25)
            #self.simg_cp = self.simg[:,:,::-1]
            
            #self.imgcon = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            #self.p = ImageTk.PhotoImage(Image.fromarray(self.imgcon))
            #self.camera_lbl['image'] = self.p
            
            #print('here')
            
            #self.root.update()
        
        self.update_feed()
        
        self.back_button = Button(self, text="Back",
                                 command=self.go_back)
        self.back_button.grid(row=8, column=2, sticky="E", pady=10)

    def select_question(self):
        if len(self.questions) != 0:
            self.answer = self.questions[0]
            self.questions.remove(self.answer)
            self.gesture_label['text'] = "Gesture: " + self.answer
        else:
            self.go_back()

    def temp(self):
        self.ret, self.image = self.cap.read()

        self.image = cv2.flip(self.image, 1)  # Mirror display
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.debug_image = copy.deepcopy(self.image)
        self.results = self.hands.process(self.image)

        if self.results.multi_hand_landmarks is not None:
            for hand_landmarks, handedness in zip(self.results.multi_hand_landmarks,
                                                  self.results.multi_handedness):

                # Landmark calculation
                landmark_list = app.calc_landmark_list(self.debug_image, hand_landmarks)
                imagec, fs, count = app.fingers(self.image, self.results, self.mp_hands)
                image_details = [imagec, fs, count]
                # Conversion to relative coordinates / normalized coordinates
                pre_processed_landmark_list = app.pre_process_landmark(
                    landmark_list)

                # Hand sign classification
                hand_sign_id = self.keypoint_classifier(pre_processed_landmark_list)
                hand_gesture = self.keypoint_classifier_labels[hand_sign_id]
                self.input_hand = handedness.classification[0].label[0:].lower()
                self.predictions.append(hand_gesture)

                if self.check_pred():
                    self.pred = app.count_pred(self.predictions)
                    if self.pred == self.answer:
                        self.update_score()
                    self.predictions = []
                    pic_image = cv2.imread('img/%s/%s.png' % (self.input_hand, self.answer.lower()), 0)
                    pic_image = cv2.cvtColor(pic_image, cv2.COLOR_BGR2RGB)
                    self.results2 = self.hands.process(pic_image)
                    #print(self.results2.multi_handedness)
                    if self.results2.multi_handedness is not None:
                        pic, fs2, count2 = app.fingers(pic_image, self.results2, self.mp_hands)
                        pic_details = [pic, fs2, count2]
                        self.finger_diff = app.compare_input(pic_details, image_details, self.input_hand)
                        self.update_feedback()
                    else:
                        pass
                        #finger_diff = compare_close(image_details[1])
                        self.finger_diff = {}

                #print(self.finger_diff)


                # Drawing part
                self.debug_image = app.draw_info_text(
                    self.debug_image,
                    handedness,
                    self.keypoint_classifier_labels[hand_sign_id]
                )
        return

    def update_feedback(self):
        #_Thumb: is open, it should be closed
        #_Index: is closed, it should be opened
        #_Middle:
        #_Ring:
        #_Pinky:
        if self.input_hand.lower() == "left":
            hand = "LEFT_"
        else:
            hand = "RIGHT_"
        finger_labels = {"THUMB": self.thumb_label,
                         "INDEX": self.index_label,
                         "MIDDLE": self.middle_label,
                         "RING": self.ring_label,
                         "PINKY": self.pinky_label}

        for i, (k, label) in enumerate(finger_labels.items()):
            finger = hand+k #RIGHT_THUMB
            label['text'] = finger + ": correct form"
            for j, (key, value) in enumerate(self.finger_diff.items()):
                if finger == key:
                    if value:
                        label['text'] = finger + ": Should be open"
                    else:
                        label['text'] = finger + ": Should be close"

            #finger_labels[finger]['text'] =

        #self.feedback
        return

    def update_feed(self):
        self.temp()
        self.img = Image.fromarray(self.debug_image)
        self.photo.paste(self.img)
        self.job = self.root.after(10, self.update_feed)

    def check_pred(self):
        thres = 20
        pred = None
        if len(self.predictions) > thres:
            return True
        else:
            return False

    def update_score(self):
        self.score += 1
        self.score_label["text"] = "Score: %d" % self.score
        self.select_question()


    def go_back(self):
        if self.job is not None:
            self.root.after_cancel(self.job)
            self.job = None
        self.cap.release()
        return

class ViewerFrame(Frame):
    def __init__(self, master, main, dict_list, option):
        Frame.__init__(self, master)
        self.root = master
        self.main = main
        self.option = option
        self.options = dict_list
        #self.canvas = Canvas(self, height=300, width=240,)
        #self.canvas.grid(row=1, column=1, columnspan=2)
        Label(self, text="Viewier").grid(row=0, column=1, pady=10)
        #Label(self, text="Score: %d" % score).grid(row=1, column=0, sticky="w", pady=10)
        
        self.imgs = ImageTk.PhotoImage(Image.open("img/"+self.option+".png").resize((300,240),Image.ANTIALIAS))
        #self.canvas.create_image(anchor="center", image=self.imgs)
        self.lbl = Label(self, image=self.imgs)
        self.lbl.grid(row=1, column=1, columnspan=2)
        
        self.back_btn = Button(self, text="<<", command=self.prev_img)
        self.exit_btn = Button(self, text="exit", command=self.go_back)
        self.forward_btn = Button(self, text=">>", command=self.next_img)
        
        self.back_btn.grid(row=2, column=0)
        self.exit_btn.grid(row=2, column=1)
        self.forward_btn.grid(row=2, column=2)
        
        self.back_button = Button(self, text="Back",
                                 command=self.go_back)
        self.back_button.grid(row=3, column=2)
        pass
    
    def go_back(self):
        self.root.current_frame.destroy()
        self.root.title("Dictionary")
        self.main.current_frame = Dictionary(self.root, self.main)
        self.main.current_frame.pack()
        return
    
    def next_img(self):
        self.lbl.destroy()
        x = len(self.options) - 1
        option_index = self.options.index(self.option)
        if x == option_index:
            self.option = self.options[0]
        else:
            self.option = self.options[option_index+1]
        self.imgs = ImageTk.PhotoImage(Image.open(
            "img/"+self.option+".png").resize((300,240),Image.ANTIALIAS))
        self.lbl = Label(self, image=self.imgs)
        self.lbl.grid(row=1, column=1, columnspan=2)
        
    def prev_img(self):
        self.lbl.destroy()
        x = len(self.options) - 1
        option_index = self.options.index(self.option)
        if 0 == option_index:
            self.option = self.options[x]
        else:
            self.option = self.options[option_index-1]
        self.imgs = ImageTk.PhotoImage(Image.open(
            "img/"+self.option+".png").resize((300,240),Image.ANTIALIAS))
        self.lbl = Label(self, image=self.imgs)
        self.lbl.grid(row=1, column=1, columnspan=2)
        

class VerticalScrolledFrame(Frame):
    def __init__(self, master, *args, **kw):
        Frame.__init__(self, master, *args, **kw)
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
        interior.bind('<Configure>', _configure_interior)
        
        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


    def get_frame(self):
        return self.scrollframe
    
def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo.screenheight()

def main():
    myapp = App()

if __name__ == "__main__":
    myapp = App()
    myapp.mainloop()
