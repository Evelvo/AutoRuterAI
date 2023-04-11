from tkinter import *
from time import sleep
import os
import random
import keyboard
import json

root = Tk()
root.title("AutoRuter")
root.resizable(False, False)
root.configure(bg="#242424")

window_width = 1400
window_height = 800

def on_closing():
    os._exit(0)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

x = 10
y = 10
x1 = 0

xn = None
yn = None

size = 1.8


placing_x_reset = 100
placing_x = placing_x_reset
placing_y_reset = 60
placing_y = placing_y_reset
margin = 30 * size
margin_y = 30 * size
point_size = 23 * size
points_amount = x * y
line_number = 1
btns = []
color = None

number_identification = []

first_cords = None
second_cords = None

top = None
bottom = None
right = None
left = None

json_list = []

obstructed = []




Cords_display = Label(root, 
                      text = "0, 0, 0", 
                      font= ("Arial", 30), 
                      background="#242424", 
                      fg = "white")
Cords_display.place(x = 1070, y = 60)

def hex_code_colors():
    a = hex(random.randrange(0,256))
    b = hex(random.randrange(0,256))
    c = hex(random.randrange(0,256))
    a = a[2:]
    b = b[2:]
    c = c[2:]
    if len(a)<2:
        a = "0" + a
    if len(b)<2:
        b = "0" + b
    if len(c)<2:
        c = "0" + c
    z = a + b + c
    return "#" + z.upper()




def add_point(point):
    for i in number_identification:
        if point == (i[0], i[1]):
            added_points_append = i[0], i[1]
            obstructed.append(added_points_append)
            btns[i[4]- 1].configure(bg = color)

def check_finish(point):
    checker = False
    x2 = second_cords[0]
    y2 = second_cords[1]
    top1 = x2, y2-1
    bottom1 = x2, y2+1
    right1 = x2+1, y2
    left1 = x2-1, y2
    if point == second_cords:
        checker = True
    if point == top1:
        checker = True
    if point == bottom1:
        checker = True
    if point == right1:
        checker = True
    if point == left1:
        checker = True
    
    return checker


def random_select():
    global first_cords, second_cords, xn, yn, top, bottom, right, left, color
    color = hex_code_colors()
    while True:
        first = random.choice(number_identification)
        print(first)
        second = random.choice(number_identification)
        print(second)
        first_cords = first[0], first[1]
        second_cords = second[0], second[1]
        videre = True
        for obs in obstructed:
            if obs == first_cords:
                videre = False
            if obs == second_cords:
                videre = False
        if videre:
            break
    xn = first[0]
    yn = first[1]

    top = xn, yn-1
    bottom = xn, yn+1
    right = xn+1, yn
    left = xn-1, yn

    obstructed.append(first_cords)
    obstructed.append(second_cords)

    btns[first[4] -1].configure(bg=color, text = "1", font = ("Arial", 13))
    btns[second[4]- 1].configure(bg=color, text = "2", font = ("Arial", 13))
    print(first)
    print(second)

def finished():
    print("done")
    random_select()

def write_click():
    with open("test.json", "w") as json_file:
        json.dump(json_list, json_file)
    
def reset_click():
    global obstructed, btns
    obstructed = []
    for i in btns:
        i.configure(text = "", bg = "white", bd = 0)
    random_select()

def train_gather(x, y, direction):
    global second_cords, obstructed, json_list
    #Legge til hvor stor planen er for eksempel 20 * 14
    print(f"Kanskje seinere trene med? {obstructed}")
    top = x, y-1
    bottom = x, y+1
    right = x+1, y
    left = x-1, y
    top_ob = 0
    bottom_ob = 0
    right_ob = 0
    left_ob = 0
    for obs in obstructed:
        if top == obs:
            top_ob = 1
        if bottom == obs:
            bottom_ob = 1
        if right == obs:
            right_ob = 1
        if left == obs:
            left_ob = 1

    
    data = [x, y, second_cords[0], second_cords[1],top_ob, bottom_ob, right_ob, left_ob, direction]
    print(data)

    print(obstructed)
    obs_append = []
    for obsed in obstructed:
        obs_append.append(obsed[0])
        obs_append.append(obsed[1])
    print(obs_append)

    json_data = {
        "x": x,
        "y": y,
        "x_to": second_cords[0],
        "y_to": second_cords[1],
        "top": top_ob,
        "bottom": bottom_ob,
        "right": right_ob,
        "left": left_ob,
        "obstructed": obs_append,
        "outcome": direction
    }

    json_list.append(json_data)


def get_cords(number):
    x = number_identification[number-1][0]
    y = number_identification[number-1][1]
    Cords_display.configure(text = (f"{number}, {x}, {y}"))

def right_click():
    print("right")
    global xn, right, yn
    train_gather(xn, yn, "right")
    xn += 1
    right = xn, yn
    add_point(right)
    print(check_finish(right))
    if check_finish(right):
        finished()

def left_click():
    print("left")
    global xn, left, yn
    train_gather(xn, yn, "left")
    xn -= 1
    left = xn, yn
    add_point(left)
    if check_finish(left):
        finished()

def top_click():
    print("top")
    global xn, top, yn
    train_gather(xn, yn, "top")
    yn -= 1
    top = xn, yn
    add_point(top)
    if check_finish(top):
        finished()

def bottom_click():
    print("bottom")
    global xn, bottom, yn
    train_gather(xn, yn, "bottom")
    yn += 1
    bottom = xn, yn
    add_point(bottom)
    if check_finish(bottom):
        finished()


keyboard.add_hotkey('up', top_click)
keyboard.add_hotkey('down', bottom_click)
keyboard.add_hotkey('right', right_click)
keyboard.add_hotkey('left', left_click)


for number in range(1, points_amount + 1):
    if x1 == x:
        x1 = 0
    x1 += 1
    btns.append(Button(root, bd = 0, activebackground = "#c2c2c2", command=lambda number=number: get_cords(number)))
    btns[number-1].place(x = placing_x, y = placing_y, width = point_size, height = point_size)
    joint = x1, line_number, placing_x, placing_y, number
    number_identification.append(joint)
    placing_x += margin
    if number == x * line_number:
        placing_x = placing_x_reset
        placing_y += margin_y
        line_number += 1

label_y_placing_y = placing_y_reset

for label_y in range(1, y + 1):
    Label(root, text = label_y, background="#242424", fg = "white", width = 2, height = 1).place(x = placing_x_reset - 40, y = label_y_placing_y)
    label_y_placing_y += margin_y

label_x_placing_x = placing_x_reset

for label_x in range(1, x + 1):
    Label(root, text = label_x, background="#242424", fg = "white", width = 2, height = 1).place(x = label_x_placing_x, y = placing_y_reset - 40)
    label_x_placing_x += margin


right_btn = Button(root,
                    command = right_click, 
                    background="#242424", 
                    fg = "white", 
                    font= ("Arial", 30), 
                    bd = 2,
                    activebackground="#424242",
                    activeforeground="white")
right_btn.place(x = 1250, y = 300, width = 50, height = 50)


left_btn = Button(root,
                    command = left_click, 
                    background="#242424", 
                    fg = "white", 
                    font= ("Arial", 30), 
                    bd = 2,
                    activebackground="#424242",
                    activeforeground="white")
left_btn.place(x = 1100, y = 300, width = 50, height = 50)

top_btn = Button(root,
                    command = top_click, 
                    background="#242424", 
                    fg = "white", 
                    font= ("Arial", 30), 
                    bd = 2,
                    activebackground="#424242",
                    activeforeground="white")
top_btn.place(x = 1175, y = 225, width = 50, height = 50)

bottom_btn = Button(root,
                    command = bottom_click, 
                    background="#242424", 
                    fg = "white", 
                    font= ("Arial", 30), 
                    bd = 2,
                    activebackground="#424242",
                    activeforeground="white")
bottom_btn.place(x = 1175, y = 375, width = 50, height = 50)

write_btn = Button(root,
                    command = write_click, 
                    text = "Write",
                    background="#242424", 
                    fg = "white", 
                    font= ("Arial", 30), 
                    bd = 2,
                    activebackground="#424242",
                    activeforeground="white")
write_btn.place(x = 1100, y = 475)

reset_btn = Button(root,
                    command = reset_click, 
                    text = "Reset",
                    background="#242424", 
                    fg = "white", 
                    font= ("Arial", 30), 
                    bd = 2,
                    activebackground="#424242",
                    activeforeground="white")
reset_btn.place(x = 1100, y = 575)

random_select()



root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()