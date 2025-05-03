import pygame
import sys
import time
import json
import os
from tetris import Tetris
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, GRID_SIZE,
    GRID_WIDTH, GRID_HEIGHT, COLORS,
    BLACK, WHITE, GRAY, CYAN, MUSIC_VOLUME, BGM_FILE,
    MAX_LEVEL, FPS, RANKING_FILE, MAX_RANKINGS
)

class TetrisGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('Tetris')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.game = None
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 48)
        self.paused = False
        self.game_over = False
        self.selected_level = 1
        self.show_level_select = True
        self.show_ranking = False
        self.rankings = self.load_rankings()
        
        # キー長押し用の変数
        self.key_delays = {
            pygame.K_LEFT: 0,
            pygame.K_RIGHT: 0,
            pygame.K_DOWN: 0
        }
        self.key_hold_times = {
            pygame.K_LEFT: 0,
            pygame.K_RIGHT: 0,
            pygame.K_DOWN: 0
        }
        # キー長押しの速度設定
        self.key_speeds = {
            'initial': 0.2,    # 最初の移動までの遅延（秒）
            'normal': 0.1,     # 通常の移動間隔（秒）
            'fast': 0.05,      # 高速移動間隔（秒）
            'turbo': 0.02      # 超高速移動間隔（秒）
        }
        self.speed_thresholds = {
            'fast': 0.5,       # 高速モードに移行するまでの時間（秒）
            'turbo': 1.0       # 超高速モードに移行するまでの時間（秒）
        }
        
        # BGMの設定
        pygame.mixer.music.load(BGM_FILE)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)  # -1でループ再生

    def load_rankings(self):
        """ランキングデータを読み込む"""
        if os.path.exists(RANKING_FILE):
            try:
                with open(RANKING_FILE, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_rankings(self):
        """ランキングデータを保存する"""
        with open(RANKING_FILE, 'w') as f:
            json.dump(self.rankings, f)

    def add_ranking(self, score, level):
        """新しいスコアをランキングに追加"""
        self.rankings.append({
            'score': score,
            'level': level,
            'date': time.strftime('%Y-%m-%d %H:%M:%S')
        })
        # スコアの高い順にソート
        self.rankings.sort(key=lambda x: x['score'], reverse=True)
        # 最大ランキング数を超えた分を削除
        if len(self.rankings) > MAX_RANKINGS:
            self.rankings = self.rankings[:MAX_RANKINGS]
        self.save_rankings()

    def draw_ranking(self):
        """ランキング画面を描画"""
        self.screen.fill(BLACK)
        
        # タイトル
        title = self.big_font.render("HIGH SCORES", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
        self.screen.blit(title, title_rect)
        
        # ランキング表示
        y = 120
        for i, ranking in enumerate(self.rankings):
            rank_text = f"{i+1}. {ranking['score']} (Level {ranking['level']}) - {ranking['date']}"
            text = self.font.render(rank_text, True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH//2 - 200, y))
            y += 40
        
        # 戻るボタン
        back_text = self.font.render("Press ESC to return to menu", True, WHITE)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        self.screen.blit(back_text, back_rect)

    def handle_ranking_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.show_ranking = False
                    self.show_level_select = True

    def draw_level_select(self):
        self.screen.fill(BLACK)
        
        # タイトル
        title = self.big_font.render("TETRIS", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # レベル選択の説明
        instruction = self.font.render("Select Level (1-10)", True, WHITE)
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(instruction, instruction_rect)
        
        # 現在選択中のレベル
        level_text = self.big_font.render(f"Level: {self.selected_level}", True, CYAN)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH//2, 300))
        self.screen.blit(level_text, level_rect)
        
        # 操作方法
        controls = self.font.render("Up/Down: Change Level  Enter: Start", True, WHITE)
        controls_rect = controls.get_rect(center=(SCREEN_WIDTH//2, 400))
        self.screen.blit(controls, controls_rect)
        
        # ランキング表示ボタン
        ranking_text = self.font.render("Press H to view High Scores", True, WHITE)
        ranking_rect = ranking_text.get_rect(center=(SCREEN_WIDTH//2, 450))
        self.screen.blit(ranking_text, ranking_rect)

    def handle_level_select_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_level = min(self.selected_level + 1, MAX_LEVEL)
                elif event.key == pygame.K_DOWN:
                    self.selected_level = max(self.selected_level - 1, 1)
                elif event.key == pygame.K_RETURN:
                    self.game = Tetris(self.selected_level)
                    self.game.on_new_block = self.reset_key_hold_times
                    self.show_level_select = False
                elif event.key == pygame.K_h:
                    self.show_ranking = True
                    self.show_level_select = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def draw_grid(self):
        # グリッドの描画
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, GRAY, 
                               (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                if self.game.grid[y][x] != 0:
                    pygame.draw.rect(self.screen, COLORS[self.game.grid[y][x] - 1],
                                   (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def draw_block(self, block, x, y):
        for i in range(4):
            for j in range(4):
                if block.shape[i][j]:
                    pygame.draw.rect(self.screen, COLORS[block.color],
                                   ((x + j) * GRID_SIZE, (y + i) * GRID_SIZE, GRID_SIZE, GRID_SIZE))

    def draw_next_block(self):
        # 次のブロックの表示
        next_text = self.font.render("Next:", True, WHITE)
        self.screen.blit(next_text, (GRID_WIDTH * GRID_SIZE + 20, 20))
        
        if self.game.next_block:
            self.draw_block(self.game.next_block, GRID_WIDTH + 1, 2)

    def draw_score(self):
        # スコアの表示
        score_text = self.font.render(f"Score: {self.game.score}", True, WHITE)
        self.screen.blit(score_text, (GRID_WIDTH * GRID_SIZE + 20, 150))
        
        # レベルの表示
        level_text = self.font.render(f"Level: {self.game.level}", True, WHITE)
        self.screen.blit(level_text, (GRID_WIDTH * GRID_SIZE + 20, 200))
        
        # 消した行数の表示
        lines_text = self.font.render(f"Lines: {self.game.lines_cleared}", True, WHITE)
        self.screen.blit(lines_text, (GRID_WIDTH * GRID_SIZE + 20, 250))

    def draw_game_over(self):
        # ゲームオーバー画面
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.big_font.render("GAME OVER", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        score_text = self.font.render(f"Final Score: {self.game.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(score_text, score_rect)
        
        restart_text = self.font.render("Press R to Restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        self.screen.blit(restart_text, restart_rect)
        
        ranking_text = self.font.render("Press H to view High Scores", True, WHITE)
        ranking_rect = ranking_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 150))
        self.screen.blit(ranking_text, ranking_rect)

    def draw_pause(self):
        # ポーズ画面
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        pause_text = self.big_font.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(pause_text, pause_rect)

    def reset_key_hold_times(self):
        """キーの長押し時間をリセット"""
        current_time = time.time()
        for key in self.key_hold_times:
            self.key_hold_times[key] = 0
            self.key_delays[key] = current_time + self.key_speeds['initial']

    def get_key_speed(self, key):
        hold_time = self.key_hold_times[key]
        if hold_time >= self.speed_thresholds['turbo']:
            return self.key_speeds['turbo']
        elif hold_time >= self.speed_thresholds['fast']:
            return self.key_speeds['fast']
        else:
            return self.key_speeds['normal']

    def handle_key_repeat(self, current_time):
        keys = pygame.key.get_pressed()
        
        # 左右移動
        if keys[pygame.K_LEFT]:
            if current_time >= self.key_delays[pygame.K_LEFT]:
                self.game.move_left()
                self.key_delays[pygame.K_LEFT] = current_time + self.get_key_speed(pygame.K_LEFT)
                self.key_hold_times[pygame.K_LEFT] += 1/FPS
        else:
            self.key_delays[pygame.K_LEFT] = 0
            self.key_hold_times[pygame.K_LEFT] = 0
            
        if keys[pygame.K_RIGHT]:
            if current_time >= self.key_delays[pygame.K_RIGHT]:
                self.game.move_right()
                self.key_delays[pygame.K_RIGHT] = current_time + self.get_key_speed(pygame.K_RIGHT)
                self.key_hold_times[pygame.K_RIGHT] += 1/FPS
        else:
            self.key_delays[pygame.K_RIGHT] = 0
            self.key_hold_times[pygame.K_RIGHT] = 0
            
        # 下移動（加速落下）
        if keys[pygame.K_DOWN]:
            if current_time >= self.key_delays[pygame.K_DOWN]:
                self.game.move_down()
                self.key_delays[pygame.K_DOWN] = current_time + self.get_key_speed(pygame.K_DOWN)
                self.key_hold_times[pygame.K_DOWN] += 1/FPS
        else:
            self.key_delays[pygame.K_DOWN] = 0
            self.key_hold_times[pygame.K_DOWN] = 0

    def handle_events(self):
        current_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                    if self.paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                elif event.key == pygame.K_r and self.game_over:
                    self.game = Tetris(self.selected_level)
                    self.game_over = False
                    pygame.mixer.music.play(-1)
                elif event.key == pygame.K_h and self.game_over:
                    self.show_ranking = True
                    self.game_over = False
                elif not self.paused and not self.game_over:
                    if event.key == pygame.K_UP:
                        self.game.rotate()
                    elif event.key == pygame.K_SPACE:
                        self.game.hard_drop()
        
        # キー長押しの処理
        if not self.paused and not self.game_over:
            self.handle_key_repeat(current_time)

    def run(self):
        while True:
            if self.show_ranking:
                self.handle_ranking_events()
                self.draw_ranking()
            elif self.show_level_select:
                self.handle_level_select_events()
                self.draw_level_select()
            else:
                self.handle_events()
                
                if not self.paused and not self.game_over:
                    self.game.update()
                    if self.game.game_over:
                        self.game_over = True
                        self.add_ranking(self.game.score, self.game.level)
                        pygame.mixer.music.stop()
                
                self.screen.fill(BLACK)
                self.draw_grid()
                if self.game.current_block:
                    self.draw_block(self.game.current_block, self.game.current_x, self.game.current_y)
                self.draw_next_block()
                self.draw_score()
                
                if self.game_over:
                    self.draw_game_over()
                elif self.paused:
                    self.draw_pause()
                
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = TetrisGame()
    game.run() 