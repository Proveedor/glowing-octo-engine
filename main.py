from Tkinter import *
import threading
import time
##import Tkinter as tk

ui_locale = '' # e.g. 'fr_FR' fro French, '' as default
large_text_size = 168
time_format = 24 # 12 or 24
date_format = "%b %d, %Y" # check python doc for strftime() for options
medium_text_size = 28
small_text_size = 18
LOCALE_LOCK = threading.Lock()

def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

class Application:
    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.topFrame = Frame(self.tk, background='black')
        self.topFrame.pack(side=TOP, fill=BOTH, expand=YES)
        self.clock = Clock(self.topFrame)
        self.clock.pack(anchor=N, padx=100, pady=60)

        #self.tk.attributes("-fullscreen",True)
        #self.quitButton = Button(self.tk, text='Quit', command=self.tk.quit)
        #self.quitButton.grid()
        #x = blah(self.tk, "Window 1", 20,  10)
        #y = blah(self.tk, "Window 2", 230, 10)
        #y = blah(self.tk, "Window 3", 440, 10)

    def createWidgets(self):
        self.quitButton = self.tk.Button(self, text='Quit', command=self.quit)
        self.quitButton.grid()

    def mainloop(self):
        self.tk.mainloop()

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"


class Clock(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg='black')
        # initialize time label
        self.time1 = ''
        self.timeLbl = Label(self, font=('Helvetica', large_text_size), fg="white", bg="black")
        self.timeLbl.pack(side=TOP, anchor=E)
        # initialize day of week
        self.day_of_week1 = ''
        self.dayOWLbl = Label(self, text=self.day_of_week1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dayOWLbl.pack(side=TOP, anchor=E)
        # initialize date label
        self.date1 = ''
        self.dateLbl = Label(self, text=self.date1, font=('Helvetica', small_text_size), fg="white", bg="black")
        self.dateLbl.pack(side=TOP, anchor=E)
        self.tick()

    def tick(self):
        ##with setlocale(ui_locale):
        if time_format == 12:
            time2 = time.strftime('%I:%M %p') #hour in 12h format
        else:
            time2 = time.strftime('%H:%M') #hour in 24h format
        day_of_week2 = time.strftime('%A')
        date2 = time.strftime(date_format)
        # if time string has changed, update it
        if time2 != self.time1:
            self.time1 = time2
            self.timeLbl.config(text=time2)
        if day_of_week2 != self.day_of_week1:
            self.day_of_week1 = day_of_week2
            self.dayOWLbl.config(text=day_of_week2)
        if date2 != self.date1:
            self.date1 = date2
            self.dateLbl.config(text=date2)
        # calls itself every 200 milliseconds
        # to update the time display as needed
        # could use >200 ms, but display gets jerky
        self.timeLbl.after(200, self.tick)


class blah:
    all = []
    event_start_x = None
    event_start_y = None
    def __init__(self, root, title, x, y):
        self.root = root
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.x = x
        self.y = y
        self.move_lastx = self.x
        self.move_lasty = self.y
        self.f = Frame(self.root, bd=1, relief=RAISED)
        #self.f = Label(self.root, bd=1, bg="#08246b", fg="white", text=title)
        self.f.place(x=x, y=y, width=200, height=200)

        #self.l = Label(self.f, bd=1, bg="#08246b", fg="white",text=title)
        #self.l.pack(fill=X)

        self.f.bind('<Button-1>', self.MoveWindowStart)
        #self.f.bind('<1>', self.focus)
        self.f.bind('<B1-Motion>', self.MoveWindow)
        self.all.append(self)
        #self.focus()

    def clamp(self, lo, hi, x):
        return min(max(x, lo), hi)

    def MoveWindowStart(self, event):
        self.move_lastx = event.x_root
        self.move_lasty = event.y_root
        self.event_start_x = event.x - self.x
        self.event_start_y = event.y - self.y
        self.focus()

    def MoveWindow(self, event):
        self.root.update_idletasks()
        dx = event.x_root - self.move_lastx
        dy = event.y_root - self.move_lasty
        self.move_lastx = event.x_root
        self.move_lasty = event.y_root

        self.x = self.clamp(0, self.root.winfo_width()-200, self.x + self.event_start_x + dx ) # should depend on
        self.y = self.clamp(0, self.root.winfo_height()-200, self.y + self.event_start_y + dy) # actual size here
        self.f.place_configure(x=self.x, y=self.y )

    def focus(self, event=None):
        self.f.tkraise()

if __name__ == '__main__':
    app = Application()
    app.mainloop()



