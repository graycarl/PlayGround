# 游戏配置常量
GRID_SIZE = 4
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
WINDOW_BG = '#faf8ef'
GRID_BG = '#bbada0'
CELL_BG = '#cdc1b4'
CELL_PAD = 7.5
CELL_WIDTH = 6
CELL_HEIGHT = 3
FONT = ('Arial', 36, 'bold')

# 颜色配置
COLORS = {
    0: ('#cdc1b4', '#cdc1b4'),
    2: ('#776e65', '#eee4da'),
    4: ('#776e65', '#ede0c8'),
    8: ('#f9f6f2', '#f2b179'),
    16: ('#f9f6f2', '#f59563'),
    32: ('#f9f6f2', '#f67c5f'),
    64: ('#f9f6f2', '#f65e3b'),
    128: ('#f9f6f2', '#edcf72'),
    256: ('#f9f6f2', '#edcc61'),
    512: ('#f9f6f2', '#edc850'),
    1024: ('#f9f6f2', '#edc53f'),
    2048: ('#f9f6f2', '#edc22e')
}

# 动画配置
ANIMATION_SPEED = 10  # 移动速度(像素/帧)
ANIMATION_DELAY = 5   # 帧间隔(毫秒)

# 单元格尺寸计算
CELL_SIZE = int((WINDOW_WIDTH - 2 * CELL_PAD * (GRID_SIZE + 1)) / GRID_SIZE)