from tkinter import*
from tkinter import messagebox

def callback(event):
    global tag,x,y,a,hq
    X,Y = round(event.x/mesh)-1,round(event.y/mesh)-1 #欲落子处QP[X][Y]
    x,y = mesh*(x+1),mesh*(y)                         #欲落子处坐标(x,y)
    errorX,errorY = x-event.x ,y-event.y              #点击处与落子处坐标差值 
    distance = (errorX ** 2 + errorY ** 2) ** 0.5     #点击处与落子处距离差值
    #满足以下四点时可落子
    # 1.棋子落在棋盘上 2.差值不敏感 3.游戏正在进行 4.当前棋格无子
    if 0 <= X <=17 and 0 <= Y <= 17 and \
       distance < K*Qr and stop == 0 and QP[X][Y] == -1 :
        QP[x][y] = tag  #标记当前棋格         
        canvas.create_oval(x-Qr,y-Qr,x+Qr,y+Qr,fill=color[tag])  #绘制棋子
        hq = 1          #标记当前可悔棋
        panduan()       #调用自定义函数，判断游戏是否结束
        tag = (tag+1)%2 #更换执棋方
        a.config(text=key[tag],fg=color[tag]) #中间文字改变
        tagx,tagy = X,Y #储存当前落子坐标，悔棋时调用
def panduan():
    iswin = 0 #标记是否分出胜负，0代表否
    for i in range(num-4):
        for j in range (num):  #
            if QP[i][j]==QP[i+1][j]==QP[i+2][j]==QP[i+3][j]==QP[i+4][j] != -1:
                iswin = 1
                canvas.create_line(mesh*(i+1)-Qr/2,mesh*(j+1),mesh*(i+5)+Qr/2,mesh*(j+1),fill="yellow")
                win()
    for i in range(num):
        for j in range (num-4):
            if QP[i][j]==QP[i][j+1]==QP[i][j+2]==QP[i][j+3]==QP[i][j+4] != -1:
                iswin = 1
                canvas.create_line(mesh*(i+1),mesh*(j+1)-Qr/2,mesh*(i+1),mesh*(j+5)+Qr/2,fill="yellow")
                win()
    for i in range(num-4):
        for j in range(num-4):
            if QP[i][j]==QP[i+1][j+1]==QP[i+2][j+2]==QP[i+3][j+3]==QP[i+4][j+4] != -1:
                iswin = 1
                canvas.create_line(mesh*(i+1)-Qr/2,mesh*(j+1)-Qr/2,mesh*(i+5)+Qr/2,mesh*(j+5)+Qr/2,fill="yellow")
                win()
    for i in range(num-4):
        for j in range(4,num):
            if QP[i][j]==QP[i+1][j-1]==QP[i+2][j-2]==QP[i+3][j-3]==QP[i+4][j-4] != -1:
                iswin = 1
                canvas.create_line(mesh*(i+1)-Qr/2,mesh*(j+1)+Qr/2,mesh*(i+5)+Qr/2,mesh*(j-3)-Qr/2,fill="yellow")
                win()
    boring=[]
    for i in range(num):
        for j in range(num):
            boring.append(QP[i][j])
    if -1 not in boring and iswin != 1:
        print(messagebox.askokcancel('游戏结束','旗鼓相当！平局！'))
def restart():
    global QP,tag,a,b,stop,hq
    QP = []
    for i in range (num):
        QP.append([-1]*num)
        canvas.create_line(mesh,mesh*(i+1),mesh*num,mesh*(i+1))
        canvas.create_line(mesh*(i+1),mesh,mesh*(i+1),mesh*num)
    canvas.create_rectangle(mesh-20,mesh-20,mesh*num+20,mesh*num+20,fill="bisque")
    tag = 0
    stop = 0
    hq = 0
    a.config(text=key[tag],fg=color[tag])
    b.config(text="落子",fg=color[tag])  
def regret():
    global tag,hq
    if hq == 1:
        tag = (tag+1)%2
        a.config(text=key[tag],fg=color[tag])
        QP[tagx][tagy] = -1
        hq = 0
        x,y = mesh*(tagx+1),mesh*(tagy+1)
        #这里写的这么麻烦主要是因为tkinter 蛋疼的画图功能不够强大。
        #没有办法设置棋子边界颜色，悔棋后会留下印记。        
        #在棋子处，用黄色先覆盖
        canvas.create_rectangle(x-Qr,y-Qr,x+Qr,y+Qr,fill="bisque")
        #在黑色的边界处用画了黄颜色的线条
        canvas.create_line(x-Qr,y-Qr,x-Qr,y+Qr,fill="bisque")
        canvas.create_line(x-Qr,y+Qr,x+Qr,y+Qr,fill="bisque")
        canvas.create_line(x+Qr,y+Qr,x+Qr,y-Qr,fill="bisque")
        canvas.create_line(x+Qr,y-Qr,x-Qr,y-Qr,fill="bisque")
        #最后再画上棋线
        canvas.create_line(x,y-mesh/2 ,x,y+mesh/2)
        canvas.create_line(x-mesh/2,y ,x+mesh/2,y)
        #若棋子在边界，擦除界外棋线
        if y == 0:
            canvas.create_line(x,y-mesh/2,x,y,fill="bisque")
        if x == 0:
            canvas.create_line(x-mesh/2,y,x,y,fill="bisque")
        if y == 17:
            canvas.create_line(x,y,x,y+mesh/2,fill="bisque")
        if x == 17:
            canvas.create_line(x,y,x+mesh/2,y,fill="bisque")
    else:
        print(messagebox.askokcancel('提示','此时不能悔棋，请继续游戏或重新开局！'))
def lose():
    global stop
    if stop != 1:       
        a.config(text = key[tag],fg = color[tag])
        b.config(text = "认输",fg='black')
        stop = 1
        hq = 0
        if tag == 0:
            r=messagebox.askokcancel('游戏结束','黑方认输，白方获胜！')
        else:
            r=messagebox.askokcancel('游戏结束','白方认输，黑方获胜！')  
        print(r)
def win():
    global stop,hq
    a.config(text = key[tag],fg = color[tag])
    b.config(text = "获胜",fg='red')
    stop = 1
    hq = 0
    if tag == 0:
        r=messagebox.askokcancel('游戏结束','黑方五子相连！获胜！')
    else:
        r=messagebox.askokcancel('游戏结束','白方五子相连！获胜！')  
    print(r)

if __name__=='__main__':   
    K = 0.9  #点击的灵敏度 0~1 之间
    hq = 0   #hq标记是否可悔棋，0代表不可以，1代表可以
    num = 18 #棋盘网格数量
    tag = 0  #tag标记执棋方，0代表黑方，1代表白方 
    stop = 0 #stop标记游戏状态，0代表游戏进行中，1代表游戏结束
    mesh = round(500/num) #一个棋格宽度
    Qr = 0.45 * mesh #棋子半径，前面的系数可在0~0.5之间选取
    key = ["黑方","白方"]
    color = ["black","white"]
#初始化棋盘
    px,py = 5,75
    wide,high = 100,40
    #用列表QP[]标记棋格状态
    #-1代表该位置无棋子，0代表该位置有黑棋，1代表该位置有白棋
    QP = []
    for i in range (num):
        QP.append([-1]*num)
    tk = Tk() #建立根窗口
    tk.geometry(str((num+1)*mesh+2*px)+'x'+str((num+1)*mesh+py+px)) #主窗口大小("宽*长")
    tk.title('五子连珠') #给窗口命名
#构造棋盘界面
    asdf = Canvas(tk,width=(num+1)*mesh+2*px,height=(num+1)*mesh+py+px)
    asdf.place(x=0 ,y=0)
    asdf.create_rectangle(0,0,(num+1)*mesh+2*px,(num+1)*mesh+py+px,fill="pink")
    canvas = Canvas(tk,width=str((num+1)*mesh),height=str((num+1)*mesh))
    canvas.place(x=px ,y=py)
    canvas.create_rectangle(mesh-20,mesh-20,mesh*num+20,mesh*num+20,fill="bisque")
    for i in range(num):
        canvas.create_line(mesh,mesh*(i+1),mesh*num,mesh*(i+1))
        canvas.create_line(mesh*(i+1),mesh,mesh*(i+1),mesh*num)
    canvas.bind("<Button-1>", callback) #<Button-1>：鼠标左击事件
#几个按钮
    Button(tk,text="开局 / 重新开局",command=restart).place(x=4*px,\
                                                      y=(py-high)/2,width=wide,heigh=high)#按钮位置及尺寸
    Button(tk,text="落子方 悔棋 ",command=regret).place(x=(num+1)*mesh-2*wide-4*px-15,\
                                                      y=(py-high)/2,width=wide,heigh=high)
    Button(tk,text="执棋方 认输 ",command=lose).place(x=(num+1)*mesh-wide-4*px,\
                                                     y=(py-high)/2,width=wide,heigh=high)
#中间的文字
    a = Label(tk,text=key[tag],fg=color[tag],bg = "pink",font = ("楷体", "18", "bold"))
    b = Label(tk,text= "落子" ,fg=color[tag],bg = "pink",font = ("楷体", "18", "bold"))
    a.place(x=3*px+wide+40    ,y=(py-high)/2+3)
    b.place(x=3*px+wide+40+55 ,y=(py-high)/2+3)
    print(messagebox.askokcancel('提示','游戏开始！黑方先行！'))
    tk.mainloop() #创建循环事件直到关闭主窗口
