import tensorflow as tf
from tensorflow import keras

model = keras.models.load_model('model.h5')

def find_highest_number(lst):
    highest_num = None
    direction = None
    for idx, sub_lst in enumerate(lst):
        for jdx, num in enumerate(sub_lst):
            if highest_num is None or num > highest_num:
                highest_num = num
                direction = [idx, jdx]
    return direction


while True:

    x = input("x: ")
    y = input("y: ")
    x_to = input("x_to: ")
    y_to = input("y_to: ")
    top = input("top: ")
    bottom = input("bottom: ")
    right = input("right: ")
    left =  input("left: ")

    new_input = [int(x), 
                 int(y), 
                 int(x_to), 
                 int(y_to), 
                 int(top), 
                 int(bottom), 
                 int(right), 
                 int(left)
    ]
    new_input = tf.constant([new_input], dtype=tf.float32)
    print(new_input)

    prediction = model.predict(new_input)

    print(prediction)
    directions = ["top", "bottom", "right", "left"]
    direction = find_highest_number(prediction)
    print(directions[direction[1]])