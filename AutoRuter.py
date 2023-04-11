from tkinter import *
from time import sleep
import os
import random
import tensorflow as tf
from tensorflow import keras

model = keras.models.load_model('model_tester.h5')
value = 808

def find_highest_number(lst):
    highest_num = None
    direction = None
    for idx, sub_lst in enumerate(lst):
        for jdx, num in enumerate(sub_lst):
            if highest_num is None or num > highest_num:
                highest_num = num
                direction = [idx, jdx]
    return direction

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

x = 20
y = 14
x1 = 0

size = 1.3


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

number_identification = []


selected_points = []
select = False
selected_amount = 0
max_select = 2
selected_cords = ()
color_select = ""
route_number = 0
placeholder = False

#Nødvendige for algoritme
selected_cords_final = []
comp_used = []
line_points_id = []

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

def set_select():
    Select_btn.configure(background="#575757")
    global select
    select = True

def click_reset():
    global selected_points, selected_cords_final, comp_used, line_points_id, route_number, obstructed
    selected_points = []
    obstructed = []
    selected_cords_final = []
    comp_used = []
    line_points_id = []
    route_number = 0
    for i in btns:
        i.configure(text = "", bg = "white", bd = 0)

def set_placeholder():
    global placeholder
    if placeholder:
        placeholder = False
        placeholder_btn.configure(background="#242424")
    else:
        placeholder_btn.configure(background="#575757")
        placeholder = True


def get_cords(number):
    global selected_amount, select, selected_cords, selected_cords_final, color_select, route_number, comp_used, line_points_id, obstructed
    x = number_identification[number-1][0]
    y = number_identification[number-1][1]
    p_x = number_identification[number-1][2]
    p_y = number_identification[number-1][3]
    Cords_display.configure(text = (f"{number}, {x}, {y}"))
    if placeholder:
        btns[number-1].configure(bg="#292929")
        comp_append = x, y
        comp_used.append(comp_append)
        obstructed.append(x)
        obstructed.append(y)
    if select:
        if selected_amount == 0:
            color_select = str(hex_code_colors())
            route_number += 1
        selected_amount += 1
        selected_cords += number, x, y, color_select
        obstructed.append(x)
        obstructed.append(y)
        btns[number-1].configure(bg=color_select, bd = 2, text = route_number)
        btns[number-1].place(x = p_x-1, y = p_y-1)
        if selected_amount == max_select:
            selected_amount = 0
            select = False
            Select_btn.configure(background="#242424")
            selected_cords_final.append(selected_cords)
            selected_cords = ()

def route():
    global selected_cords_final, comp_used, number_identification, x, y, value, obstructed
    #for btn in btns:
    #    btn.configure(width=2, height = 1, bd = 0, bg = "white", text = "")
    for routes in selected_cords_final:
        idn = routes[0]
        xn = routes[1]
        yn = routes[2]
        idn1 = routes[4]
        xn1 = routes[5]
        yn1 = routes[6]
        color = routes[3]

        def add_point(point):
            for i in number_identification:
                if point == (i[0], i[1]):
                    line_point_append = i[0], i[1]
                    line_points_id.append(line_point_append)
                    obstructed.append(i[0])
                    obstructed.append(i[1])
                    btns[i[4]- 1].configure(bg = color)
                    btns[i[4]- 1].update()
        
        def check_taken(point):
            is_taken = 0
            for taken in comp_used:
                if point == taken:
                    is_taken = 1
            for taken in line_points_id:
                if point == taken:
                    is_taken = 1
            for taken in selected_cords_final:
                first_cords = taken[1], taken[2]
                second_cords = taken[5], taken[6]
                if point == first_cords:
                    is_taken = 1
                if point == second_cords:
                    is_taken = 1

            return is_taken

        
        while True:

            top = xn, yn-1
            bottom = xn, yn+1
            right = xn+1, yn
            left = xn-1, yn

            left_ob = 0
            right_ob = 0
            top_ob = 0
            bottom_ob = 0

            if yn-1 == 0:
                top_ob = 1
            if yn+1 >y:
                bottom_ob = 1
            if xn+1 > x:
                right_ob = 1
            if xn-1 == 0:
                left_ob = 1
                
            
            top_ob = check_taken(top)
            bottom_ob = check_taken(bottom)
            right_ob = check_taken(right)
            left_ob = check_taken(left)

            print(obstructed)

            new_input = [xn, yn, xn1, yn1, top_ob, bottom_ob, right_ob, left_ob]
            for obs in obstructed:
                new_input.append(obs)
            print(new_input)
            while len(new_input) < value:
                new_input.append(0)
            while len(new_input) > value:
                new_input.pop()
            new_input = tf.constant([new_input], dtype=tf.float32)
            print(new_input)

            prediction = model.predict(new_input)

            print(prediction)
            directions = ["top", "bottom", "right", "left"]
            direction = find_highest_number(prediction)
            dir = (directions[direction[1]])
            if dir == "top":
                yn-=1
                add_point(top)
            if dir == "bottom":
                yn+=1
                add_point(bottom)
            if dir == "right":
                xn +=1
                add_point(right)
            if dir == "left":
                xn -=1
                add_point(left)
            
                
            if (xn, yn) == (xn1, yn1):
                break
            if (xn, yn) == (xn1-1, yn1):
                break
            if (xn, yn) == (xn1+1, yn1):
                break
            if (xn, yn) == (xn1, yn1+1):
                break
            if (xn, yn) == (xn1, yn1-1):
                break
            



        

Select_btn = Button(root, 
                    text = "select", 
                    command = set_select, 
                    background="#242424", 
                    fg = "white", 
                    font= ("Arial", 30), 
                    bd = 0,
                    activebackground="#242424",
                    activeforeground="white")
Select_btn.place(x = 1090, y = 210)

placeholder_btn = Button(root, 
                        text = "Comp", 
                        command = set_placeholder, 
                        background="#242424", 
                        fg = "white", 
                        font= ("Arial", 30), 
                        bd = 0,
                        activebackground="#575757",
                        activeforeground="white")
placeholder_btn.place(x = 1090, y = 300)

Route_btn = Button(root, 
                        text = "Route", 
                        command = route, 
                        background="#242424", 
                        fg = "white", 
                        font= ("Arial", 30), 
                        bd = 0,
                        activebackground="#575757",
                        activeforeground="white")
Route_btn.place(x = 1090, y = 600)

Reset_btn = Button(root, 
                        text = "Reset", 
                        command = click_reset, 
                        background="#242424", 
                        fg = "white", 
                        font= ("Arial", 30), 
                        bd = 0,
                        activebackground="#575757",
                        activeforeground="white")
Reset_btn.place(x = 1090, y = 400)





for number in range(1, points_amount + 1):
    if x1 == x:
        x1 = 0
    x1 += 1
    btns.append(Button(root, bd = 0, activebackground = "#c2c2c2", command=lambda number=number: get_cords(number)))
    btns[number-1].place(x = placing_x, y = placing_y, width=point_size, height = point_size)
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



root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()