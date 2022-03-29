from yanesdk import *

# ==============================================================================
#                         Life Game main
# ==============================================================================

class LifeGame:
    def __init__(self):
        # 400px*400pxなので10pxずつ区切って40升四方とみなす。
        self.width     = 40
        self.height    = 40
        self.chip_size = 10

        self.field      = self.cleared_field()
        # 毎回クリアするのもったいないので、1つ前のと入れ替えて使う。
        self.field_last = self.cleared_field()

        # 生きてるセルを画面中央に置く
        def pset(x:int,y:int):
            self.field[self.height//2 + y][self.width//2 + x] = 1

        # F pentomino
        pset( 0, 0)
        pset( 1, 0)
        pset( 0, 1)
        pset(-1, 1)
        pset( 0, 2)

        # 世代番号
        self.generation = 0

    # 空のfieldを返す
    # サイズは(width , height)
    def cleared_field(self)->list[list[int]]:
        return [[0]*self.width for _ in range(self.height)]

    # 1世代進める
    def do_next_generation(self):
        # b = 1世代前の状態 , a = 次に更新すべき状態
        a = self.field_last
        b = self.field

        for y in range(self.height):
            for x in range(self.width):
                # この周辺の升の生きているセルの数をカウントする
                s = 0
                for vy in range(-1,2):
                    for vx in range(-1,2):
                        if vx == 0 and vy == 0:
                            continue
                        x2 = x + vx
                        y2 = y + vy
                        if not( 0 <= x2 < self.width and 0 <= y2 < self.height):
                            continue
                        s += 1 if b[y2][x2] else 0

                if b[y][x]:
                    a[y][x] = b[y][x] + 1 if s == 2 or s == 3 else 0
                    # 前回の値 + 1して、長生きしていると徐々に増える感じにしておく。
                else:
                    a[y][x] = 1 if s == 3 else 0

        self.field      = a
        self.field_last = b

    def onDraw(self,app:"TheApp"):
        # alias for app
        canvas = app.canvas

        # 画面クリア
        canvas.clear()

        # fieldの描画
        c = self.chip_size
        for y in range(self.height):
            for x in range(self.width):
                n = self.field[y][x]
                if n:
                    # b : brightness 明るさ(0-255)
                    # b = int(MathTools.min(n,7)*127// 7) + 128
                    # color = canvas.make_color(b,b,b)
                    # →　モノクロ、ダサい？
                    color = ["#000","#008","#080","#088","#800","#808","#888","#FFF"][min(n,7)]
                    canvas.draw_rect(Vector2D(x*c,y*c),Vector2D(c-1,c-1),color)
                # if n:
                #     canvas.draw_rect(Vector2D(x*c,y*c),Vector2D(c-1,c-1),"white")

        canvas.draw_text(f"Generation {self.generation}",Vector2D(10,10))
        self.generation += 1

        # 1世代進める        
        self.do_next_generation()

# ==============================================================================
#                         The App
# ==============================================================================

class TheApp:
    def __init__(self):

        # 描画用スクリーン
        self.canvas    = Canvas("canvas")

        # Life Game本体
        self.lifegame  = LifeGame()

        # 描画のloop
        self.gametimer = GameTimer( lambda : self.lifegame.onDraw(self) ,15)  # 15FPSでスタート
        
# the singleton instance of TheApp
TheApp()
