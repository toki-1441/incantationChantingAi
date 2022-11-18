import numpy as np
from random import randint
class SquarePuzzle:
    """
    正方形パズルクラス
    一辺の長さ=3の場合,8パズルになる. 以下が最終状態. 空白マスは0で表す.
    1 2 3
    4 5 6
    7 8 0
    一辺の長さ=4の場合,15パズルになる.
    """
    def __init__(self,edge_length=3,board=None):
        """
        コンストラクタ.
        edge_length:一辺の長さ.
        board:初期状態を指定する場合に使う. マスの配置を一次元化したもの.
        """
        if board is not None:
            assert len(board)==edge_length**2,f"invalid square. edge_length={edge_length} and board={board}"
            self.space = [x for x in range(edge_length ** 2) if board[x]==0][0]
            board = list(board)
        else:
            board=[i+1 for i in range(edge_length**2)]
            board[-1]=0  
            self.space = edge_length ** 2 - 1
        self.edge_length = edge_length
        self.board = board
        self.actions = [[0,1],[0,-1],[1,0],[-1,0]]
        self.step_count = 0

    def reset(self,shuffle_count=100):
        """
        板を初期化する.
        最終状態からshuffle_count回シャッフルする.shuffle_countが増えるほどパズルの難易度が上がる.
        """
        self.board=[i + 1 for i in range(self.edge_length ** 2)]
        self.board[-1]=0  
        self.space = self.edge_length ** 2 - 1
        self.step_count = 0
        pre_space = -1
        for _ in range(shuffle_count):
            i, j = divmod(self.space, self.edge_length)
            di, dj = self.actions[randint(0, len(self.actions) - 1)]
            ni, nj = i + di,j + dj
            if 0 <= ni < self.edge_length and 0 <= nj < self.edge_length and ni * self.edge_length + nj != pre_space:
                self.board[self.space], self.board[ni * self.edge_length+nj] = self.board[ni * self.edge_length + nj], self.board[self.space]
                pre_space = self.space
                self.space = ni * self.edge_length + nj
        return tuple(self.board)

    def step(self,action,air=False):
        """
        行動の結果(状態,報酬,終了フラグ,info)を返す.
        指定の方向へ動かせない場合,状態を変えず返す.
        action:行動.空白マスを動かす方向を表す. {0:右,1:左,2:下,3:上}
        air:状態を変えずに行動の結果を取得したい場合Trueにする.
        """
        if not air:self.step_count += 1
        i,j = divmod(self.space,self.edge_length)
        di,dj = self.actions[action]
        ni,nj = i+di,j+dj
        if air:
            board_ = self.board.copy()
        else:
            board_ = self.board
        if 0 <= ni < self.edge_length and 0 <= nj < self.edge_length:
            board_[self.space],board_[ni*self.edge_length+nj] = board_[ni*self.edge_length+nj],board_[self.space]
            if not air:self.space = ni * self.edge_length+nj
        done = all(board_[i] == (i + 1) % (self.edge_length ** 2) for i in range(self.edge_length ** 2))
        reward = 1 if done else 0
        info = {"step_count":self.step_count}
        return tuple(board_), reward, done, info
    
    def get_state(self):
        """
        現在の状態を返す.
        """
        return tuple(self.board)
        
    def get_able_actions(self):
        """
        可能なアクションを返す.
        """
        ret = []
        i,j = divmod(self.space,self.edge_length)
        if j < self.edge_length - 1:ret.append(0) # 右
        if 0 < j:ret.append(1) # 左
        if i < self.edge_length - 1:ret.append(2) # 下
        if 0 < i:ret.append(3) # 上
        return ret

    def show(self):
        """
        現在の状態をコンソールに表示する.
        """
        for i in range(self.edge_length):
            print(self.board[i*self.edge_length:(i+1)*self.edge_length])
    
    def self_game(self):
        """
        手動ゲームの作成
        """
        tuple1 = 1,2,3,4,5,6,7,8,0
        self.reset()
        while(self.get_state() != tuple1):
          self.show()
          print('操作を入力してください。0:右,1:左,2:下,3:上')
          movable = ','.join(map(str,self.get_able_actions()))
          print('ただし移動可能は'+movable+'です')
          your_choice = input('>>')
          if(int(your_choice) < 0):
            break
          self.step(int(your_choice))
        print('end')

class MyStack:
    def __init__(self):
        self.stack = []
    def push(self, item):
        self.stack.append(item)
    def pop(self):
        result = self.stack[-1]  # 末尾の要素を変数に取り出す
        del self.stack[-1]  # リストから要素を削除する
        return result  # リスト末尾から取り出したデータを返送する
    def semiitem(self,item):
        """
        同じものがあるかどうか
        """
        semiitem_have = self.stack.count(item)
        return semiitem_have != 0
