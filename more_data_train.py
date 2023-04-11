import tensorflow as tf
import json
import numpy as np

with open('train_data.json', 'r') as f:
    dataset = json.load(f)


inputs = []
labels = []
obstructed_list = []

for data in dataset:
    input_data = []
    for key in data.keys():
        if key != 'outcome':
            if key != "obstructed":
                value = data[key]
                input_data.append(value)
        if key == "obstructed":
            obstructed_list.append(data[key])
            for obs in data[key]:
                input_data.append(obs)
    print(input_data)
    inputs.append(input_data)
    if data['outcome'] == 'top':
        label = [1, 0, 0, 0]
    elif data["outcome"] == "bottom":
        label = [0, 1, 0, 0]
    elif data["outcome"] == "right":
        label = [0, 0, 1, 0]
    elif data["outcome"] == "left":
        label = [0, 0, 0, 1]
    labels.append(label)

print(obstructed_list)

max_length = max(len(sublist) for sublist in inputs)
padded_data = np.array([sublist + [0]*(max_length-len(sublist)) for sublist in inputs])

print(inputs)
print(padded_data)

inputs = tf.constant(padded_data, dtype=tf.float32)
labels = tf.constant(labels, dtype=tf.float32)

print(inputs)
print(labels)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(16, activation='relu', input_shape=[len(inputs[0])]),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(4, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(inputs, labels, epochs=1000, batch_size=32)

model.save("model_tester.h5")

print("")
print("")
print(f"Values: {max_length}")
print("")
print("")

