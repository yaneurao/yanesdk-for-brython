from yanesdk import *

# ==============================================================================
#                         Game Main
# ==============================================================================

class AUDIO(IntEnum):
    SUSHI  = 0 , # 寿司に当たった時のサウンド
    # GAME_OVER = 1 , # ゲームオーバーになった時のサウンド

# ↑のに対応する、読み込むオーディオファイル名(これはaudios/ に配置する)
AudioFileList = [
    "chime.mp3"   ,
    ]

ImageFileList = [
    "sushi_akami-s.png"   ,
    "sushi_ebi-s.png"     ,
    "sushi_hamachi-s.png" ,
    "sushi_harasu-s.png"  ,
    "sushi_kinmedai-s.png",
    "sushi_tamago-s.png"
    ]

# ゲームオブジェクトを表す定数
class GameObjectType(IntEnum):
    SUSHI           = 0 # 寿司
    BALL            = 1 # ボール
    BALL_TRAIL      = 2 # ボールの軌跡
    SUSHI_GENERATOR = 3 # 寿司の生成器
    PLAYER          = 4 # プレイヤー

# このゲームで使うGameObject
class MyGameObject(GameObject):
    def __init__(self, p:"Vector2D", type:GameObjectType):
        super().__init__()

        self.p    = p
        self.type = type

    def onDraw(self, app:"TheApp"): # type:ignore
        pass

# このゲームで使うGameObject
class SushiGenerator(MyGameObject):
    def __init__(self):
        super().__init__(Vector2D(), GameObjectType.SUSHI_GENERATOR)

        # カウンター
        self.count = 0

        # 次に出現させる寿司(0..5)
        self.sushi_no = 0

    def onDraw(self, app:"TheApp"):
        scene = cast(GameMainScene, app.scene)
        
        # 1秒ごとに寿司オブジェクト一つ追加。
        if self.count % 15 == 0:
            # 順番に出現させる
            p        = Vector2D(-30 , 60) # 画面左上からでてくる。
            scene.objects.append(Sushi(p, self.sushi_no))
            self.sushi_no = (self.sushi_no + 1) % 6

        self.count += 1

# 画面上に表示する寿司
class Sushi(MyGameObject):
    # sushi_no = 0..5 寿司の番号
    def __init__(self, p:"Vector2D", sushi_no:int):
        super().__init__(p, GameObjectType.SUSHI)
        self.sushi_no  = sushi_no

        # 寿司の移動方向(この変数を参照するごとに新しいベクトルを返す)
        self.sushi_mover = self.sushi_mover_iter()

    # 寿司の移動方向を返す。
    # 呼び出されるごとに次の移動ベクトルを返すようになっている。
    def sushi_mover_iter(self)->Generator[Vector2D, None, None]:
        for _ in range(10): yield Vector2D( 5,0) # 左上(画面外)から画面内へ
        while True:
            for _ in range(70): yield Vector2D( 5,0) # 右移動
            for _ in range(20): yield Vector2D( 0,3) # 下移動
            for _ in range(70): yield Vector2D(-5,0) # 左移動
            for _ in range(20): yield Vector2D( 5,3) # 下移動

    def onDraw(self, app:"TheApp"):
        canvas    = app.canvas
        images    = app.image_loader.images
        math      = app.math
        scene     = cast(GameMainScene, app.scene)

        # 寿司の移動方向。これは iterableで 1つずつ取り出される。
        v = next(self.sushi_mover)

        # 寿司の移動
        self.p = self.p + v

        # 画面外に行ったものも次フレームで削除
        if self.p.y >= canvas.height:
            self.deleted = True

        # ballとの接触判定
        # ballの座標
        ball = scene.ball
        if (ball.p - self.p).norm() <= 30:
            # 反射する。寿司の中心座標から、ボールの座標方向に跳ね返るものとする。
            ball.v = (ball.p - self.p + Vector2D(math.randint(-2,2),math.randint(-2,2))).unit(10)
            # この寿司、自爆する。
            self.deleted = True
            # スコア加算
            scene.score += 100
            # サウンドの再生
            app.audio_loader.audios[AUDIO.SUSHI].play()

        canvas.draw_image_center(images[self.sushi_no], self.p)


# 画面上に表示するボール
class Ball(MyGameObject):
    # p : 座標
    # v : 速度
    def __init__(self, p:"Vector2D", v:"Vector2D"):
        super().__init__(p, GameObjectType.BALL)
        self.v         = v
        self.ball_size = Vector2D(20,20)

    def onDraw(self, app:"TheApp"):
        canvas  = app.canvas
        scene   = cast(GameMainScene, app.scene)

        # 移動
        self.p += self.v

        # 壁に反射
        if self.p.x >= canvas.width:
            self.v = Vector2D(-abs(self.v.x) ,  self.v.y)
        if self.p.x < 0:
            self.v = Vector2D( abs(self.v.x) ,  self.v.y)
        if self.p.y < 0:
            self.v = Vector2D( self.v.x      , abs(self.v.y))

        # プレイヤーの座標
        player = scene.player.p

        # プレイヤー(pad)に反射する
        if player.x - 25 < self.p.x <= player.x + 50 and \
           player.y - 10 < self.p.y <= player.y + 10 :
            # 反射する X方向は、Padの当たった部分に応じる。
            # -25..25の間
            vx     = (self.p.x - player.x) * 10 / 25
            self.v = Vector2D(vx, -abs(self.v.y))

        canvas.draw_rect_center(self.p, self.ball_size,"blue")

        # 痕跡オブジェクトの生成
        # 現在のボールの座標に出現。
        scene.objects.append(BallTrail(self.p))


# ボールの軌跡
class BallTrail(MyGameObject):
    def __init__(self, p:"Vector2D"):
        super().__init__(p, GameObjectType.BALL_TRAIL)

        self.ball_size = Vector2D(20,20)

        # 5フレーム程度で消滅すればいいと思う。
        # そのためのcounter
        self.counter = 0

    def onDraw(self, app:"TheApp"):
        canvas = app.canvas

        # 徐々に薄くなる
        b = 128*(5 - self.counter) // 5

        color = canvas.make_color(0, 0, b)
        canvas.draw_rect_center(self.p, self.ball_size,color)

        self.counter += 1
        if self.counter >= 5:
            self.deleted = True
            return

# プレイヤー
class Player(MyGameObject):
    def __init__(self, p:"Vector2D"):
        super().__init__(p, GameObjectType.PLAYER)

    def onDraw(self, app:"TheApp"):
        # alias for app
        canvas    = app.canvas
        keyinput  = app.keyinput
        math      = app.math

        # キーに応じた移動
        vx = 0
        keyinput.update()
        if   keyinput.is_key_pressed(VKEY.LEFT ):
            vx = -20
        elif keyinput.is_key_pressed(VKEY.RIGHT):
            vx = +20
        
        # プレイヤーの移動
        self.p = Vector2D(math.clamp(self.p.x + vx , 0, canvas.width) , self.p.y )

        # プレイヤーの描画
        canvas.draw_rect_center(self.p , Vector2D(50,20),"green")


# Scene基底class
class Scene:
    def onDraw(self, app:"TheApp"):
        pass

# ゲーム開始時のキー説明のScene
class GameOpeningScene(Scene):
    def onDraw(self, app:"TheApp"):
        canvas = app.canvas
        image_loader = app.image_loader

        # ゲーム説明の表示
        canvas.clear()
        canvas.draw_text_center("Instruction",Vector2D(200,130))
        canvas.draw_text_center("Right/Left Cursor Key to move",Vector2D(200,200),"25px serif")
        canvas.draw_text_center("Mouse Right and Left Button",Vector2D(200,240),"20px serif")
        canvas.draw_text_center(" or Touch Right/Left side is also available",Vector2D(200,270),"20px serif")

        # 読み込みが完了している画像の数
        canvas.draw_text_center(f"loading images .. {image_loader.completed_num()}/{len(image_loader.images)}",
            Vector2D(200,340),"20px serif")

        # 画像の読み込みが完了していて、かつ、何かキーが押されたらゲーム開始
        app.keyinput.update()
        if app.keyinput.is_any_key_pressed() and image_loader.load_completed():
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

        self.score = 0  # ゲームスコア

        # ゲーム上の物体
        self.objects = GameObjectManager()

        # プレイヤー
        # 外部から参照したいのでメンバとしても持たせておく。
        self.player = Player(Vector2D(200,380))
        self.objects.append(self.player)

        # 寿司の生成器を追加
        self.objects.append(SushiGenerator())

        self.ball = Ball(Vector2D(200,360) , Vector2D(1,-2).unit(10))

        # ゲームのスコア
        self.score = 0

    def onDraw(self,app:"TheApp"):

        # alias for app
        canvas    = app.canvas

        # canvas丸ごと塗りつぶし
        color  = canvas.make_color(0,0,40)
        canvas.clear(color)

        # ゲームオブジェクトの描画
        self.objects.onDraw(app)

        # ballの描画
        self.ball.onDraw(app)

        # スコアの加算、描画
        self.score += 1
        app.canvas.draw_text(f"Score {self.score}",Vector2D(5,5))

        # 画面下までボールが移動したらゲームオーバー
        if self.ball.p.y >= canvas.height:
            # ゲームオーバーになっていたら、それを表示。
            canvas.draw_text("Game Over",Vector2D(50,170),"60px serif","red")

            # ゲームオーバー画面に移動
            app.scene = GameOverScene()

# ==============================================================================
#                         The App
# ==============================================================================

class TheApp(GameContext):
    def __init__(self):

        # Sceneクラスのインスタンスを生成
        self.scene:Scene  = GameOpeningScene()

        # キー入力用(左右)
        self.keyinput     = VirtualKeyInput()
        self.keyinput.configure_4keys_2directions_game()

        # 描画用スクリーン
        self.canvas       = Canvas("canvas")

        # 画像loader
        self.image_loader = ImageLoader(ImageFileList)

        # 数学関連のツール
        self.math         = MathTools()

        # 音声ファイル
        self.audio_loader = AudioLoader(AudioFileList)

        # 描画のloop
        self.gametimer    = GameTimer(lambda : self.scene.onDraw(self) , 15)  # 15FPSでスタート

# the singleton instance of The App
TheApp()
