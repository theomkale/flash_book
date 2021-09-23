from tkinter import *
import pandas as pd
import random
import threading

# Constants
BACKGROUND_COLOR = "#B1DDC6"


def init():
    global words
    try:
        if len(words) != 0:
            words = pd.read_csv('data/remaining_words.csv')
    except FileNotFoundError:
        words = pd.read_csv('data/french_words.csv')
    else:
        words = pd.read_csv('data/french_words.csv')
        words = words.to_dict(orient='records')


words = ''
word = ''
timer = ''


# Functions
def get_word():
    global timer
    global word
    if timer != '':
        window.after_cancel(timer)
    word = random.choice(words)
    canvas.itemconfig(image_canvas, image=card_front)
    canvas.create_line(50, 30, 50, 480, width=10, fill=BACKGROUND_COLOR)
    english_label['text'] = "French"
    french_label['text'] = word['French']
    timer = window.after(3000, func=flip_card)


def remove_word():
    if len(words) == 0:
        raise IndexError
    try:
        words.remove(word)
    except IndexError:
        init()

    remaining_words = pd.DataFrame(words)
    remaining_words.to_csv('data/remaining_words.csv')
    get_word()


def flip_card():
    canvas.itemconfig(image_canvas, image=card_back)
    english_label['text'] = "English"
    english_label.config(bg=BACKGROUND_COLOR, fg="white")
    french_label['text'] = word["English"]
    french_label.config(bg=BACKGROUND_COLOR, fg="white")
    canvas.create_line(50, 30, 50, 480, width=10, fill="white")


# UI
window = Tk()
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
window.title("Flashy")
window.resizable(False, False)

canvas = Canvas(height=526, width=800, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

card_front = PhotoImage(file='images/card_front.png')
card_back = PhotoImage(file='images/card_back.png')

image_canvas = canvas.create_image(400, 265, image=card_front)
english_label = Label(text="French", font=("Ariel", 40, "italic"))
english_label.place(x=80, y=150)

french_label = Label(text="trove", font=("Ariel", 70, "bold"))
french_label.place(x=80, y=263)

wrong_button_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_button_image, highlightthickness=0, command=get_word)
wrong_button.grid(row=1, column=0)

right_button_image = PhotoImage(file="images/right.png", )
right_button = Button(image=right_button_image, highlightthickness=0, command=remove_word)
right_button.grid(row=1, column=1)
init()
get_word()

window.mainloop()
