import random
import numpy as np
from block import Block, SHAPES
from constants import (
    GRID_WIDTH, GRID_HEIGHT, COLORS,
    SCORE_PER_LINE, SCORE_MULTIPLIER,
    LINES_PER_LEVEL, SPEED_INCREASE_PER_LEVEL,
    INITIAL_FALL_SPEED
)
import time

class Tetris:
    def __init__(self, initial_level=1):
        self.grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=int)
        self.current_block = None
        self.next_block = None
        self.current_x = 0
        self.current_y = 0
        self.score = 0
        self.level = initial_level
        self.lines_cleared = 0
        self.game_over = False
        self.last_fall_time = time.time()
        self.fall_speed = INITIAL_FALL_SPEED - (self.level - 1) * SPEED_INCREASE_PER_LEVEL
        self.generate_new_block()
        self.generate_new_block()

    def generate_new_block(self):
        if self.next_block is None:
            self.next_block = Block(random.randint(0, len(SHAPES) - 1))
        self.current_block = self.next_block
        self.next_block = Block(random.randint(0, len(SHAPES) - 1))
        self.current_x = GRID_WIDTH // 2 - 2
        self.current_y = 0
        
        if self.check_collision():
            self.game_over = True
        
        if hasattr(self, 'on_new_block'):
            self.on_new_block()

    def check_collision(self):
        for i in range(4):
            for j in range(4):
                if self.current_block.shape[i][j]:
                    x = self.current_x + j
                    y = self.current_y + i
                    if (x < 0 or x >= GRID_WIDTH or 
                        y >= GRID_HEIGHT or 
                        (y >= 0 and self.grid[y][x])):
                        return True
        return False

    def rotate(self):
        """現在のブロックを回転"""
        self.current_block.rotate()
        if self.check_collision():
            self.current_block.rotate(clockwise=False)

    def move_left(self):
        """ブロックを左に移動"""
        self.current_x -= 1
        if self.check_collision():
            self.current_x += 1

    def move_right(self):
        """ブロックを右に移動"""
        self.current_x += 1
        if self.check_collision():
            self.current_x -= 1

    def move_down(self):
        """ブロックを下に移動"""
        self.current_y += 1
        if self.check_collision():
            self.current_y -= 1
            self.lock_block()
            return True
        return False

    def hard_drop(self):
        """ブロックを最下部まで一気に移動"""
        while not self.move_down():
            pass

    def lock_block(self):
        """現在のブロックをグリッドに固定"""
        for i in range(4):
            for j in range(4):
                if self.current_block.shape[i][j]:
                    y = self.current_y + i
                    x = self.current_x + j
                    if y >= 0:
                        self.grid[y][x] = self.current_block.color + 1
        self.clear_lines()
        self.generate_new_block()

    def clear_lines(self):
        """完成した行を消去"""
        lines_to_clear = []
        for i in range(GRID_HEIGHT):
            if all(self.grid[i]):
                lines_to_clear.append(i)

        if not lines_to_clear:
            return

        # スコア計算
        self.score += SCORE_PER_LINE * SCORE_MULTIPLIER[len(lines_to_clear) - 1] * self.level
        self.lines_cleared += len(lines_to_clear)
        
        # レベルアップ
        new_level = self.lines_cleared // LINES_PER_LEVEL + 1
        if new_level > self.level:
            self.level = new_level
            self.fall_speed = INITIAL_FALL_SPEED - (self.level - 1) * SPEED_INCREASE_PER_LEVEL

        # 行を消去して上から詰める
        for line in lines_to_clear:
            self.grid = np.vstack((np.zeros((1, GRID_WIDTH), dtype=int), 
                                 self.grid[:line], 
                                 self.grid[line+1:]))

    def update(self):
        """ゲーム状態を更新"""
        if self.game_over:
            return

        current_time = time.time()
        if current_time - self.last_fall_time > self.fall_speed:
            self.move_down()
            self.last_fall_time = current_time

    def get_grid_with_block(self):
        """現在のブロックを含むグリッドを返す"""
        grid = self.grid.copy()
        if self.current_block:
            for i in range(4):
                for j in range(4):
                    if self.current_block.shape[i][j]:
                        y = self.current_y + i
                        x = self.current_x + j
                        if 0 <= y < GRID_HEIGHT and 0 <= x < GRID_WIDTH:
                            grid[y][x] = self.current_block.color + 1
        return grid 