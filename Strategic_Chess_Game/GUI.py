import pygame
import sys
from pygame.locals import QUIT,KEYDOWN
import numpy as np
import time

pygame.init()
#獲取對顯示系統的訪問，并創建一個視窗screen
#視窗大小為670x670

# 開始計時
start = time.time()

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

# 讀取input.txt
with open("input.txt", "r") as f:
    content = f.read().split('\n')
    size = content[0].split(' ')
    n = int(size[0])
    m = int(size[1])
    f.close()

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


screen = pygame.display.set_mode((670, 670))
screen_color = [255, 226, 168] #設定畫布顏色
line_color = [82, 54, 0] #設定線條顏色

def find_pos(x,y):#找到顯示的可以落子的位置
    for i in range(27,670,44):
        for j in range(27,670,44):
            L1=i-22
            L2=i+22
            R1=j-22
            R2=j+22
            if x>=L1 and x<=L2 and y>=R1 and y<=R2:
                return i,j
    return x,y

flag = False
tim = -1

over_pos = [] #表示已經落子的位置
# white_color = [255, 255, 255] #白棋顏色
black_color = [82, 54, 0] #黑棋顏色

interval = 60 # 間隔60px
col = m # 列數
row = n # 行數

player1_score = 0
player2_score = 0

chess_old = chess.copy()

while True: #不斷訓練重繪畫布

    for event in pygame.event.get(): #獲取事件，如果滑鼠點擊右上角關閉按鈕，關閉
        if event.type in (QUIT,KEYDOWN):
            sys.exit()

    screen.fill(screen_color) #清屏
    for i in range(27, 27+interval*col+1, interval): #畫棋盤邊緣線
    # for i in range(27,670,44):
        # #先畫豎線
        # if i==27 or i==670-27:#邊緣線稍微粗一些
        #     pygame.draw.line(screen,line_color,[i,27],[i,670-27],4)
        # else:
        #     pygame.draw.line(screen,line_color,[i,27],[i,670-27],2)
        pygame.draw.line(screen, line_color, [i,27], [i, interval*row+27], 2)
        #再畫橫線
        # if i == 27 or i == interval*col:#邊緣線稍微粗一些
        #     pygame.draw.line(screen, line_color, [27, i], [interval*col, i], 2)
        # else:
        #     pygame.draw.line(screen, line_color, [27,i],[interval*col, i], 2)
        # pygame.draw.line(screen, line_color, [27, i], [interval*col+27, i], 2)
    for i in range(27, 27+interval*row+1, interval): #畫棋盤邊緣線
        pygame.draw.line(screen, line_color, [27, i], [interval*col+27, i], 2)

    
    
    font = pygame.font.SysFont("Times New Roman", 30, bold=True)
    text = font.render("Game Start", True, (0, 0, 0))
    text_clicked = font.render("Running...", True, (0, 0, 0))
    text_rect = text_clicked.get_rect(center=(670/2, 620), width=150, height=32)
    # screen.blit(text, text_rect)
    


    #獲取滑鼠坐標資訊
    x, y = pygame.mouse.get_pos()

    x, y = find_pos(x,y)
   

    keys_pressed = pygame.mouse.get_pressed()# 獲取滑鼠按鍵資訊
    
    # 開始印出遊戲過程
    if keys_pressed[0]:
        flag = True
    if flag:
        pygame.draw.rect(screen, (255, 215, 0), text_rect)
        screen.blit(text_clicked, text_rect)
        if tim != -1 and tim < len(path):
            if tim%2 == 0:
                player1_score += scores[tim]
                player1 = '1st Player'
                score1 = str(path[tim][0]+str(path[tim][1])) + ' Total: ' + str(player1_score)+' points'
                text_player = font.render(player1, True, (255, 226, 168))
                text_score = font.render(score1, True, (82, 54, 0))
            else:
                player2_score += scores[tim]
                player2 = '2nd Player'
                score2 = str(path[tim][0]+str(path[tim][1])+' Total: '+str(player2_score)+' points')
                text_player = font.render(player2, True, (255, 226, 168))
                text_score = font.render(score2, True, (82, 54, 0))
            text_player_rect = text_player.get_rect(center=(670/2-130, 570), width=150, height=32)
            pygame.draw.rect(screen, (82, 54, 0), text_player_rect)
            text_score_rect = text_score.get_rect(center=(670/2+130, 570), width=150, height=32)
            screen.blit(text_player, text_player_rect)
            screen.blit(text_score, text_score_rect)
            if path[tim][0] == 'Row':
                for j in range(m):
                    chess[path[tim][1]-1][j] = 0
            elif path[tim][0] == 'Column':
                for i in range(n):
                    chess[i][path[tim][1]-1] = 0
        elif tim >= len(path): # 遊戲結束
            result = 'Score: '+str(score)+' points'+', '+'Total run time = ' + "{:0.3f}".format(end-start) + ' seconds.'
            text_player = font.render(result, True, (82, 54, 0))
            text_player_rect = text_player.get_rect(center=(670/2, 570), width=150, height=32)
            screen.blit(text_player, text_player_rect)
            time.sleep(1.5)
    else: # 遊戲未開始
        flag = False
        pygame.draw.rect(screen, (34, 139, 34), text_rect)
        screen.blit(text, text_rect)
        chess = chess_old.copy()
        tim = -1
        player1_score = 0
        player2_score = 0
    
    # 顯示所有棋子
    for i in range(n):
        for j in range(m):
            if chess[i][j] == 1:
                pygame.draw.circle(screen, black_color, [57+60*j, 57+60*i], 20, 0)
       

    #滑鼠左鍵延時作用
    if flag:
        tim += 1
        time.sleep(1.5)
   
    if tim == len(path)+3:
        flag = False
    

    pygame.display.update() # 重繪顯示

