from yanesdk import *

# ==============================================================================
#                         Mandelbrot set
# ==============================================================================

class TheApp:
    def __init__(self):
        # 描画用スクリーン
        self.canvas = Canvas("canvas")
        self.canvas.clear("black")

        # 繰り返す回数の上限
        self.n_max  = 100

        # ひとつの点のサイズ
        self.scale  = 1
        self.chip   = Vector2D(self.scale,self.scale)

        # canvasのサイズ
        self.width  = 400 // self.scale
        self.height = 400 // self.scale

        # マンデルブロー集合の描画範囲
        self.rect = Rect(Vector2D(-1.5 , -1.25) , Vector2D(2.5, 2.5))

        # 描画中のy座標
        self.y = 0

        # 描画できる限り速く描画して欲しいのでfps = 1000にしておく。
        self.game_timer = GameTimer(self.onDraw, 1000)

    # 呼び出すごとに1行ずつ描画
    def onDraw(self):
        # yは呼び出されるごとに1行ずつ描画したいため、
        # メンバ変数にもたせておく。
        if self.y >= self.height:
            self.game_timer.stop()
            return
        y = self.y
        self.y += 1 # 忘れないうちに次回呼び出し時のためにインクリメントしておく。

        for x in range(self.width):
            # ループ変数をマンデルブロー集合の座標系に変換
            # y方向が虚数部。虚数単位をjとすると、
            # c = cx + cy*j
            r = self.rect
            cx = x * r.s.x /self.width  + r.p.x
            cy = y * r.s.y /self.height + r.p.y

            # z = zx + zy*j
            zx = 0.0
            zy = 0.0

            # z(n+1) = z(n)**2 + c
            # z(0)   = 0
            # なる複素数列を考える。
            # n → ∞ で ∞ に発散しないという条件を満たす複素数c全体が作る集合をplot。
            # ↓のloopで何回目のnで発散する(1e10より大きくなる)かを調べてそれをplotしていく。

            n = 0
            while n < self.n_max and zx ** 2 + zy ** 2 < 1e10:
                # z(n+1) = z(n)**2 + c = (zx + zy*j)^2 + cx + cy*j = (zx**2 - zy**2 + cx ) + (2*zx*zy + cy)*j
                (zx,zy) = (zx ** 2 - zy ** 2 + cx ,  2 * zx * zy + cy)
                n += 1

            # b : brightness == 塗りつぶしの明るさ(0-255)
            b     = int(n * 2.55)
            color = Canvas.make_color(b,b,b)
            self.canvas.draw_rect(Vector2D(x,y) * self.scale , self.chip , color)


# singleton instance of TheApp
TheApp()
