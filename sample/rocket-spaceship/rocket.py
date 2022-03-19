from yanesdk import * # done by preprocessor

# ==============================================================================
#                         Game Main
# ==============================================================================

class AUDIO(IntEnum):
    POWER_UP  = 0 , # パワーアップした時のサウンド
    GAME_OVER = 1 , # ゲームオーバーになった時のサウンド

# ↑のに対応する、読み込むオーディオファイル名(これはaudios/ に配置する)
AudioFileList = [
    "chime.mp3",
    "gameover.mp3"
    ]

# ゲームオブジェクトを表す定数
class GameObjectType(IntEnum):
    WALL         = 0 # 壁
    POWERUP      = 1 # パワーアップ
    PLAYER_TRAIL = 2 # プレイヤーの軌跡

# ゲームに出てくる物体(プレイヤーの軌跡、壁など)
class MyGameObject:

    # p : Vector2D , 座標
    # t = WALL or POWERUP or PLAYER
    def __init__(self,p:Vector2D,type:GameObjectType):

        # これをTrueにすると次の描画frameで削除される。
        self.deleted = False

        # オブジェクトの座標
        self.p = p

        # オブジェクト種別
        self.type = type

# Scene基底class
class Scene:
    def onDraw(self, app:"TheApp"):
        pass

# ゲーム開始時のキー説明のScene
class GameOpeningScene(Scene):
    def onDraw(self, app:"TheApp"):
        canvas = app.canvas
        # ゲーム説明の表示
        canvas.clear()
        canvas.draw_text_center("Instruction",Vector2D(200,130))
        canvas.draw_text_center("Space Key to hover",Vector2D(200,200),"28px serif")
        canvas.draw_text_center("Mouse Click or Touch is also available",Vector2D(200,240),"20px serif")

        # スペースキー相当のキーが押されたらゲーム開始
        app.keyinput.update()
        if app.keyinput.is_key_pressed(VKEY.SPACE):
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

        # プレイヤーの座標        : position of the player
        self.p  = Vector2D(40,200)
        # プレイヤーの移動方向    : velocity of the player
        self.v  = Vector2D()
        #  プレイヤーの加速度方向 : acceleration of the player
        self.a  = Vector2D(0,1)  

        # 現在の壁(がない部分の)の座標とその高さ
        self.wall_y      = 200
        self.wall_height = 200

        # ゲーム上の物体
        self.objects:list[MyGameObject] = []

        # プレイヤー画像
        self.spaceship = Image("space_rocket_kids-small.png")

    def onDraw(self,app:"TheApp"):

        # alias for app
        canvas    = app.canvas
        keyinput  = app.keyinput
        math      = app.math

        # ゲームオーバーになったかのフラグ       
        gameover = False

        # キーに応じた移動
        keyinput.update()
        if keyinput.is_key_pressed(VKEY.SPACE):
            self.a = Vector2D(0, -1)
        else:
            self.a = Vector2D(0, +1)

        # スクリーンのサイズ
        (width,height) = (canvas.width,canvas.height)

        # プレイヤーの移動
        self.v += self.a
        self.p += self.v
        if not 0 <= self.p.y < height:
            gameover = True

        # canvas丸ごと塗りつぶし
        canvas.clear()

        # 物体のスクロール
        self.objects = [MyGameObject(Vector2D(obj.p.x - 20, obj.p.y), obj.type) for obj in self.objects if obj.p.x > 0 and not obj.deleted]

        # 壁の生成

        self.wall_y      += math.randint(-10,10)
        self.wall_y       = math.clamp(self.wall_y, 30, 370)
        self.wall_height += math.randint(-10,10) # 壁の幅、ちょっと変わる
        self.wall_height  = math.clamp(self.wall_height, 80, 200)

        # 壁の範囲は区間[y1,y2]
        y1 = self.wall_y - self.wall_height // 2
        y2 = self.wall_y + self.wall_height // 2
        for y in range(int(y1) % 20 - 20, height + 20, 20):
            if y1 <= y <= y2:
                continue
            self.objects.append(MyGameObject(Vector2D(width, y), GameObjectType.WALL))

        # 種の生成
        # 1/20の確率で生成
        if math.randint(20) == 0:
            self.objects.append(MyGameObject(Vector2D(width, self.wall_y), GameObjectType.POWERUP))

        # 障害物・種の表示
        for obj in self.objects:

            color = ("purple", "red", "green")[obj.type]
            canvas.draw_rect_center(obj.p , Vector2D(20, 20) , color)

            # プレイヤーとの衝突判定
            # 2点間の距離が20以内
            if (obj.p - self.p).norm() <= 20:
                if obj.type == GameObjectType.WALL:
                    gameover = True
                elif obj.type == GameObjectType.POWERUP:
                    self.objects.append(MyGameObject(self.p, GameObjectType.PLAYER_TRAIL))  # 自分の痕跡
                    # 種を取ったので少し前へ
                    self.p = Vector2D( min(self.p.x + 10, 300), self.p.y)
                    app.audio_loader.audios[AUDIO.POWER_UP].play()
                    # このオブジェクト、次のframeで削除する。
                    obj.deleted = True

        # プレイヤーの描画
        canvas.draw_image_center(self.spaceship, self.p)
        self.objects.append(MyGameObject(self.p, GameObjectType.PLAYER_TRAIL))  # 自分の痕跡

        # スコアの加算、描画
        self.score += (self.p.x-30)//10 # 前に出ているほどスコアたくさん入る。
        canvas.draw_text(f"Score {self.score}",Vector2D(10,10),color = "white")

        # ゲームオーバーになっていたら、それを表示。
        if gameover:
            app.audio_loader.audios[AUDIO.GAME_OVER].play() # 爆発音
            canvas.draw_text_center("Game Over",Vector2D(200,170),"60px serif","red")

            # 終了させるなら、こう。
            # app.gametimer.stop()
            # app.keyinput.remove_event();

            # ゲームオーバー画面に移動
            app.scene = GameOverScene()

# ==============================================================================
#                         The App
# ==============================================================================

class TheApp:
    def __init__(self):

        # Sceneクラスのインスタンスを生成
        self.scene:Scene  = GameOpeningScene()

        # キー入力用(スペースキー、マウスクリック、タッチイベントどれでもOK)
        self.keyinput     = VirtualKeyInput()
        self.keyinput.configure_1key_game()

        # 描画用スクリーン
        self.canvas       = Canvas("canvas")

        # 数学関連のツール
        self.math         = MathTools()

        # 音声ファイル
        self.audio_loader = AudioLoader(AudioFileList)

        # 描画のloop
        self.gametimer    = GameTimer(lambda : self.scene.onDraw(self) , 15)  # 15FPSでスタート

if __name__ == "__main__":
    try:
        # the singleton instance of TheApp
        TheApp()
    except:
        InfoDialog("Exception",traceback.format_exc())
