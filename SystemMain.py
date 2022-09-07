import time
from tkinter import *

from ArchiveInsert import insert
from Login import login
from sqlcont import MSSQL

root = Tk()
root.title("血浆系统测试数据生成器")
screenwidth = root.winfo_screenwidth()  # 获取显示屏宽度
screenheight = root.winfo_screenheight()  # 获取显示屏高度
size = '%dx%d+%d+%d' % (600, 450, (screenwidth - 600) / 2, (screenheight - 450) / 2)  # 设置窗口居中参数
root.geometry(size)

items = {'建立新档案': 1, '无浆证浆员登记': 2, '有浆证浆员登记': 3, '建立体格检查并创建合格的病史征询': 4}
header = {}
vars = []
strvar = []
host = Label(root, text='测试地址')
host.grid(row=0, column=1, pady=10)
host_entry = Entry(root, textvariable=StringVar(root, 'http://qa-plasma.gdmk.cn:8280'))
host_entry.grid(row=0, column=2, pady=10)

hostuser = Label(root, text='测试账号')
hostuser.grid(row=0, column=3, pady=10)
hostuser_entry = Entry(root, width=15, textvariable=StringVar(root, '102'))
hostuser_entry.grid(row=0, column=4, pady=10)

hostpas = Label(root, text='账户密码')
hostpas.grid(row=0, column=5, pady=10)
hostpas_entry = Entry(root, textvariable=StringVar(root, 'Aa123456!@#'))
hostpas_entry.grid(row=0, column=6, pady=10)

link = Label(root, text='数据库地址')
link.grid(row=1, column=1)
link_entry = Entry(root, textvariable=StringVar(root, '192.168.1.197:49307'))
link_entry.grid(row=1, column=2)

linkuser = Label(root, text='数据库用户')
linkuser.grid(row=1, column=3)
linkuser_entry = Entry(root, textvariable=StringVar(root, 'sa'), width=15)
linkuser_entry.grid(row=1, column=4)

linkpas = Label(root, text='用户密码')
linkpas.grid(row=1, column=5)
linkpas_entry = Entry(root, textvariable=StringVar(root, 'maike123!@#+1s'))
linkpas_entry.grid(row=1, column=6)

linkdb = Label(root, text='db')
linkdb.grid(row=2, column=1)
linkdb_entry = Entry(root, textvariable=StringVar(root, 'PlasmaDB44002'), width=30)
linkdb_entry.grid(row=2, column=2,  columnspan=2)

for i in range(len(items)):
    vars.append(IntVar())
    strvar.append(IntVar())
for key, value in items.items():
    Checkbutton(root, onvalue=value, variable=vars[list(items.keys()).index(key)]).grid(row=value+3, column=1, pady=5)
    Label(root, text=key, justify=LEFT).grid(row=value+3, column=2, columnspan=3)
    Entry(root, textvariable=strvar[list(items.keys()).index(key)]).grid(row=value+3, column=5, columnspan=2)

text = Text(root, height=12)
text.grid(row=999, column=1, columnspan=6)



# 定义信息显示的方法
def showinfo(result):
    realtime = time.strftime("%Y-%m-%d %H:%M:%S ")
    textvar = realtime + result  # 系统时间和传入结果
    text.insert('end', textvar)  # 显示在text框里面
    text.insert('insert', '\n')  # 换行

def show():
    global header
    check = {}
    entvalue = {}

    for new_var in enumerate(vars):
        check[new_var[0]] = new_var[1].get()
    for val in enumerate(strvar):
        entvalue[val[0]] = val[1].get()
    print(check)
    print(entvalue)

    host = host_entry.get()
    hostuser = hostuser_entry.get()
    hostpas = hostpas_entry.get()

    if len(header) == 0:
        loginsystem = login(host, hostuser, hostpas)
        showinfo(loginsystem[0])
        header = loginsystem[1]

    link = link_entry.get()
    linkuser = linkuser_entry.get()
    linkpas = linkpas_entry.get()
    linkdb = linkdb_entry.get()
    MSSQL(host=link, user=linkuser, pwd=linkpas, db=linkdb)

    for k, v in check.items():
        if v != 0:
            print(entvalue[v-1])
            if v == 1:
                for i in range(0, entvalue[v-1]):
                    ins = insert(host, header)
                    showinfo(ins)
                    time.sleep(1)
            if v == 2:
                for i in range(0, entvalue[v-1]):
                    print(i)


Button(root, text='开 始', command=show).grid(row=99, column=1, columnspan=6, pady=5)

root.mainloop()
