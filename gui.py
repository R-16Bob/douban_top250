from tkinter import *
from tkinter import ttk
import pymysql

root = Tk()  # 创建窗口对象的背景色
root.title('豆瓣电影TOP250')
root.geometry("1000x300")
frame1 = Frame(root)
frame2 = Frame(root)
# 创建标签和文本框
lb1=Label(frame1,text="hello")
lb1.grid(column=1,row=0)
lb1.configure(text="请输入要查询的电影名： ")
txt=Entry(frame1,width=10)
txt.grid(column=2,row=0)

# 按钮事件，根据文本框的内容查找电影
def search_movie():
    # 修改listb的内容
    # 清除列表
    x = tree.get_children()
    for item in x:
        tree.delete(item)
    # 列表插入查询信息
    db = pymysql.connect(host="localhost", user="root", passwd="pass", db="douban", charset='utf8mb4')
    # 获取游标
    cursor = db.cursor()
    title=txt.get()
    if title=='':
        sql="select * from top250"
    else:
        sql = "select * from top250 where name like '%" + title + "%'"
    cursor.execute(sql)
    data = cursor.fetchall()
    i = 0
    for movie in data:
        tree.insert("", i, values=movie)
        i += 1
    cursor.close()
    db.close()

# 获取数据库内容
def get_allmovie(tree):
    db = pymysql.connect(host="localhost", user="root", passwd="pass", db="douban", charset='utf8mb4')
    # 获取游标
    cursor = db.cursor()
    sql="select * from top250"
    cursor.execute(sql)
    data=cursor.fetchall()
    i=0
    for movie in data:
        tree.insert("",i,values=movie)
        i+=1
    cursor.close()
    db.close()

#创建按钮
btn=Button(frame1,text="确定", command=search_movie)
btn.grid(column=3, row=0)

# 创建表格
tree = ttk.Treeview(frame2,show="headings")      # #创建表格对象
tree["columns"] = ("rank", "name", "rate", "quote","staff")     # #定义列
tree.column("rank", width=100, anchor='center')          # #设置列
tree.column("name", width=100, anchor='center')
tree.column("rate", width=100, anchor='center')
tree.column("quote", width=200, anchor='center')
tree.column("staff", width=450, anchor='center')
tree.heading("rank", text="排名")        # #设置显示的表头名
tree.heading("name", text="影片名")
tree.heading("rate", text="评分")
tree.heading("quote", text="简介")
tree.heading("staff", text="staff")
tree.pack()

frame1.grid(column=0, row=0)
frame2.grid(column=0, row=1)
get_allmovie(tree)
root.mainloop()  # 进入消息循环