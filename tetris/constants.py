# 画面設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# テトリミノの色
COLORS = [
    CYAN,    # I
    YELLOW,  # O
    MAGENTA, # T
    GREEN,   # S
    RED,     # Z
    BLUE,    # J
    ORANGE   # L
]

# ゲーム設定
FPS = 60
INITIAL_FALL_SPEED = 0.5  # 秒
SPEED_INCREASE_PER_LEVEL = 0.05
LINES_PER_LEVEL = 10
MAX_LEVEL = 10  # 最大レベル

# スコア設定
SCORE_PER_LINE = 100
SCORE_MULTIPLIER = [1, 2, 3, 4]  # 1-4行消した時の倍率

# 音声設定
MUSIC_VOLUME = 0.5
BGM_FILE = r"C:\Users\mryo2\OneDrive\ドキュメント\python\person\project\tetris\tetris-theme-korobeiniki-arranged-for-piano-186249.mp3"

# ランキング設定
RANKING_FILE = "ranking.json"
MAX_RANKINGS = 10 