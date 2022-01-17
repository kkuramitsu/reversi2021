#
# オセロ（リバーシ） 6x6
#

N = 6  # 大きさ

EMPTY = 0  # 空
BLACK = 1  # 黒
WHITE = 2  # 白
STONE = ['□', '●', '○']  #石の文字

#
# board = [0] * (N*N)
#

def xy(p):    # 1次元から2次元へ
  return p % N, p // N


def p(x, y):    # 2次元から1次元へ
  return x + y * N

# リバーシの初期画面を生成する

def init_board():
  board = [EMPTY] * (N*N)
  c = N//2
  board[p(c, c)] = BLACK
  board[p(c-1, c-1)] = BLACK
  board[p(c, c-1)] = WHITE
  board[p(c-1, c)] = WHITE
  return board

# リバーシの画面を表示する

def show_board(board):
  counts = [0, 0, 0]
  for y in range(N):
    for x in range(N):
      stone = board[p(x, y)]
      counts[stone] += 1
      print(STONE[stone], end='')
    print()
  print()
  for pair in zip(STONE, counts):
    print(pair, end=' ')
  print()


# (x,y) が盤面上か判定する
def on_borad(x, y):
  return 0 <= x < N and 0 <= y < N

# (x,y)から(dx,dy)方向をみて反転できるか調べる
def try_reverse(board, x, y, dx, dy, color):
  if not on_borad(x, y) or board[p(x, y)] == EMPTY:
    return False
  if board[p(x, y)] == color:
    return True
  if try_reverse(board, x+dx, y+dy, dx, dy, color):
    board[p(x, y)] = color
    return True
  return False

# 相手（反対）の色を返す
def opposite(color):
  if color == BLACK:
    return WHITE
  return BLACK

# (x,y) が相手（反対）の色かどうか判定

def is_oposite(board, x, y, color):
  return on_borad(x, y) and board[p(x, y)] == opposite(color)


DIR = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0),         (1, 0),
    (-1, 1), (0, 1), (1, 1),
]

def put_and_reverse(board, position, color):
  if board[position] != EMPTY:
  	return False
  board[position] = color

  x, y = xy(position)
  turned = False
  for dx, dy in DIR:
    nx = x + dx
    ny = y + dy
    if is_oposite(board, nx, ny, color):
      if try_reverse(board, nx, ny, dx, dy, color):
        turned = True
  if not turned:
    board[position] = EMPTY
  return turned

# プレイが継続できるか？ 
# つまり、まだ石を置けるところが残っているか調べる？
def can_play(board, color):
  board = board[:] # コピーしてボードを変更しないようにする
  for position in range(0, N*N):
    if put_and_reverse(board, position, color):
      return True
  return False


def game(player1, player2):
	board = init_board()
	show_board(board)
	on_gaming = True  # 　ゲームが続行できるか？
	while on_gaming:
		on_gaming = False  # 　いったん、ゲーム終了にする
		if can_play(board, BLACK):
			# player1 に黒を置かせる
			position = player1(board[:], BLACK)
			show_board(board)
			# 黒が正しく置けたら、ゲーム続行
			on_gaming = put_and_reverse(board, position, BLACK)
		if can_play(board, WHITE):
			# player1 に白を置かせる
			position = player2(board[:], WHITE)
			show_board(board)
			# 白が置けたらゲーム続行
			on_gaming = put_and_reverse(board, position, WHITE)
	show_board(board)  # 最後の結果を表示!

# AI 用のインターフェース
  
def my_AI(board, color): #おチビちゃんAI
  for position in range(N*N):
    if put_and_reverse(board, position, color):
      return position
  return 0


from collections import deque

H = [10,5,5,5,5,10,
      5,1,2,2,1,5,
      5,2,0,0,2,5,
      5,2,0,0,2,5,
      5,1,2,2,1,5,
     10,5,5,5,5,10]
       
def maxhand(board,color):
  hako = []
  for i in range(N*N):
    if put_and_reverse(board[:],i,color):
      hako.append(i)
  if len(hako) == 0:
    return 0
  else:
    d = []
    for k in hako:
      put_and_reverse(board,k,color)
      s = 0
      for j in range(N*N):
        if board[j] == color:
          s += H[j]
      d.append(s)
    p = max(d)
    return p


def yakiniku_AI(board,color):
  box = deque()
  box1 = []
  for position in range(N*N):
    if put_and_reverse(board[:],position,color):
      box.append(position)
      box1.append(position)

  if color == BLACK:
    AC = WHITE
  else:
    AC = BLACK
  enemypoint = []
  a_board = board
  if len(box) != 0:  
    while len(box) > 0:
      x = box.popleft()
      put_and_reverse(a_board,x,color)
      b_board = board[:]
      n = maxhand(b_board,AC)
      enemypoint.append(n)
    e = min(enemypoint)
    posi = box1[enemypoint.index(e)]
    return posi
  return 0