'''
小组成员：刘璐瑶
负责模块：游戏结果即玩家胜负或平局判定
**请编写必要注释以便小组其他成员更好的理解
'''
#游戏结果判断
def panduan():
    iswin = 0 #标记是否有一方完成五子相连，0代表否
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
    boring=[]   #遍历棋盘，记录每个棋格状态
    for i in range(num):
        for j in range(num):
            boring.append(QP[i][j])
    if -1 not in boring and iswin != 1:  #当棋盘中不存在无棋子的棋格且双方均为完成五子相连判定为平局
        print(messagebox.askokcancel('游戏结束','旗鼓相当！平局！'))

#决出胜负
def win():
    global stop,hq
    a.config(text=key[(tag+1)%2],fg=color[(tag+1)%2])
    b.config(text = "获胜",fg='red')
    stop,hq = 1,0 #决出胜负后游戏结束，不可悔棋
    if tag == 0:
        r=messagebox.askokcancel('游戏结束','白方五子相连！获胜！')
    else:
        r=messagebox.askokcancel('游戏结束','黑方五子相连！获胜！')  
    print(r)
