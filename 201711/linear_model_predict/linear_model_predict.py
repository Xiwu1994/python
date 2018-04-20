import numpy as np
from sklearn import linear_model
import matplotlib.pyplot as plt

def predict():
    with open('/Users/liebaomac/Desktop/My_Git/python/201711/linear_model_predict/test.txt', 'r') as f:
        data_x = []
        data_y = []
        time = []
        yesday = []
        for line in f.readlines():
            line = map(int, line.strip().split('\t'))
            time.append(line[0])
            yesday.append(line[1])
            data_x.append([line[0], line[1]])
            if len(line) > 2:
                data_y.append(line[2])

        train_len = len(data_y)
        test_len = len(data_x) - len(data_y)

        reg = linear_model.LinearRegression()
        reg.fit(data_x[:train_len], data_y)
        outcome = reg.predict(data_x[train_len:])
        print outcome

        plt.scatter(time[:train_len], data_y, color='blue')
        plt.plot(time, reg.predict(data_x), color='red', linewidth=4)
        plt.plot(time, yesday, color='green', linewidth=4)
        plt.xticks(range(25))
        plt.yticks(range(0, 11000000, 1000000))
        plt.show()
        f.close()


predict()