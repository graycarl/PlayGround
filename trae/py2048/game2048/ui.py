import tkinter as tk
from tkinter import messagebox
from .constants import *
from .logic import GameLogic

class GameUI:
    def __init__(self, master):
        self.master = master
        self.game = GameLogic()
        self.cells = []
        self._setup_window()
        self._init_ui()
        self.animations = []  # 存储当前动画
        self.after_id = None  # 动画定时器ID

    def _setup_window(self):
        self.master.title("2048 Game")
        self.master.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.master.resizable(False, False)
        self.master.configure(bg=WINDOW_BG)

    def _init_ui(self):
        self.grid_frame = tk.Frame(self.master, bg=GRID_BG, bd=3)
        self.grid_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        for i in range(GRID_SIZE):
            row = []
            for j in range(GRID_SIZE):
                cell = tk.Label(
                    self.grid_frame, 
                    text='', 
                    width=CELL_WIDTH, 
                    height=CELL_HEIGHT,
                    font=FONT, 
                    bg=CELL_BG,
                    relief='raised'
                )
                cell.grid(row=i, column=j, padx=CELL_PAD, pady=CELL_PAD)
                row.append(cell)
            self.cells.append(row)
        
        self.master.bind('<Key>', self._handle_keypress)
        self._update_ui()

    def _update_ui(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.game.board[i][j]
                self.cells[i][j]['text'] = str(value) if value else ''
                self.cells[i][j]['fg'] = COLORS[value][0]
                self.cells[i][j]['bg'] = COLORS[value][1]

    def _animate_move(self, from_row, from_col, to_row, to_col, value, is_merge):
        """创建移动动画"""
        # 计算起始和结束位置
        from_x = from_col * (CELL_SIZE + 2*CELL_PAD) + CELL_PAD
        from_y = from_row * (CELL_SIZE + 2*CELL_PAD) + CELL_PAD
        to_x = to_col * (CELL_SIZE + 2*CELL_PAD) + CELL_PAD
        to_y = to_row * (CELL_SIZE + 2*CELL_PAD) + CELL_PAD
        
        # 创建动画标签
        label = tk.Label(
            self.grid_frame,
            text=str(value),
            font=FONT,
            fg=COLORS[value][0],
            bg=COLORS[value][1],
            width=CELL_WIDTH,
            height=CELL_HEIGHT,
            relief='raised'
        )
        label.place(x=from_x, y=from_y)
        
        # 合并效果特殊处理
        if is_merge:
            label.config(font=('Arial', 42, 'bold'))
        
        # 添加到动画队列
        self.animations.append({
            'label': label,
            'from_x': from_x,
            'from_y': from_y,
            'to_x': to_x,
            'to_y': to_y,
            'current_x': from_x,
            'current_y': from_y,
            'value': value,
            'is_merge': is_merge
        })
        
        # 启动动画循环
        if not self.after_id:
            self._update_animations()

    def _update_animations(self):
        """更新所有动画"""
        if not self.animations:
            self.after_id = None
            self._update_ui()  # 动画完成后更新UI
            return
            
        for anim in self.animations[:]:
            # 计算移动步长
            dx = anim['to_x'] - anim['current_x']
            dy = anim['to_y'] - anim['current_y']
            distance = (dx**2 + dy**2)**0.5
            
            if distance < ANIMATION_SPEED:
                # 动画完成
                anim['label'].destroy()
                self.animations.remove(anim)
                continue
                
            # 更新位置
            step_x = dx * ANIMATION_SPEED / distance
            step_y = dy * ANIMATION_SPEED / distance
            anim['current_x'] += step_x
            anim['current_y'] += step_y
            anim['label'].place(
                x=int(anim['current_x']),
                y=int(anim['current_y'])
            )
        
        self.after_id = self.master.after(ANIMATION_DELAY, self._update_animations)

    def _handle_keypress(self, event):
        if self.animations:
            return
            
        direction_map = {
            'Up': 'up',
            'Down': 'down',
            'Left': 'left',
            'Right': 'right'
        }
        
        if event.keysym in direction_map:
            moved, moves = self.game.move(direction_map[event.keysym])
            if moved:
                # 处理所有移动和合并动画
                for move in moves:
                    self._animate_move(*move)
                
                # 动画完成后添加新方块
                def add_new_tile():
                    pos, value = self.game.add_random_tile()
                    if pos:
                        self._animate_spawn(pos[0], pos[1], value)
                    self._update_ui()
                    if self.game.is_game_over():
                        messagebox.showinfo("Game Over", "Game Over!")
                        self._reset_game()
                
                self.master.after(len(moves) * ANIMATION_DELAY * 20, add_new_tile)

    def _animate_spawn(self, row, col, value):
        """生成新方块的动画"""
        x = col * (CELL_SIZE + 2*CELL_PAD) + CELL_PAD
        y = row * (CELL_SIZE + 2*CELL_PAD) + CELL_PAD
        
        label = tk.Label(
            self.grid_frame,
            text=str(value),
            font=FONT,
            fg=COLORS[value][0],
            bg=COLORS[value][1],
            width=CELL_WIDTH,
            height=CELL_HEIGHT,
            relief='raised'
        )
        label.place(x=x, y=y)
        
        # 初始缩放效果
        label.config(font=('Arial', 10, 'bold'))
        
        def grow(size):
            if size >= 36:
                label.config(font=FONT)
                label.destroy()
                self.cells[row][col].config(
                    text=str(value),
                    fg=COLORS[value][0],
                    bg=COLORS[value][1]
                )
            else:
                label.config(font=('Arial', size, 'bold'))
                self.master.after(10, lambda: grow(size + 2))
        
        grow(10)

    def _reset_game(self):
        """自动重置游戏状态"""
        self.game.reset_game()
        self._update_ui()