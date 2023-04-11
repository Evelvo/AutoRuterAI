import tensorflow as tf
from tensorflow import keras

model = keras.models.load_model('model_tester.h5')

values = 260

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
    input()

    new_input = [4, 2, 6, 8, 0, 1, 0, 1, 4, 6, 9, 6, 6, 8, 8, 843, 734, 74, 9, 3]
    while len(new_input) < values:
        new_input.append(0)
    while len(new_input) > values:
        new_input.pop()
    new_input = tf.constant([new_input], dtype=tf.float32)
    print(new_input)

    prediction = model.predict(new_input)

    print(prediction)
    directions = ["top", "bottom", "right", "left"]
    direction = find_highest_number(prediction)
    print(directions[direction[1]])