# -*- coding: cp1251 -*-

import csv
import time

def extract(row,dates,all_pos):
    pos = str(row[1])
    amount = float(row[2])
    dt = time.strptime(row[3],"%Y-%m-%d %H:%M:%S")

    dt_key = time.strftime("%d.%m.%Y",dt)
    sum = 0

    if not dt_key in dates:
        dates[dt_key] = {}

    for p in all_pos:
        if not p in dates[dt_key]:
            dates[dt_key][p] = [0,0]
        if p == pos:
            dates[dt_key][pos][0] += amount
            dates[dt_key][pos][0] = toFixed(dates[dt_key][pos][0],2)
        sum += float(dates[dt_key][p][0])

    for p in all_pos:
        dates[dt_key][p][1] = percent(dates[dt_key][p][0],sum)

    return dates
    
def percent(amount, sum):
    if amount == 0:
        return 0
    return toFixed(((amount * 100) / sum),2)
    
def toFixed(num,digits):
    return float(f"{num:.{digits}f}")


def main():
    dates = {}

    with open('data.csv',newline='') as file:
        filereader = csv.reader(file,delimiter=';')
        nextRow = True
        all_pos = set()
        for row in filereader:
            if nextRow:
                nextRow = False
                continue 
            all_pos.add(str(row[1]))
            dates = extract (row,dates,all_pos)

    with open('data_out.csv','w',newline='') as file:
        filewriter = csv.writer(file,delimiter=';',escapechar=' ',quoting = csv.QUOTE_NONE)
        sorted_dates = []
        for d in dates:
            date = time.strptime(d,"%d.%m.%Y")
            sorted_dates.append(date)
        sorted_dates.sort()

        
        doublePos = sorted(all_pos)
        rowDoublePos = []
        for pos in doublePos:
            rowDoublePos.append(pos)
            rowDoublePos.append(pos)
        filewriter.writerow(["Date/Pos"]+rowDoublePos)
        for dt in sorted_dates:
            dt_prep = time.strftime("%d.%m.%Y",dt)
            values = []
            sorted_pos = sorted(dates[dt_prep])
            sorted_pos = sorted(set(sorted_pos + sorted(all_pos)))
            for pos in sorted_pos:
                if not pos in dates[dt_prep]:
                    values.append(str(0))
                    values.append(str(0)+"%")
                else:
                    values.append(str(dates[dt_prep][pos][0]))
                    values.append(str(dates[dt_prep][pos][1])+"%")
               
            filewriter.writerow([dt_prep]+values)

main()