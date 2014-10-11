import requests
import json
from datetime import datetime as dtime, timedelta
from tkinter import Tk, Canvas, BOTH
from math import ceil


def main():
    DAYS = 365
    WIDTH = 1000
    base_url = "http://api.coindesk.com/v1/bpi/historical/close.json"
    end = dtime.now().date()
    start = end - timedelta(days=DAYS)
    request_params = {
        'start': start.strftime("%Y-%m-%d"),
        'end': end.strftime("%Y-%m-%d"),
    }
    # что бы получить параметры в виде start=2014-10-10&end=...
    response = requests.get(base_url, params=request_params)
    if response.status_code != 200:  # 200 is HTTP OK
        print("Error, server returned: {}".format(response.status_code))
        return

    # мы получим строку от сервера, приведём в unicode строку
    # и с помощью библиотеки json превратим в структуру
    data = json.loads(response.content.decode('utf-8'))['bpi']
    # data = {
    #     '2014-10-10': "353.53",
    #     '2014-10-08': "353.48",
    #     '2014-10-09': "356.03",
    # }
    # из чисел в строки
    # map(int, '1', '2', '3') => int('1'), int('2'), int('3')
    # в результате имеем числа (1, 2, 3)
    max_value = ceil(max(data.values()))

    root = Tk()
    root.title = 'BitCoin graph'
    root.geometry("{}x{}".format(WIDTH, max_value))
    canvas = Canvas(root)
    canvas.pack(fill=BOTH, expand=1)

    step = WIDTH/len(data)
    for key, value in data.items():
        cur_date = dtime.strptime(key, "%Y-%m-%d").date()
        days = (cur_date-start).days
        canvas.create_rectangle(days*step, max_value,
                                (days+1)*step, max_value - round(value),
                                fill="black")

    root.mainloop()

if __name__ == '__main__':
    main()