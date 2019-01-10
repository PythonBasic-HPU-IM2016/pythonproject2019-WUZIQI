'''
小组成员：吴佳丽
负责模块：游戏中玩家操作模块设计。包括落子、认输及悔棋。
**请编写必要注释以便小组其他成员更好的理解
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
        canvas.create_oval(x-Qr,y-Qr,x+Qr,y+Qr,fill=color[tag])  #绘制棋子
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
    if stop != 1:  #非游戏进行时不可认输     
        b.config(text = "认输",fg='black')
        stop,hq = 1,0   #认输后游戏结束，不可悔棋
        if tag == 0:
            r=messagebox.askokcancel('游戏结束','黑方认输，白方获胜！')
        else:
            r=messagebox.askokcancel('游戏结束','白方认输，黑方获胜！')  
    else:
        r=messagebox.askokcancel('提示','请点击开局开始游戏！')
