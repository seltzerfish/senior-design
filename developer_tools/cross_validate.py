# -*- coding: utf-8 -*-
# import matplotlib.pyplot as plt
import warnings
import numpy as np
from sklearn.linear_model import LinearRegression
from tabulate import tabulate
from helpers import *
from itertools import chain
warnings.filterwarnings(action="ignore", module="scipy",
                        message="^internal gelsd")  # ignore this

NUM_PARTITIONS = 10

# initialize variables
print("reading data...")
labels, data = load_data("data/real_data.txt")


np.random.shuffle(data)  # shuffle the data
CHUNK_SIZE = len(data) // NUM_PARTITIONS
table = []
for i in range(NUM_PARTITIONS):
    print("Iteration {}/{}".format(i + 1, NUM_PARTITIONS))
    l_v_bound = i * CHUNK_SIZE
    r_v_bound = min(i * CHUNK_SIZE + CHUNK_SIZE, len(data))

    validation = data[l_v_bound:r_v_bound]  # validation set
    train = np.concatenate(
        [data[:l_v_bound], data[r_v_bound:len(data)]])  # training set

    x_train = []
    y_train = []
    for entry in train:
        x_train.append(extract_features(entry[0])[1])
        y_train.append(np.array([float(e) for e in entry[2:]]))
    reg_model = LinearRegression()
    reg_model.fit(x_train, y_train)

    x_val = []
    y_val = []
    for entry in validation:
        x_val.append(extract_features(entry[0])[1])
        y_val.append(np.array([float(e) for e in entry[2:]]))
    pred = reg_model.predict(x_val)
    table.append(calculate_error(pred, np.array(y_val)))
with open("linear_cross.csv", "w") as f:
    new_table = np.array(table)
    f.write(",".join(labels[2:]) + "\n")
    avg = np.mean(new_table, axis=0)
    std = np.std(new_table, axis=0)
    f.write(",".join([str(q) for q in avg]) + "\n")
    f.write(",".join([str(q) for q in std]) + "\n")


# plt.bar(labels[2:], avg, label="difference")
# plt.title("Predicted vs actual Difference")
# plt.xticks(rotation='vertical')
# plt.gcf().subplots_adjust(bottom=0.32)
# plt.legend()
# plt.show()
