import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import pyttsx3

import cv2
import numpy as np
from matplotlib import pyplot as plt

def upload_file():
    global img
    global filename
    f_types = [('Jpg Files', '*.jpg')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img = ImageTk.PhotoImage(file=filename)
    b2 =tk.Button(my_w,image=img) # using Button 
    b2.grid(row=4,column=2)

def speaktext(command):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', 10.0)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 25)
    engine.say(command)
    engine.runAndWait()


def backend():
    img = cv2.imread(filename)
    img=cv2.resize(img,(500,500))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(
        threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    i = 0
    for contour in contours:
        if i == 0:
            i = 1
            continue
        approx = cv2.approxPolyDP(
            contour, 0.01 * cv2.arcLength(contour, True), True)
        cv2.drawContours(img, [contour], 0, (0, 0, 255), 5)
        M = cv2.moments(contour)
        if M['m00'] != 0.0:
            x = int(M['m10']/M['m00'])
            y = int(M['m01']/M['m00'])
        if len(approx) == 3:
            cv2.putText(img, 'Triangle', (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            speaktext('It is a Triangle')
        elif len(approx) == 4:
            cv2.putText(img, 'Quadrilateral', (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            speaktext('It is a quadrilateral')
        elif len(approx) == 5:
            cv2.putText(img, 'Pentagon', (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            speaktext('It is Pentagon')
        elif len(approx) == 6:
            cv2.putText(img, 'Hexagon', (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            speaktext('It is Hexagon')
        else:
            cv2.putText(img, 'Circle', (x, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            speaktext('It is Circle')

    cv2.imshow('shapes', img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


my_w = tk.Tk()
my_w.geometry("800x1000")  # Size of the window
my_w.config(bg='green')
my_w.title('AI Shape Detection')
my_font1=('times', 18, 'bold')
l1 = tk.Label(my_w,text='Shapes Detection System',width=30,font=my_font1)  
l1.grid(row=1,column=2)
b1 = tk.Button(my_w, text='Upload File', 
   width=20,command = upload_file)
b1.grid(row=2,column=2) 
b2 = tk.Button(my_w, text='Detect Shape', 
   width=20,command = backend)
b2.grid(row=3,column=2) 

my_w.mainloop()  # Keep the window open

