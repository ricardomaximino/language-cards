from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
TITLE_FONT = ("Ariel", 40, "italic")
WORD_FONT = ("Ariel", 60, "bold")

data = None
current_card = {}
options = ["English", "Spanish", "Portuguese"]


def load_data():
    global data
    try:
        data = pandas.read_csv("resources/data/words_to_learn.csv")
    except FileNotFoundError:
        data = pandas.read_csv("resources/data/words.csv")
    finally:
        data = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(data)
    canvas.itemconfig(canvas_image, image=front_card_image)
    canvas.itemconfig(title_text, text=language_from.get(), fill="black")
    canvas.itemconfig(word_text, text=current_card[language_from.get()], fill="black")
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(canvas_image, image=back_card_image)
    canvas.itemconfig(title_text, text=language_to.get(), fill="white")
    canvas.itemconfig(word_text, text=current_card[language_to.get()], fill="white")


def save_words_to_learn():
    global data, current_card
    data.remove(current_card)
    words_to_learn = pandas.DataFrame(data)
    words_to_learn.to_csv("resources/data/words_to_learn.csv", index=False)


def right_answer():
    save_words_to_learn()
    next_card()


def wrong_answer():
    next_card()


window = Tk()
window.title("Languages Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

front_card_image = PhotoImage(file="resources/images/card_front.png")
back_card_image = PhotoImage(file="resources/images/card_back.png")
canvas = Canvas(width=810, height=556, highlightthickness=0, bg=BACKGROUND_COLOR)
canvas_image = canvas.create_image(405, 275, image=front_card_image)
canvas.grid(row=2, column=0, columnspan=2)
title_text = canvas.create_text(400, 150, text="Title", font=TITLE_FONT)
word_text = canvas.create_text(400, 263, text="Word", font=WORD_FONT)

right_image = PhotoImage(file="resources/images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=right_answer)
right_button.grid(row=3, column=0)

wrong_image = PhotoImage(file="resources/images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, command=wrong_answer)
wrong_button.grid(row=3, column=1)

language_from = StringVar()
language_from.set(options[0])
drop_from = OptionMenu(window, language_from, *options)
drop_from.config(bg=BACKGROUND_COLOR, highlightthickness=0)
drop_from["menu"].config(bg=BACKGROUND_COLOR)
drop_from.grid(row=1, column=0)

language_to = StringVar()
language_to.set(options[1])
drop_to = OptionMenu(window, language_to, *options)
drop_to.config(bg=BACKGROUND_COLOR, highlightthickness=0)
drop_to["menu"].config(bg=BACKGROUND_COLOR)
drop_to.grid(row=1, column=1)

load_data()
next_card()

window.mainloop()
