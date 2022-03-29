from yanesdk import *

# ==============================================================================
#                         Game Main
# ==============================================================================

# Game enum
class GameObjectType(IntEnum):
    WALL         = 0 # 壁
    SPEED_UP     = 1 # 取るとスピード上がる種
    PLAYER_TRAIL = 2 # プレイヤーの軌跡

# プレイヤー以外の物体
class MyGameObject:
    def __init__(self, p:Vector2D, type:GameObjectType):
        # これをTrueにすると次の描画frameで削除される。
        self.deleted = False

        # 座標
        self.p       = p

        # オブジェクトの種別
        self.type    = type

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
        canvas.draw_text_center("Cursor Right/Left to move",Vector2D(200,200),"20px serif")
        canvas.draw_text_center("Mouse Right/Left Click or ",Vector2D(200,240),"20px serif")
        canvas.draw_text_center("Touch Right/Left screen is also available",Vector2D(200,260),"20px serif")

        # 何かキーが押されたらゲーム開始
        app.keyinput.update()
        if app.keyinput.is_any_key_pressed():
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
        self.p = Vector2D(10,3)

        self.scale  = 20  # 1升の大きさ
        self.width  = 20  # フィールドの幅
        self.height = 20  # フィールドの高さ

        # 画面上の一つのチップサイズ
        self.chip_size = Vector2D(self.scale - 2, self.scale - 2)

        # 画面上のオブジェクト(プレイヤーを除く)
        self.objects : list[MyGameObject] = []

    def onDraw(self,app:"TheApp"):
        
        # aliases for app
        keyinput = app.keyinput
        math     = app.math
        canvas   = app.canvas

        # キー入力
        keyinput.update()
        if keyinput.is_key_pressed(VKEY.LEFT):  # 左
            vx = -1
        elif keyinput.is_key_pressed(VKEY.RIGHT):  # 右
            vx = 1
        else:
            vx = 0

        # プレイヤーの移動
        self.p = Vector2D(math.clamp(self.p.x + vx , 0, self.width -1) , self.p.y)

        # 画面クリア
        canvas.clear()

        # プレイヤーの描画
        canvas.draw_rect( self.p * self.scale , self.chip_size , "lime")

        # スキーの痕跡を追加する。
        self.objects.append(MyGameObject(self.p, GameObjectType.PLAYER_TRAIL)) 

        # 物体のスクロール
        self.objects = [MyGameObject(Vector2D(obj.p.x, obj.p.y - 1) , obj.type) for obj in self.objects if obj.p.y > 0 and not obj.deleted]

        # 障害物・種の生成
        obj_x    = math.randint(self.width)
        obj_type = GameObjectType(math.randint(2))  # 障害物か種かをどちらかをランダムに
        self.objects.append(MyGameObject(Vector2D(obj_x, self.height - 1), obj_type))

        # プレイヤーの1つ前の升(当たり判定はここにある)
        player = Vector2D(self.p.x , self.p.y + 1)

        # 障害物・種の表示
        gameover = False

        # for obj in self.objects:
        # → ループのなかでappendしたいのでwhileで書き直す。

        # listに対してforで回している時のappend、Pythonでは現状問題がないのだが、将来的に
        # 変わりうると思うので、この仕様には依存した書き方をすべきではないと思う。
        # 備考)  https://dev.classmethod.jp/articles/python-delete-element-of-list/

        i = 0
        while i < len(self.objects):
            obj = self.objects[i]
            i += 1

            # 障害物
            color = ("white", "red", "green")[obj.type]
            canvas.draw_rect( obj.p * self.scale, self.chip_size, color )

            # プレイヤーとの衝突判定
            if obj.p == player:
                if obj.type == GameObjectType.WALL:
                    gameover = True
                elif obj.type == GameObjectType.SPEED_UP:   # ひとつ前へ

                    # 前に移動するので現在地点にスキーの痕跡を追加する。
                    self.objects.append(MyGameObject(self.p, GameObjectType.PLAYER_TRAIL)) 

                    self.p      = Vector2D(self.p.x , min(self.p.y + 1, 15))
                    obj.deleted = True # 次の描画frameで削除する。(実際はプレイヤーの痕跡に重なって見えないが)

        # スコアの加算、描画
        # 前に出ているほどスコアが高くなる。
        self.score += (self.p.y - 2)
        canvas.draw_text("Score " + str(self.score),Vector2D(10,5))

        # ゲームオーバーになっていたら、それを表示。
        if gameover:
            canvas.draw_text_center("Game Over",Vector2D(200,170),"60px serif",color = "Red")
            # app.gametimer.stop()
            # app.keyinput.remove_event()
            app.scene = GameOverScene()

# === ゲーム初期化 ===

class TheApp(GameContext):
    def __init__(self):

        # キー入力用
        self.keyinput  = VirtualKeyInput()
        self.keyinput.configure_4keys_2directions_game()

        # 描画用スクリーン
        self.canvas      = Canvas()

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
