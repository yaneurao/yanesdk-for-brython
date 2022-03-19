from yanesdk import * # done by preprocessor

# ==============================================================================
#                         Game Main
# ==============================================================================

# 画像読み込み用
class ImageLoader:
    def __init__(self):
        # ゲームレバーの画像
        self.lever = Image("lever-s.png")

# GameSceneの基底クラス。これを派生させて、各シーンを作る。
class Scene:
    def onDraw(self, app:"TheApp"):
        pass

# ゲーム開始時のキー説明のScene
class GameOpeningScene(Scene):
    def onDraw(self, app:"TheApp"):
        canvas   = app.canvas
        keyinput = app.keyinput

        # ゲーム説明の表示
        canvas.clear()
        canvas.draw_text_center("Instruction",Vector2D(200,130))
        canvas.draw_text_center("Cursor Key to move",Vector2D(200,200),"28px serif")
        canvas.draw_text_center("Mouse Click or Tourch is also available",Vector2D(200,230),"20px serif")

        # 何かキーが押されたらゲーム開始
        keyinput.update()
        if keyinput.is_any_key_pressed():
            app.scene = GameMainScene()

# ゲームオーバー時のScene
class GameOverScene(Scene):
    def __init__(self):
        # 時間経過監視用のカウンター
        self._counter = 0

    def onDraw(self, app:"TheApp"):
        # 画面更新は不要
        self._counter += 1
        if self._counter > 3 * 15: # 3秒経過
            # オープニングのSceneへ
            app.scene = GameOpeningScene()

# ゲーム本体
class GameMainScene(Scene):
    def __init__(self):
        self.score = 0  # スコア

        # プレイヤーの座標
        self.p = Vector2D(10,10)
        # プレイヤーの移動方向(他のキーを押すまでずっとこの方向に移動)
        self.v = Vector2D(0,1)

        # 餌の座標
        self.a    = Vector2D(15,15)

        self.scale  = 20  # 1升の大きさ
        self.width  = 20  # フィールドの幅
        self.height = 20  # フィールドの高さ

        self.trail:list[Vector2D] = []  # 蛇の軌跡 (headから順番に座標が格納されている)
        self.tail = 3                   # 蛇の長さ

        # 画面上の一つのチップサイズ
        self.chip_size = Vector2D(self.scale - 2, self.scale - 2)


    def onDraw(self,app:"TheApp"):
        
        # aliases for app
        keyinput = app.keyinput
        math     = app.math
        canvas   = app.canvas
        images   = app.images

        # 画面クリア
        canvas.clear()

        # キーの更新
        keyinput.update()

        # マウス、タッチの補助線を描く
        canvas.draw_rectline(app.touch_rect.p , app.touch_rect.s, "#888")
        if keyinput.touch_pos:
            # タッチされているなら、レバーをその場所に描画する。
            canvas.draw_image_center(images.lever, keyinput.touch_pos)
        else:
            # タッチされていない場合、レバーをニュートラルの位置に描画する。
            canvas.draw_image_center(images.lever, app.touch_rect.p + app.touch_rect.s//2)

        # キー入力
        if   keyinput.is_key_pressed(VKEY.LEFT):   # 左
            self.v = Vector2D(-1, 0)
        elif keyinput.is_key_pressed(VKEY.RIGHT):  # 右
            self.v = Vector2D(+1, 0)
        elif keyinput.is_key_pressed(VKEY.UP):     # 上
            self.v = Vector2D( 0,-1)
        elif keyinput.is_key_pressed(VKEY.DOWN):   # 下
            self.v = Vector2D( 0,+1)
        # それ以外ならself.vを変化させない(慣性移動)
        
        # プレイヤーの移動
        self.p = self.p + self.v

        # 蛇は画面外にでれない(画面の上下、左右がつながっているとゲームが簡単になりすぎる)
        self.p = Vector2D(
            math.clamp(self.p.x  , 0, self.width  - 1),
            math.clamp(self.p.y  , 0, self.height - 1)
        )

        # プレイヤーの描画
        gameover = False
        for pos in self.trail:
            canvas.draw_rect( pos * self.scale, self.chip_size , "lime")

            # 胴体を頭が踏んづけている。
            # self.pは上で移動させたので1つ前の升に進んでいるはずだから、
            # trailの集合にその升があるなら踏んづけているということである。
            if pos == self.p:
                gameover = True

        # 蛇の頭の座標を軌跡の先頭に挿入
        self.trail.insert(0, self.p)

        # 蛇の胴体をtailの長さになるまで末尾を削除
        # (ゲーム開始時、胴体の長さが足りないので、こうしないといけない)
        while len(self.trail) > self.tail:
            self.trail.pop()

        # 蛇の頭が餌を取ったなら
        if self.a == self.p:
            # 胴体長さ + 1
            self.tail  += 1
            self.a = Vector2D(math.randint(self.width),math.randint(self.height))

        # 餌の描画
        canvas.draw_rect(self.a * self.scale , self.chip_size , "red")

        # スコアの加算、描画(尻尾の長さに応じたスコア加算)
        self.score += self.tail - 2
        canvas.draw_text(f"Score {self.score}",Vector2D(10,10))

        # ゲームオーバーになっていたら、それを表示。
        if gameover:
            canvas.draw_text("Game Over",Vector2D(50,170),"60px serif","red")
            # app.gametimer.stop()
            # app.keyinput.remove_event();
            app.scene = GameOverScene()


# === ゲーム初期化 ===

class TheApp:
    def __init__(self):

        # タッチ入力矩形
        self.touch_rect  = Rect(Vector2D(50,200),Vector2D(150,150))

        # キー入力用
        self.keyinput    = VirtualKeyInput()
        self.keyinput.configure_6keys_4directions_game(self.touch_rect)

        # 描画用スクリーン
        self.canvas      = Canvas()

        # 画像
        self.images      = ImageLoader()

        # 数学関連のツール
        self.math        = MathTools()

        # Scene
        self.scene:Scene = GameOpeningScene()

        # 描画のloop
        self.gametimer   = GameTimer(lambda : self.scene.onDraw(self) , 15)  # 15FPSでスタート

if __name__ == "__main__":
    try:
        # the singleton instance of TheApp
        TheApp()
    except:
        InfoDialog("Exception",traceback.format_exc())

