'''
小组成员：余叶钰
负责模块：游戏的可视化设计。包括游戏界面设计及棋盘设计，
                 棋盘设计部分包括运行程序开始游戏及重新开局时初始化棋盘
**请编写必要注释以便小组其他成员更好的理解
'''
#重新开始游戏初始化棋盘
def restart():
    global QP,tag,a,b,stop,hq
    canvas.create_rectangle(0.3*mesh,0.3*mesh,mesh*(num+0.7),mesh*(num+0.7),fill="bisque")  #重绘棋盘
    QP = []     
    for i in range (num):
        QP.append([-1]*num)   #清空棋子
        canvas.create_line(mesh,mesh*(i+1),mesh*num,mesh*(i+1))
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
    num = 18 #棋盘网格数量
    tag = 0  #tag标记执棋方，0代表黑方，1代表白方 
    stop = 0 #stop标记游戏状态，0代表游戏进行中，1代表游戏结束
    mesh = round(B/num) #一个棋格宽度
    Qr   = 0.45 * mesh  #棋子半径，前面的系数可在0~0.5之间选取
    key  = ["黑方","白方"]
    color = ["black","white"]
    px,py = 0.01*B,0.15*B
    wide,high = 0.2*B,0.08*B
#初始化棋盘
    #用列表QP[]标记棋格状态
    #-1代表该位置无棋子，0代表该位置有黑棋，1代表该位置有白棋
    QP = []
    for i in range (num):
        QP.append([-1]*num)
    tk = Tk()            #建立根窗口
    tk.geometry(str(int((num+1)*mesh+3*px))+'x'+str(int((num+1)*mesh+py+2*px)))    #主窗口大小("宽*长")
    tk.title("五子连珠") #给窗口命名
#构造游戏界面
    asdf = Canvas(tk,width=(num+6)*mesh,height=(num+6)*mesh)             #asdf：窗体背景设计
    asdf.place(x=-1,y=-1)
    asdf.create_rectangle(0,0,(num+6)*mesh,(num+6)*mesh,fill="pink")
    canvas = Canvas(tk,width=str((num+1)*mesh),height=str((num+1)*mesh)) #canvas：棋盘设计
    canvas.place(x=px ,y=py)
    canvas.create_rectangle(0.3*mesh,0.3*mesh,mesh*(num+0.7),mesh*(num+0.7),fill="bisque")
    for i in range(num):                                                 #棋格绘制
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
