import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import numpy as np
import time
import random


tim = 0
flag = False

# 節點資訊
class Node:
    def __init__(self, board, select, select_place, score, path, scores, parent):
        self.board = board # 棋盤
        self.successors = [] # 子節點
        self.parent = parent # 父節點
        self.selected = select # 選擇的行或列
        self.selected_place = select_place # 選擇的行或列的位置
        self.score = score # 分數
        self.scores = scores # 分數紀錄
        self.path = path # 路徑

# 创建主窗口
root = tk.Tk()
root.withdraw()  # 隐藏主窗口

# 弹出对话框让用户输入行数和列数
n = simpledialog.askinteger("Input", "Enter number of rows:", parent=root, minvalue=1, maxvalue=10)
m = simpledialog.askinteger("Input", "Enter number of columns:", parent=root, minvalue=1, maxvalue=10)

if n is not None and m is not None:
    # 显示主窗口
    root.deiconify()

    # # 创建棋盘
    # chessboard_frame = tk.Frame(root, borderwidth=1, relief="solid")
    # chessboard_frame.grid(row=0, column=0, padx=100, pady=80)
    # chessboard_frame.configure(background='#5897A0')
    # root.mainloop()

else:
    print("No input provided")
    

length = ''
length = str(n) + ' ' + str(m) + '\n'

# 隨機產生0或1的矩陣
start_str = ''
for i in range(n):
    start_str = start_str + " ".join(str(random.randint(0,1)) for _ in range(m))
    start_str = start_str + '\n'
# 如果矩陣全為0，則重新產生
while start_str.count('1') == 0:
    start_str = ''
    for i in range(n):
        start_str = start_str + " ".join(str(random.randint(0,1)) for _ in range(m))
        start_str = start_str + '\n'

out = length + start_str
with open('input.txt', 'w') as f3:
    f3.write(out)
    f3.close()

# 開始計時
start = time.time()

# 讀取input.txt
with open("input.txt", "r") as f:
    content = f.read().split('\n')
    size = content[0].split(' ')
    n = int(size[0])
    m = int(size[1])

# 建立棋盤
chess = np.zeros((n, m), dtype=int)
for i in range(n):
    row = content[i+1].split(' ')
    for j in range(m):
        chess[i][j] = int(row[j])

# 建立樹
self = Node(chess, None, None, 0, [], [], None) # initial state

# 找出所有子節點
def get_successors(self):
    successors = []
    for i in range(len(self.board)): # 取走第i行
        if 1 in self.board[i]:
            child_board = self.board.copy()
            num = sum([1 for j in range(len(child_board[i])) if child_board[i][j] == 1])
            child_board[i] = [0] * len(child_board[i])
            scores = self.scores + [num]
            path = self.path + [('Row', i+1)]  # 紀錄取走的行數
            successors.append(Node(child_board, 'Row', i+1, 0, path, scores, self))
    
    for j in range(len(self.board[0])): # 取走第j列
        if 1 in [self.board[i][j] for i in range(len(self.board))]:
            child_board = self.board.copy()
            num = sum([1 for i in range(len(child_board)) if child_board[i][j] == 1])
            for i in range(len(child_board)):
                child_board[i][j] = 0
            scores = self.scores + [num]
            path = self.path + [('Column', j+1)]  # 紀錄取走的列數
            successors.append(Node(child_board, 'Column', j+1, 0, path, scores, self))
    successors.sort(key=lambda node: node.scores[-1], reverse=True)  # 根據scores的最後一項進行排序
    self.successors = successors
   
# alpha-beta pruning
def alpha_beta(self, alpha, beta, depth, max_player):
    get_successors(self) # 找出所有子節點
    if len(self.successors) == 0 or depth == 0: # 如果沒有子節點或是達到最大深度
        score_even = sum(self.scores[::2])
        score_odd = sum(self.scores[1::2])
        self.score = score_even - score_odd # 計算分數
        return self.path, self.score, self.scores
    
    if max_player:
        v = -float('inf')
        best_path = []
        best_scores = []
        for child in self.successors:
            child_path, child_v, child_scores = alpha_beta(child, alpha, beta, depth-1, False)
            if child_v > v: 
                v = child_v
                best_path = child_path 
                best_scores = child_scores
            alpha = max(alpha, v)
            if alpha >= beta: # alpha剪枝
                break
        return best_path, v, best_scores
    else:
        v = float('inf')
        best_path = []
        best_scores = []
        for child in self.successors:
            child_path, child_v, child_scores = alpha_beta(child, alpha, beta, depth-1, True)
            if child_v < v:
                v = child_v
                best_path = child_path 
                best_scores = child_scores
            beta = min(beta, v) 
            if beta <= alpha: # beta剪枝
                break
        return best_path, v, best_scores

# 使用alpha-beta pruning找出最佳路徑
path, score, scores = alpha_beta(self, -np.inf, np.inf, 500, True)

# 結束計時
end = time.time()

# 輸出結果
out = ''
out += str(path[0][0])+ ' #: ' + str(path[0][1]) + '\n' # 選出最佳路徑的第一步
out += str(score)+' points\n' # 加上分數
out += 'Total run time = ' + "{:0.3f}".format(end-start) + ' seconds.' # 加上運行時間

# 寫入output.txt
with open("output.txt", 'w') as f2:
    f2.write(out)
    f2.close()

chess_old = chess.copy()

def start_game():
    global flag, tim, player1_score, player2_score, chess, chess_old
    flag = True
    chess = chess_old.copy()
    update_game()  # 开始游戏更新

player1_score = 0
player2_score = 0

# 创建主窗口
root = tk.Tk()
root.title("Strategic Chess Game")
root.configure(background='#829BB8')

# # 加载图像
# image_path = 'chess.png'  # 图像文件路径
# photo = PhotoImage(file=image_path)

# 创建棋盘
chessboard_frame = tk.Frame(root, borderwidth=1, relief="solid")
chessboard_frame.grid(row=0, column=0, padx=100, pady=80)
# chessboard_frame.configure(background='#64778D')


# 根据chess数组的值设置按钮颜色
color_map = {0: "#F0D9B5", 1: "#B58863"}
buttons = [[None for _ in range(m)] for _ in range(n)]  # 按钮数组

for i in range(n):  
    for j in range(m):
        color = color_map[chess[i][j]]
        # 创建一个更大尺寸的按钮
        button = tk.Button(chessboard_frame, bg=color, width=4, height=2)
        button.grid(row=i, column=j, padx=5, pady=5)
        buttons[i][j] = button


# 创建控制面板
control_frame = tk.Frame(root, borderwidth=1, relief="solid")
control_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

start_button = tk.Button(control_frame, text="Start", command=start_game, bg='#64778D', fg='white', font=('Times New Roman', 10))
start_button.pack(padx=10, pady=10)

# 创建结果显示区域
result_frame = tk.Frame(root, borderwidth=1, relief="solid", bg='#64778D')
result_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

result_label = tk.Label(result_frame, text="Result", bg='#64778D', fg='white', font=('Times New Roman', 10))
result_label.pack(padx=10, pady=10)

# 创建個別玩家分數顯示區域
score_frame = tk.Frame(root, borderwidth=1, relief="solid", bg='#64778D')
score_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

score_label = tk.Label(score_frame, text="Score", bg='#64778D', fg='white', font=('Times New Roman', 10))
score_label.pack(padx=10, pady=10)

def update_game():
    global tim, flag, player1_score, player2_score, n, m, chess
    if flag and tim < len(path):
        if tim % 2 == 0:
            player1_score += scores[tim]
            score1 = f'1st Player\nRow/Column: {path[tim][0]} {path[tim][1]}'
            result_label.config(text=score1)
            score_label.config(text=f'1st Player: {player1_score} points\n2nd Player: {player2_score} points')
        else:
            player2_score += scores[tim]
            score2 = f'2nd Player\nRow/Column: {path[tim][0]} {path[tim][1]}'
            result_label.config(text=score2)
            score_label.config(text=f'1st Player: {player1_score} points\n2nd Player: {player2_score} points')
        if path[tim][0] == 'Row':
            for j in range(m):
                chess[path[tim][1]-1][j] = 0
        elif path[tim][0] == 'Column':
            for i in range(n):
                chess[i][path[tim][1]-1] = 0

        for i in range(n):
            for j in range(m):
                color = color_map[chess[i][j]]
                buttons[i][j].config(bg=color)

        tim += 1
        if tim < len(path):
            root.after(2000, update_game)  # 继续周期性调用
        else:
            result = f'Score: {score} points, Total run time = {end-start:.3f} seconds.'
            result_label.config(text=result)
            # result = f'The End'
            # result_label.config(text=result)
            flag = False


root.mainloop()