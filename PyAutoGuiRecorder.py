import time
import tkinter as tk
import tkinter.filedialog
import pyautogui
from pynput import mouse
from optparse import OptionParser

class Stopwatch():
    def __init__(self):
        self.starttime = time.time()
    def elapsed(self,reset=False):
        t = time.time() - self.starttime
        if reset:
            self.reset()
        return t
    def reset(self):
        self.starttime = time.time()

clock = Stopwatch()

def on_click(x, y, button, pressed):
    if not stopRecording:
        if pressed:
            if button.name == "left":
                listbox.insert(tk.END, "pyautogui.click(x=%d, y=%d)" % (x,y))
            else:    
                listbox.insert(tk.END, "pyautogui.click(x=%d, y=%d, button='right')" % (x,y))
            listbox.insert(tk.END, "time.sleep(%f)" % clock.elapsed(True))    

listener = mouse.Listener(on_click=on_click)
listener.start() 

def recording():
    listbox.insert(tk.END, "pyautogui.moveTo(%d, %d)" % pyautogui.position())
    if options.Delay:
        listbox.insert(tk.END, "time.sleep(%f)" % options.Delay)
    else:    
        listbox.insert(tk.END, "time.sleep(%f)" % clock.elapsed(True))
    if not stopRecording:
        root.after(delay*1000, recording)

def click_r():
    global stopRecording
    button_r["relief"] = tk.SUNKEN
    button_p["state"] = "disabled"
    stopRecording = False
    if not options.Delay:
        clock.reset()
    if options.recordMoves:
        root.after(delay, recording)   
def click_p():
    button_p["relief"] = tk.SUNKEN
    button_r["state"] = "disabled"
    i = 0
    while True:
        entry = listbox.get(i)
        if entry:
            if i > 1:
                eval(entry)
            i += 1
        else:
            break    
    button_p["relief"] = tk.RAISED
    button_r["state"] = "normal"        
def click_s():
    global stopRecording
    stopRecording = True
    button_r["state"] = "normal"
    button_p["state"] = "normal"
    button_r["relief"] = tk.RAISED
    button_p["relief"] = tk.RAISED
def click_d():
    name = tkinter.filedialog.asksaveasfilename()    
    if name:
        f = open(name,"w")
        i = 0
        while True:
            entry = listbox.get(i)
            if entry:
                f.write(entry+"\n")
                i += 1
            else:
                break    
        f.close()

usage = '''
python3 PyAutoGuiRecorder.oy OPTIONS
'''
parser = OptionParser(usage)        
parser.add_option("--delay", dest="Delay", default=0.0, type="float",
    help="Replay delay in seconds")
parser.add_option("--recordMoves", dest="recordMoves", action="store_true",
    help="Capture simply mouse moves")    
options, args = parser.parse_args()

root = tk.Tk()
title = "PyAutoGuiRecorder Version 1.0"
root.title(title)
delay = 1
stopRecording = True
# Create listbox
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)
frame2 = tk.Frame(frame)
frame2.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

items = []
list_items = tk.Variable(value=items)
listbox = tk.Listbox(
    frame2, listvariable=list_items
)
listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar_v = tk.Scrollbar(frame2, orient="vertical")
scrollbar_v.config(command=listbox.yview)
scrollbar_v.pack(side=tk.RIGHT, fill=tk.BOTH)
listbox.config(yscrollcommand=scrollbar_v.set)
scrollbar_h = tk.Scrollbar(frame, orient="horizontal")
scrollbar_h.config(command=listbox.xview)
scrollbar_h.pack(side=tk.BOTTOM, fill=tk.BOTH)
listbox.config(xscrollcommand=scrollbar_h.set)
listbox.insert(tk.END, "import pyautogui")
listbox.insert(tk.END, "import time")

# Create buttons
icon1 = tk.PhotoImage(file="./images/Record.png")
button_r = tk.Button(root, text="Record", command=click_r, image=icon1)
button_r.pack(side=tk.LEFT)
icon2 = tk.PhotoImage(file="./images/Play.png")
button_p = tk.Button(root, text="Play", command=click_p, image=icon2)
button_p.pack(side=tk.LEFT)
icon3 = tk.PhotoImage(file="./images/Stop.png")
button_s = tk.Button(root, text="Stop", command=click_s, image=icon3)
button_s.pack(side=tk.LEFT)
icon4 = tk.PhotoImage(file="./images/Download.png")
button_d = tk.Button(root, text="Download", command=click_d, image=icon4)
button_d.pack(side=tk.LEFT)
root.mainloop()
