import numpy as np
import time

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

# 使用alpha-beta pruning找出最佳路徑
# path, score, player, scores = alpha_beta(self, -np.inf, np.inf, 100, True)
path, score, scores = alpha_beta(self, -np.inf, np.inf, 500, True)

# 結束計時
end = time.time()

# 輸出結果
out = ''
# print(path)
# print(path[0][0], '#:', path[0][1])
out += str(path[0][0])+ ' #: ' + str(path[0][1]) + '\n' # 選出最佳路徑的第一步
# print(score, 'points')
out += str(score)+' points\n' # 加上分數
# print(scores)
# print('Total run time = ', "{:0.3f}".format(end-start), 'seconds.')
out += 'Total run time = ' + "{:0.3f}".format(end-start) + ' seconds.' # 加上運行時間

# 寫入output.txt
with open("output.txt", 'w') as f2:
    f2.write(out)
    f2.close()




