from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card={}
to_learn={}


#catch exception when there is no file existing first
try:
    data=pandas.read_csv("Data/chinese_words.csv")
except FileNotFoundError:
    original_data= pandas.read_csv("Data/chinese_words.csv")
    print(original_data)
    to_learn=original_data.to_dict(orient="records")
else:
    to_learn=data.to_dict(orient="records")


#Commands that will power the buttons and config to select chinese characters
def next_card():
    global current_card
    global flip_timer
    window.after_cancel(flip_timer)
    current_card= random.choice(to_learn) #random items from list to learn
    canvas.itemconfig(card_title, text="Character", fill= 'black', font=("Ariel", 20, "bold"))
    canvas.itemconfig(card_word, text=current_card["Character"], fill = "black", font=("Ariel", 40, "bold"))
    canvas.itemconfig(card_background, image=card_front_img)
    window.after(4000, func=flip_card)
    flip_timer = window.after(4000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text='Pinyin', fill= "white", font=("Ariel", 20, "bold"))
    canvas.itemconfig(card_word, text=current_card['Pinyin'], fill="white", font=("Ariel", 25, "bold"))
    canvas.itemconfig(card_background, image= card_back_img)

def is_known():
    to_learn.remove(current_card) #remove the words that are known and reduce overall list
    print(len(to_learn))
    data=pandas.DataFrame(to_learn)#new data frame
    data.to_csv("words_to_learn.csv", index=False)
    next_card()


#Create the window for the flash cards
window= Tk()
window.title("Basic Chinese Flashy")
window.config(padx=50, pady=50, bg = BACKGROUND_COLOR)
window.resizable(False,False) #Make window non-resizable, optimal view
flip_timer=window.after(4000, func=flip_card)


#Create the white canvas where we will build the text on. Positions are relative to Canvas size
canvas= Canvas(width=800, height=526)
card_front_img = PhotoImage(file="Images/card_front.png")
card_back_img=PhotoImage(file="Images/card_back.png")
card_background= canvas.create_image(400,263,image=card_front_img)
card_title = canvas.create_text(400,150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400,263, text="word", font=("Ariel", 50, "bold"), width = 2000)
canvas.config(bg= BACKGROUND_COLOR, highlightthickness= 0)
canvas.grid(row=0, column=0, columnspan=2)


#Images for the buttons with commands
cross_image = PhotoImage(file="Images/wrong.png")
unknown_button = Button(image=cross_image,highlightthickness= 0, command=next_card) #highlightthickness gets rid of image border
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="Images/right.png")
known_button = Button(image=check_image, highlightthickness= 0, command=is_known)
known_button.grid(row=1, column =1)


next_card() #call the function

window.mainloop()




