import tkinter as tk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.ttk as ttk
from tkinter import messagebox
dbname="weight.db"
#sqlを使う関数
def usesql(sqltext,param=()):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute(sqltext,param)
    conn.commit()
    conn.close()

sqltext="""CREATE TABLE IF NOT EXISTS personal (
            name TEXT,
            date TEXT, 
            weight REAL) """
usesql(sqltext)
#データをリストにして取得する場合
def getsql(sqltext):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute(sqltext)
    list=cur.fetchall()
    conn.close()
    return list
    
sqltext="""select distinct name from personal """
nlist=getsql(sqltext)
#addbtnの関数
def adddb():
    username,userweight=ncomb.get(),taijuentry.get()
    #名前確認
    if username=="ユーザー選択" or username=="":
        woring=messagebox.showerror("nameerror","名前を選択してください")
        return
    #日付確認
    if not (daycomb.get() and monthcomb.get()):
        woring=messagebox.showerror("date","月と日を半角数字で入力してください")
        return
    else :
        try:
            _=int(monthcomb.get())
            _=int(daycomb.get())
        except ValueError:
         woring=messagebox.showerror("dateerror","月と日を半角数字で入力してください")
         return
    #体重確認
    if not userweight:
        woring=messagebox.showerror("weighterror","体重を半角数字で入力してください")
        return
    else:
        try:
            userweight=float(userweight)
        except ValueError:
            woring=messagebox.showerror("weighterror","体重を半角数字で入力してください")
            return
    
    #本処理
    selectdate=yearentry.get()+"-"+monthcomb.get()+"-"+daycomb.get()
    selectdate="{}-{:0>2}-{:0>2}".format(int(yearentry.get()),int(monthcomb.get()),int(daycomb.get()))
    sqltext="INSERT INTO personal (name,date, weight) VALUES (?, ?, ?)"
    addparam=(username,selectdate, float(userweight))
    usesql(sqltext,addparam)

#graphbtnの関数（別ウィンドウでグラフ作る）
def makegraph():
    #グラフ用のデータの整理
    username=ncomb.get()
    #名前確認
    if username=="ユーザー選択" or username=="":
        woring=messagebox.showerror("nameerror","名前を選択してください")
        return
    sqltext="""select * from personal  where name='{}' order by date""".format(username)
    data=getsql(sqltext)
    name_dict={}
    for list in data:
        namedata=list[0]
        datedata=list[1]
        weightdata=list[2]
        if namedata not in name_dict:
            name_dict[namedata]={"date":[],"weight":[]}
        name_dict[namedata]["date"].append(datedata)
        name_dict[namedata]["weight"].append(weightdata)

    #グラフの作成
    fig,ax=plt.subplots()
    for name,value in name_dict.items():
        ax.plot(value["date"],value["weight"],label=name)
    ax.set_xlabel("date")
    ax.set_ylabel("weight(kg)")
    ax.set_title("weight-change")
    ax.legend()
    plt.xticks(rotation=45) 
    plt.tight_layout()  
    #新しいウィンドウを作る
    new_window=tk.Toplevel(root)
    new_window.title("weight-change")
    
    canvas=FigureCanvasTkAgg(fig,master=new_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

#メイン画面
root=tk.Tk()
root.geometry("200x130+600+300")
#１行目：名前(row=0)
ncomb=ttk.Combobox(root,value=nlist)
ncomb.set("ユーザー選択")
ncomb.grid(column=0,row=0)
#2行目：日付(row=1)
dateframe=tk.Frame(root);dateframe.grid(column=0,row=1)
yearentry=tk.Entry(dateframe,width=6);yearentry.grid(column=0,row=0)
nenlabel=tk.Label(dateframe,text="年",bg="white")
yearentry.insert(0,"2024");nenlabel.grid(column=1,row=0)
monthlist=list(range(1,13))
monthcomb=ttk.Combobox(dateframe,value=monthlist,width=4);monthcomb.grid(column=2,row=0)
gatsulabel=tk.Label(dateframe,text="月");gatsulabel.grid(column=3,row=0)
daylist=list(range(1,32))
daycomb=ttk.Combobox(dateframe,value=daylist,width=4);daycomb.grid(column=4,row=0)
nichilabel=tk.Label(dateframe,text="日");nichilabel.grid(column=5,row=0)
#3行目：体重(row=2)
weightframe=tk.Frame(root);weightframe.grid(column=0,row=2)
taijulabel=tk.Label(weightframe,text="体重");taijulabel.grid(column=0,row=0)
taijuentry=tk.Entry(weightframe,width=3);taijuentry.grid(column=1,row=0)
kglabel=tk.Label(weightframe,text="kg");kglabel.grid(column=2,row=0)
#4行目：ボタン(row=3)
addbtn=tk.Button(root,text="記録",command=adddb);addbtn.grid(column=0,row=3)
#5行目：グラフボタン(row=4)
graphbtn=tk.Button(root,text="グラフを見る",command=makegraph);graphbtn.grid(column=0,row=4)
root.mainloop()