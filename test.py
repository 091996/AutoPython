import datetime

for i in range(1, 24):
    t_str = '2021-10-25 16:26:23'
    d = datetime.datetime.strptime(t_str, '%Y-%m-%d %H:%M:%S')
    delta = datetime.timedelta(days=i*14)
    n_days = d + delta
    print(n_days.strftime('%Y-%m-%d %H:%M:%S'))




