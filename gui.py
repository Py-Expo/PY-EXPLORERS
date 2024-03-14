import sys
import os
from tkinter import *

window = Tk()

window.title("Gesture Based Navigation System")
window.geometry('550x200')

def brightness():
    os.system('python screenbrightness.py')
    
def scroll():
    os.system('python scrolling.py')
    
def volume():
    os.system('python volumecontrol.py')
    
def basic_cursor():
    os.system('python gestnav.py')
    
def player():
    os.system('python mediaplayer.py')

def exit_application():
    window.destroy()

btn_brightness = Button(window, text="BRIGHTNESS", bg="black", fg="white", command=brightness)
btn_brightness.grid(column=0, row=0)

btn_scroll = Button(window, text="SCROLL", bg="black", fg="white", command=scroll)
btn_scroll.grid(column=2, row=2)

btn_volume = Button(window, text="VOLUME", bg="black", fg="white", command=volume)
btn_volume.grid(column=4, row=4)

btn_cursor = Button(window, text="CURSOR", bg="black", fg="white", command=basic_cursor)
btn_cursor.grid(column=6, row=6)

btn_player = Button(window, text="PLAYER", bg="black", fg="white", command=player)
btn_player.grid(column=8, row=8)

btn_exit = Button(window, text="EXIT", bg="red", fg="white", command=exit_application)
btn_exit.grid(column=10, row=10)

window.mainloop()
