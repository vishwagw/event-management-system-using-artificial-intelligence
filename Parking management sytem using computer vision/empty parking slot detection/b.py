# libs
import pandas as pd
import datetime
import csv

def check(output, per = 15):
    df = pd.read_csv()
    df1 = pd.read_csv()
    out = output.split(',')
    time = datetime.datetime.now()
    time1 = time.hour
    out.append(time)
    print(out)
    id = out[0]
    if id not in list(df['regno']):
        print('no')
        return (0., 0)
    else:
        if id not in list(df1['regno']):
            with open('', 'a') as file:
                writer = csv.writer(file)
                writer.writerow(out)
                return (1, out)
        else:
            for i in range(len(df1['regno'])):
                if df1["regno"][i] == id:
                    t2 = df1["entry"][i]
                    delta = time1 - t2
                    print(delta)
                    price = per*delta + per
    return (price, out)

