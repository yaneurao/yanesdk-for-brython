from yanesdk import *

# ==============================================================================
#                         Game Main
# ==============================================================================

class AUDIO(IntEnum):
    GAME_OVER = 0, # ゲームオーバー時の効果音

# ↑の定義に対応する実際のオーディオファイル。
audio_file_list = [
    "gameover.mp3",
    ]

# 弾の種類
class BulletColor(IntEnum):
    YELLOW = 0,
    RED    = 1

# GameObjectの基底クラス
class MyGameObject(GameObject):
    def onDraw(self, app:"TheApp"): #type:ignore
        pass   

# ゲームに出てくる弾
class Bullet(MyGameObject):
    # p : オブジェクトの座標
    # v : オブジェクトの移動方向
    # t : 0 = 黄 , 1 = 赤
    def __init__(self, p:Vector2D , v:Vector2D , c:BulletColor):

        super().__init__()

        # オブジェクトの座標と移動方向
        self.p = p
        self.v = v

        # 弾の色
        self.color = c

    def onDraw(self,app:"TheApp"):

        # aliases
        canvas = app.canvas 
        if self.color == BulletColor.YELLOW:
            img    = app.images.bullet0
        elif self.color == BulletColor.RED:
            img    = app.images.bullet1
        else: raise

        # 移動
        self.p += self.v

        # 画面範囲外に出たものはdelete markをつけておく。
        self.deleted = not self.p.is_in_rect(canvas.rect)

        # 描画
        canvas.draw_image_center(img, self.p)

# 少年
class Boy(MyGameObject):
    def __init__(self):

        super().__init__()

        # 移動カウンター(これに従って適当に移動)
        self.counter = 0

    def onDraw(self,app:"TheApp"):

        # aliases
        canvas  = app.canvas 
        math    = app.math
        img     = app.images.boy

        scene   = cast(GameMainScene , app.scene)
        player  = scene.player.p
        bullets = scene.bullets

        # 移動
        x = 700 + math.sin_deg(self.counter *  4) * 100
        y = 200 + math.cos_deg(self.counter *  2) * 200
        self.p = Vector2D(x,y)
        self.counter += 1

        # 1/120の確率で弾を生成
        if math.randint(120) == 0:
            # プレイヤーの周囲をめがけて発射。速度6
            v = (player - self.p + Vector2D(math.randint(-100,100),math.randint(-100,100))).unit(6)
            bullets.append(Bullet(self.p,v,BulletColor.RED))

        # 描画
        canvas.draw_image_center(img, self.p)

# 少女
class Girl(MyGameObject):
    def __init__(self):

        super().__init__()

        # 移動カウンター(これに従って適当に移動)
        self.counter = 0

    def onDraw(self,app:"TheApp"):

        # aliases
        canvas  = app.canvas 
        math    = app.math
        img     = app.images.girl

        scene = cast(GameMainScene, app.scene)
        player  = scene.player.p
        bullets = scene.bullets

        # 移動
        x = 700 + math.sin_deg(self.counter *  3) * 100
        y = 200 + math.cos_deg(self.counter *  1) * 200
        self.p = Vector2D(x,y)
        self.counter += 1

        # 1/60の確率で弾を生成
        if math.randint(60) == 0:
            # プレイヤーめがけて発射。速度3
            v = (player - self.p).unit(3)
            bullets.append(Bullet(self.p, v, BulletColor.YELLOW))

        # 描画
        canvas.draw_image_center(img, self.p)

# ゲームプレイヤー(GameObjectとしての)
class GamePlayer(MyGameObject):
    def __init__(self):
        super().__init__()
        self.p = Vector2D(40,200)

    def onDraw(self, app:"TheApp"):
        keyinput  = app.keyinput
        canvas    = app.canvas
        images    = app.images

        # キー入力
        keyinput.update()

        # マウス、タッチの補助線を描く
        canvas.draw_rectline(app.touch_rect.p , app.touch_rect.s, "#888")
        if keyinput.touch_pos:
            # タッチされているなら、レバーをその場所に描画する。
            canvas.draw_image_center(images.lever, keyinput.touch_pos)
            # この場合、移動はベクトルで360°自由に移動できるものとする。ただし移動距離は4に制限される。
            self.p += (keyinput.touch_pos - (app.touch_rect.p + app.touch_rect.s//2)).unit(4)
            
        else:
            # タッチされていない場合、レバーをニュートラルの位置に描画する。
            canvas.draw_image_center(images.lever, app.touch_rect.p + app.touch_rect.s//2)

            # マウスクリック、タッチされていないのでキーに応じた移動を行う
            if keyinput.is_key_pressed(VKEY.UP):
                self.p += Vector2D(0, -4)
            if keyinput.is_key_pressed(VKEY.DOWN):
                self.p += Vector2D(0, +4)
            if keyinput.is_key_pressed(VKEY.LEFT):
                self.p += Vector2D(-4, 0)
            if keyinput.is_key_pressed(VKEY.RIGHT):
                self.p += Vector2D(+4, 0)

        # 画面外に出れないように移動を制限する
        self.p = self.p.clamp(canvas.rect)

        # プレイヤーの描画
        canvas.draw_image_center(images.spaceship, self.p)

# 敵の生成器
class EnemyGenerator(MyGameObject):
    def __init__(self):
        super().__init__()
        # ゲームの進行度を表すカウンター
        self.counter = 0

    def onDraw(self,app:"TheApp"):

        # このメソッドは、GameMainSceneからしか呼び出さない。
        scene = cast(GameMainScene, app.scene)
        
        # 敵のlist
        enemies = scene.enemies

        # 少年と少女を定期的に追加する。
        # 適当に少年と少女を追加。ただし60の倍数だと周期的になって良くない。
        # 2000を超えるまで追加して、あとは弾を激しくしていく考え

        if self.counter < 2000:
            if self.counter % 397 == 0:
                enemies.append(Boy())
            # 2秒に1回少女追加
            elif self.counter % 113 == 0:
                enemies.append(Girl())
        self.counter+=1

# 背景の星
class Star(MyGameObject):
    # predraw == Trueなら画面全体に対してランダムに配置する(ゲーム始まる前の星のセット)
    def __init__(self, app:"TheApp", predraw:bool = False):
        super().__init__()

        # 星の座標。predrawがTrueならば横方向もランダム化
        rect = app.canvas.rect
        self.p    = Vector2D(
            app.math.randint(0, int(rect.s.x) ) if predraw else rect.s.x ,
            app.math.randint(0, int(rect.s.y) )
        )

        # 星の色はランダム
        self.color = ("blue","white","red","magenta")[app.math.randint(0,4)]
        # 星の速度もランダム
        self.speed = app.math.randint(1,10)

    def onDraw(self,app:"TheApp"):
        # 点を(1,1)の矩形として描く
        app.canvas.draw_rect(self.p,Vector2D(1,1),self.color)

        # 星を移動
        self.p += Vector2D(-self.speed,0)      

        # 左端に消えたらobjectを消滅させる。
        if self.p.x < 0:
            self.deleted = True  


# スコアなどの更新器
class ScoreUpdater(MyGameObject):
    def __init__(self):
        super().__init__()

        # ゲームのスコア
        self.score = 0
        
    def onDraw(self,app:"TheApp"):
        
        # このメソッドは、GameMainSceneからしか呼び出さない。
        scene = cast(GameMainScene, app.scene)
        
        # 背景の星を生成しておく。1/10の確率で右端に生成。
        if app.math.randint(10) == 0:
            scene.stars.append(Star(app))

        # スコアの加算、描画
        self.score += 1
        app.canvas.draw_text(f"Score {self.score}",Vector2D(330,5))

        # 当たり判定
        gameover = False
        player:GamePlayer = scene.player
        for object in scene.bullets.objects:
            bullet = cast(Bullet, object)
            # 弾とプレイヤーが10以下の距離であるなら
            if (bullet.p - player.p).norm() <= 10:
                gameover = True

        # ゲームオーバーになっていたら、それを表示してゲーム停止。
        if gameover:
            app.audios[AUDIO.GAME_OVER].play() # 爆発音
            app.canvas.draw_text_center("Game Over",Vector2D(400,220),font = "60px serif",color = "red")
            # app.gametimer.stop()
            # app.keyinput.remove_event() # F5キーが利かないなど嫌なので戻しておく。
            app.scene = GameOverScene()

        # ゲーム開始直後だけ、"Game Start"のメッセージを点滅表示。↑とは同時に起きない。
        elif self.score < 100 and (self.score // 20 % 2) == 0:
            app.canvas.draw_text_center("Game Start",Vector2D(400,220),font = "60px serif",color = "blue")

# ゲームで使用する画像
# 画像が多いならImageLoaderを使うべき。(画像の読み込み完了を待機できるので)
class Images:
    def __init__(self):

        # 弾 黄と赤
        self.bullet0   = Image("star0-s.png")
        self.bullet1   = Image("star1-s.png")

        # こども 男
        self.boy       = Image("ha_yaeba_boy_s.png")

        # こども 女
        self.girl      = Image("ha_yaeba_girl_s.png")

        # プレイヤー画像
        self.spaceship = Image("space_rocket_kids-small.png")

        # レバー画像
        self.lever     = Image("lever-s.png")


# GameSceneの基底クラス。これを派生させて、各シーンを作る。
class Scene:
    def onDraw(self, app:"TheApp"):
        pass

# ゲーム開始時のキー説明のScene
class GameOpeningScene(Scene):
    def onDraw(self, app:"TheApp"):
        canvas = app.canvas
        # ゲーム説明の表示
        canvas.clear()
        canvas.draw_text_center("Instruction",Vector2D(400,130))
        canvas.draw_text_center("Cursor Key to move",Vector2D(400,200),"28px serif")
        canvas.draw_text_center("Mouse Click or Tourch is also available",Vector2D(400,230),"20px serif")

        # 何かキーが押されたらゲーム開始
        app.keyinput.update()
        if app.keyinput.is_any_key_pressed():
            app.scene = GameMainScene(app)

# ゲームオーバー時のScene
class GameOverScene(Scene):
    def __init__(self):
        # 時間経過監視用のカウンター
        self._counter = 0

    def onDraw(self, app:"TheApp"):
        # 画面更新は不要
        self._counter += 1
        if self._counter > 3 * 60: # 3秒経過
            # オープニングのSceneへ
            app.scene = GameOpeningScene()

# ゲーム本体
class GameMainScene(Scene):
    def __init__(self , app:"TheApp"):

        # このclassの外部から参照したいGameObject

        # 星
        self.stars   = GameObjectManager()
        # 最初に背景に星を散らばめておく。
        for _ in range(40):
            self.stars.append(Star(app,True))

        # 敵
        self.enemies = GameObjectManager()

        # プレイヤー
        self.player  = GamePlayer()

        # 弾
        self.bullets = GameObjectManager() 

        # 描画優先順位の逆順で登録しておく。(その順番で呼び出したいので)
        self.draw_objects = (
            self.stars        ,
            self.enemies      ,
            self.player       ,
            self.bullets      ,
            EnemyGenerator()  , # 敵の生成器
            ScoreUpdater()    , # スコアの更新器
        )

    def onDraw(self, app:"TheApp"):

        # スクリーンのクリア                
        app.canvas.clear()

        # 描画優先順位の逆順で描画していく。
        for object in self.draw_objects:
            object.onDraw(app)
        
# ==============================================================================
#                         The App
# ==============================================================================

class TheApp(GameContext):
    def __init__(self):

        # タッチ入力矩形
        self.touch_rect   = Rect(Vector2D(50,200),Vector2D(150,150))

        # キー入力用
        self.keyinput     = VirtualKeyInput()
        self.keyinput.configure_6keys_8directions_game(self.touch_rect)

        # 描画用スクリーン
        self.canvas       = Canvas()

        # 数学関連のツール
        self.math         = MathTools()

        # 画像関連
        self.images       = Images()

        # 最初に遷移すべきScene
        self.scene:Scene  = GameOpeningScene()

        # 音声ファイル
        audio_loader      = AudioLoader(audio_file_list)
        self.audios       = audio_loader.audios

        # 描画のloop
        self.gametimer    = GameTimer( lambda : self.scene.onDraw(self) , fps = 60)


if __name__ == "__main__":
    try:
        # the singleton instance of TheApp
        TheApp()
    except:
        InfoDialog("Exception",traceback.format_exc())
