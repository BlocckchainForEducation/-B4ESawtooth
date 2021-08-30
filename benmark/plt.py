import matplotlib.pyplot as plt
import numpy as np


num = []
cert = []
subs = []
with open("./data.csv") as file:
    lines = file.readlines()
    for line in lines:
        arr = line.split(",")
        num.append(int(arr[0]))
        cert.append(float(arr[1]))
        subs.append(float(arr[2]))


x1 = num
y1 = cert
# plotting the line 1 points
plt.plot(x1, y1, label = "Certificate")
# line 2 points
x2 = num
y2 = subs
# plotting the line 2 points
plt.plot(x2, y2, label = "Grade")
plt.xlabel('Number of concurrent transaction')
# Set the y axis label of the current axis.ằng
plt.ylabel('Execute time (s)')
# Set a title of the current axes.
plt.title('Measure execute time of transactions')
# show a legend on the plot
plt.legend()
# Display a figure.
plt.savefig("transaction-execute-time-tight.pdf", bbox_inches='tight')
plt.show()


