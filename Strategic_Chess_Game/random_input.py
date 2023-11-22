import random

# 隨機產生一個 1~8 的整數
n = random.randint(1,8)
m = random.randint(1,8)

length = ''
length = str(n) + ' ' + str(m) + '\n'

# 隨機產生0或1的矩陣
start = ''
for i in range(n):
    start = start + " ".join(str(random.randint(0,1)) for _ in range(m))
    start = start + '\n'
# 如果矩陣全為0，則重新產生
while start.count('1') == 0:
    start = ''
    for i in range(n):
        start = start + " ".join(str(random.randint(0,1)) for _ in range(m))
        start = start + '\n'

out = length + start
with open('input.txt', 'w') as f:
    f.write(out)
    f.close()
# print(length)
# print(start)
   