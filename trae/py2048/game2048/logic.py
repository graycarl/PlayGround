import random
from .constants import GRID_SIZE

class GameLogic:
    def __init__(self):
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.reset_game()

    def reset_game(self):
        self.board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()

    def add_random_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE) 
                      for j in range(GRID_SIZE) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = random.choice([2, 4])

    def move(self, direction):
        moves = []  # 存储所有移动信息
        moved = False
        
        if direction == 'up':
            moved, moves = self._move_vertical(False)
        elif direction == 'down':
            moved, moves = self._move_vertical(True)
        elif direction == 'left':
            moved, moves = self._move_horizontal(False)
        elif direction == 'right':
            moved, moves = self._move_horizontal(True)
            
        return moved, moves

    def _move_vertical(self, reverse):
        moves = []
        moved = False
        for j in range(GRID_SIZE):
            # 获取非零元素及其原始位置
            tiles = [(i, self.board[i][j]) for i in range(GRID_SIZE) if self.board[i][j] != 0]
            if reverse:
                tiles = tiles[::-1]
            
            # 合并处理
            merged = []
            i = 0
            while i < len(tiles):
                if i + 1 < len(tiles) and tiles[i][1] == tiles[i+1][1]:
                    # 合并记录
                    new_val = tiles[i][1] * 2
                    moves.append((tiles[i][0], j, tiles[i+1][0], j, new_val, True))
                    merged.append(new_val)
                    self.score += new_val
                    i += 2
                else:
                    # 移动记录
                    if reverse:
                        new_pos = GRID_SIZE - len(merged) - 1
                    else:
                        new_pos = len(merged)
                    if tiles[i][0] != new_pos:
                        moves.append((tiles[i][0], j, new_pos, j, tiles[i][1], False))
                    merged.append(tiles[i][1])
                    i += 1
            
            # 填充零
            if reverse:
                merged = [0] * (GRID_SIZE - len(merged)) + merged[::-1]
            else:
                merged += [0] * (GRID_SIZE - len(merged))
            
            # 更新棋盘
            for i in range(GRID_SIZE):
                if self.board[i][j] != merged[i]:
                    moved = True
                    self.board[i][j] = merged[i]
        
        return moved, moves

    def _move_horizontal(self, reverse):
        moves = []
        moved = False
        for i in range(GRID_SIZE):
            row = [num for num in self.board[i] if num != 0]
            if reverse:
                row = row[::-1]
            new_row = self._merge_tiles(row)
            if reverse:
                new_row = new_row[::-1]
                new_row = [0] * (GRID_SIZE - len(new_row)) + new_row
            else:
                new_row += [0] * (GRID_SIZE - len(new_row))
            
            for j in range(GRID_SIZE):
                if self.board[i][j] != new_row[j]:
                    moved = True
                    self.board[i][j] = new_row[j]
        return moved, moves

    def _merge_tiles(self, tiles):
        merged = []
        i = 0
        while i < len(tiles):
            if i + 1 < len(tiles) and tiles[i] == tiles[i+1]:
                merged.append(tiles[i] * 2)
                self.score += tiles[i] * 2
                i += 2
            else:
                merged.append(tiles[i])
                i += 1
        return merged

    def is_game_over(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.board[i][j] == 0:
                    return False
                if j < GRID_SIZE - 1 and self.board[i][j] == self.board[i][j+1]:
                    return False
                if i < GRID_SIZE - 1 and self.board[i][j] == self.board[i+1][j]:
                    return False
        return True