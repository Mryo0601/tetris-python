import numpy as np
from constants import GRID_WIDTH, GRID_HEIGHT, COLORS

# テトリミノの形状定義（4x4配列）
SHAPES = [
    # I
    np.array([
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]),
    # O
    np.array([
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ]),
    # T
    np.array([
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0]
    ]),
    # S
    np.array([
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [1, 1, 0, 0],
        [0, 0, 0, 0]
    ]),
    # Z
    np.array([
        [0, 0, 0, 0],
        [1, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0]
    ]),
    # J
    np.array([
        [0, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0]
    ]),
    # L
    np.array([
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [1, 1, 1, 0],
        [0, 0, 0, 0]
    ])
]

class Block:
    def __init__(self, shape_idx):
        self.shape_idx = shape_idx
        self.shape = SHAPES[shape_idx].copy()
        self.color = shape_idx
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.rotation = 0

    def rotate(self, clockwise=True):
        """ブロックを回転"""
        if clockwise:
            self.shape = np.rot90(self.shape, k=-1)
        else:
            self.shape = np.rot90(self.shape, k=1)
        self.rotation = (self.rotation + 1) % 4

    def move(self, dx, dy):
        """ブロックを移動"""
        self.x += dx
        self.y += dy

    def get_positions(self):
        """ブロックの位置を取得"""
        positions = []
        for i in range(4):
            for j in range(4):
                if self.shape[i][j]:
                    positions.append((self.x + j, self.y + i))
        return positions

    def collides_with(self, grid):
        """グリッドとの衝突判定"""
        for x, y in self.get_positions():
            if (x < 0 or x >= GRID_WIDTH or 
                y >= GRID_HEIGHT or 
                (y >= 0 and grid[y][x])):
                return True
        return False 