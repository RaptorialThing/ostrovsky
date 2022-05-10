# -*- coding: cp1251 -*-

import matplotlib.pyplot as plt
import csv

with open('data_out.csv','r') as csvfile:
    data_reader = csv.reader(csvfile, delimiter = ';')
 
    start = 1
    end = start+2

    all_pos = []
    for row in data_reader:
        nxt = True
        for pos in row[1:]:
            if nxt:
                all_pos.append(pos)
                nxt = False
            else:
                nxt = True
        break

    for i in all_pos:
        amounts = []
        percents = []
        dates = []
        skipFirst = True
        for row in data_reader:
            if skipFirst:
                skipFirst = False 
                continue
            date = row[0]
            amount_button = True
            for pos in row[start:end]:
                if amount_button:
                    amounts.append(float(pos))
                    amount_button = False 
                    dates.append(date)
                else:
                    percents.append(pos)
                    amount_button = True
        csvfile.seek(0)
        start = end
        end = start + 2
        plt.plot(dates,amounts,label="Pos # "+str(i))

plt.xticks(rotation=270)

#plt.legend()
plt.show()
