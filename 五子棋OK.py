'''
小组成员：吴佳丽
负责模块：游戏中玩家操作模块设计。包括落子、认输及悔棋
**注意**：请编写必要注释以便小组其他成员更好的理解
'''
#玩家落子
def callback(event):
    global tag,x,y,a,hq,tagx,tagy
    X,Y = round(event.x/mesh)-1,round(event.y/mesh)-1 #欲落子处QP[X][Y]
    x,y = mesh*(X+1),mesh*(Y+1)                       #欲落子处坐标(x,y)
    errorX,errorY = x-event.x ,y-event.y              #点击处与落子处坐标差值 
    distance = (errorX ** 2 + errorY ** 2) ** 0.5     #点击处与落子处距离差值
    #满足以下四点时可落子
    # 1.棋子落在棋盘上 2.差值不敏感 3.游戏正在进行 4.当前棋格无子
    if 0 <= X <=17 and 0 <= Y <= 17 and \
       distance < K*Qr and stop == 0 and QP[X][Y] == -1 :
        QP[X][Y] = tag  #标记当前棋格         
        canvas.create_oval(x-Qr,y-Qr,x+Qr,y+Qr,fill=color[tag])
        hq = 1          #标记当前可悔棋
        tag = (tag+1)%2 #更换执棋方
        a.config(text=key[tag],fg=color[tag]) #中间文字改变
        panduan()       #调用自定义函数，判断游戏是否结束
        tagx,tagy = X,Y #储存当前落子坐标，悔棋时调用
#玩家悔棋
def regret():
    global tag,hq
    if hq == 1:
        tag = (tag+1)%2     #悔棋后需重新落子，执棋方改变
        a.config(text=key[tag],fg=color[tag])
        QP[tagx][tagy] = -1 #悔棋后该棋格状态改变
        hq = 0              #一个回合只允许悔棋一次
        x,y = mesh*(tagx+1),mesh*(tagy+1)
        #棋盘恢复
        #绘制一个棋盘颜色的矩形覆盖棋子
        canvas.create_rectangle(x-Qr,y-Qr,x+Qr,y+Qr,fill="bisque")
        #覆盖绘制矩形产生的黑色边界
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
#玩家认输
def lose():
    global stop
    if stop != 1:       #非游戏进行时不可认输     
        b.config(text = "认输",fg='black')
        stop,hq = 1,0   #认输后游戏结束，不可悔棋
        if tag == 0:
            r=messagebox.askokcancel('游戏结束','黑方认输，白方获胜！')
        else:
            r=messagebox.askokcancel('游戏结束','白方认输，黑方获胜！')  
    else:
        r=messagebox.askokcancel('提示','请点击开局开始游戏！')

'''
小组成员：刘璐瑶
负责模块：游戏结果即玩家胜负或平局判定
**注意**：请编写必要注释以便小组其他成员更好的理解
'''
#游戏结果判断
def panduan():
    iswin = 0 #标记是否有一方完成五子相连，0代表否 平局判断时调用
    #判断是否有一方获胜
    #列表QP[a][b]中必须满足 0 <= a,b <= 17，i、j严格控制 
    for i in range (num-4):
        for j in range (num):    #判断是否出现有一方"—"五子相连
            if QP[i][j]==QP[i+1][j]==QP[i+2][j]==QP[i+3][j]==QP[i+4][j] != -1:
                iswin = 1
                canvas.create_line(mesh*(i+1)-Qr/2,mesh*(j+1),mesh*(i+5)+Qr/2,mesh*(j+1),fill="yellow")
                win()
    for i in range (num):
        for j in range (num-4):  #判断是否出现有一方"|"五子相连
            if QP[i][j]==QP[i][j+1]==QP[i][j+2]==QP[i][j+3]==QP[i][j+4] != -1:
                iswin = 1
                canvas.create_line(mesh*(i+1),mesh*(j+1)-Qr/2,mesh*(i+1),mesh*(j+5)+Qr/2,fill="yellow")
                win()
    for i in range (num-4):
        for j in range (num-4):  #判断是否出现有一方"\"五子相连
            if QP[i][j]==QP[i+1][j+1]==QP[i+2][j+2]==QP[i+3][j+3]==QP[i+4][j+4] != -1:
                iswin = 1
                canvas.create_line(mesh*(i+1)-Qr/2,mesh*(j+1)-Qr/2,mesh*(i+5)+Qr/2,mesh*(j+5)+Qr/2,fill="yellow")
                win()
    for i in range (num-4):
        for j in range (4,num):  #判断是否出现有一方"/"五子相连
            if QP[i][j]==QP[i+1][j-1]==QP[i+2][j-2]==QP[i+3][j-3]==QP[i+4][j-4] != -1:
                iswin = 1
                canvas.create_line(mesh*(i+1)-Qr/2,mesh*(j+1)+Qr/2,mesh*(i+5)+Qr/2,mesh*(j-3)-Qr/2,fill="yellow")
                win()
    #判断是否平局
    boring=[]
    for i in range(num):
        for j in range(num):
            boring.append(QP[i][j])
    if -1 not in boring and iswin != 1:  #当棋盘中不存在无棋子的棋格且双方均为完成五子相连判定为平局
        print(messagebox.askokcancel('游戏结束','旗鼓相当！平局！'))
#决出胜负
def win():
    global stop,hq
    a.config(text=key[(tag+1)%2],fg=color[(tag+1)%2]) #玩家落子后身份立即转换，故获胜方为当前落子方
    b.config(text = "获胜",fg='red')
    stop,hq = 1,0 #决出胜负后游戏结束，不可悔棋
    if tag == 0:
        r=messagebox.askokcancel('游戏结束','白方五子相连！获胜！')
    else:
        r=messagebox.askokcancel('游戏结束','黑方五子相连！获胜！')  
    print(r)
'''
小组成员：余叶钰
负责模块：游戏的可视化设计。包括游戏界面设计及棋盘设计，
          棋盘设计部分包括运行程序开始游戏及重新开局时初始化棋盘
**注意**：请编写必要注释以便小组其他成员更好的理解
'''
#重新开始游戏初始化棋盘
def restart():
    global QP,tag,a,b,stop,hq
    canvas.create_rectangle(0.3*mesh,0.3*mesh,mesh*(num+0.7),mesh*(num+0.7),fill="bisque")  #重绘棋盘，目的在于清空棋盘棋子
    QP = []     
    for i in range (num):
        QP.append([-1]*num)   #初始化虚拟棋盘
        canvas.create_line(mesh,mesh*(i+1),mesh*num,mesh*(i+1)) #重绘棋线
        canvas.create_line(mesh*(i+1),mesh,mesh*(i+1),mesh*num)        
    tag,stop,hq = 0,0,0
    a.config(text=key[tag],fg=color[tag])
    b.config(text="落子",fg=color[tag]) 


from tkinter import*
from tkinter import messagebox
if __name__=='__main__':
    B = 500  
    K = 0.9  #点击的灵敏度 0~1 之间
    hq = 0   #hq标记是否可悔棋，0代表不可以，1代表可以
    num = 15 #棋盘网格数量
    tag = 0  #tag标记执棋方，0代表黑方，1代表白方 
    stop = 0 #stop标记游戏状态，0代表游戏进行中，1代表游戏结束
    mesh = round(B/num) #一个棋格宽度
    Qr   = 0.45 * mesh  #棋子半径，前面的系数可在0~0.5之间选取
    key  = ["黑方","白方"]
    color = ["black","white"]
    px,py = 0.01*B,0.15*B
    wide,high = 0.2*B,0.08*B
#初始化棋盘
    #用虚拟棋盘列表QP[]标记棋格状态
    #-1代表该位置无棋子，0代表该位置有黑棋，1代表该位置有白棋
    QP = []
    for i in range (num):
        QP.append([-1]*num)
    tk = Tk()
    tk.geometry(str(int((num+1)*mesh+3*px))+'x'+str(int((num+1)*mesh+py+2*px)))
    tk.title("五子连珠") 
#构造游戏界面
    asdf = Canvas(tk,width=(num+6)*mesh,height=(num+6)*mesh)             #asdf：窗体背景设计
    asdf.place(x=-1,y=-1)
    asdf.create_rectangle(0,0,(num+6)*mesh,(num+6)*mesh,fill="pink")
    canvas = Canvas(tk,width=str((num+1)*mesh),height=str((num+1)*mesh)) #canvas：棋盘设计
    canvas.place(x=px ,y=py)
    canvas.create_rectangle(0.3*mesh,0.3*mesh,mesh*(num+0.7),mesh*(num+0.7),fill="bisque")
    for i in range(num):                                                 
        canvas.create_line(mesh,mesh*(i+1),mesh*num,mesh*(i+1))          
        canvas.create_line(mesh*(i+1),mesh,mesh*(i+1),mesh*num)
    canvas.bind("<Button-1>", callback)
#几个按钮
    Button(tk,text="开局 / 重新开局",command=restart).place(x=4*px,y=(py-high)/2,\
                                                      width=wide,heigh=high)#按钮位置及尺寸
    Button(tk,text="落子方 悔棋 ",command=regret).place(x=(num+1)*mesh-2*wide-4*px-15,y=(py-high)/2,\
                                                      width=wide,heigh=high)
    Button(tk,text="执棋方 认输 ",command=lose).place(x=(num+1)*mesh-wide-4*px,y=(py-high)/2,\
                                                      width=wide,heigh=high)
#中间的文字
    a = Label(tk,text=key[tag],fg=color[tag],bg = "pink",font = ("楷体", "18", "bold"))
    b = Label(tk,text= "落子" ,fg=color[tag],bg = "pink",font = ("楷体", "18", "bold"))
    a.place(x=3*px+wide+40    ,y=(py-high)/2+3)
    b.place(x=3*px+wide+40+55 ,y=(py-high)/2+3)
    print(messagebox.askokcancel('提示','游戏开始！黑方先行！'))
    tk.mainloop()
