# Brythonで警告を出さないためのダミーヘッダー
# preprocessor.pyで、このファイルはhtmlに埋め込まない。

from typing import Callable

class Touch:
    @property
    def clientX(self)->int:
        return 0

    @property
    def clientY(self)->int:
        return 0

    @property
    def identifier(self)->int:
        return 0
        

# addEventListenerで登録されたイベントハンドラの引数
class DOMEvent:
    @property
    def keyCode(self)->int:
        return 0

    @property
    def offsetX(self)->int:
        return 0

    @property
    def offsetY(self)->int:
        return 0

    @property
    def buttons(self)->int:
        return 0
        
    @property
    def touches(self)->list[Touch]:
        return []

    def preventDefault(self):
        pass

    def stopPropagation(self):
        pass

class TextMetrics:
    def __init__(self):
        self.width = 0
        self.height = 0

class HtmlImage:
    def __init__(self):
        self.naturalWidth = 0
        self.naturalHeight = 0

    def __setitem__(self, name:str, value:str)->"Element":
        return Element()

class CanvasRenderingContext:
    def __init__(self):
        self.fillStyle:str
        self.strokeStyle:str
        self.font:str
        self.textBaseline:str

    def fillRect(self,x:int|float,y:int|float,w:int|float,h:int|float):
        pass

    def fillText(self,text:str,x:int|float,y:int|float):
        pass

    def strokeRect(self,x:int|float,y:int|float,w:int|float,h:int|float):
        pass

    def drawImage(self,image:HtmlImage, sx:int|float,sy:int|float,sw:int|float,sh:int|float,px:int|float,py:int|float,dw:int|float,dh:int|float):
        pass

    def measureText(self,text:str) -> TextMetrics:
        return TextMetrics()


class ImageCreator:
    def new(self)->HtmlImage:
        return HtmlImage()

class IntervalHandle:
    pass

class window:
    Image = ImageCreator()

    @staticmethod
    def setInterval(callback: Callable[[],None], t:int|float)->IntervalHandle:
        return IntervalHandle()

    @staticmethod
    def clearInterval(handle:IntervalHandle):
        pass


class Element:
    def __init__(self):
        # for audio
        self.currentTime = 0
        self.volume = 0
        # for canvas
        self.width = 0
        self.height = 0

    def createElement(self, name:str)->"Element":
        return Element()

    def addEventListener(self, eventName:str, callback: Callable[[DOMEvent],None]):
        pass

    def removeEventListener(self, eventName:str, callback: Callable[[DOMEvent],None]):
        pass

    def __getitem__(self, name:str)->"Element":
        return Element()

    def __setitem__(self, name:str, value:str)->"Element":
        return Element()


    # for audio

    def play(self):
        pass
    def stop(self):
        pass
    def pause(self):
        pass

    # for canvas
    def getContext(self, name:str)->CanvasRenderingContext:
        return CanvasRenderingContext()

document = Element()

class dialog:
    pass

class widgets:
    def __init__(self):
        self.dialog = dialog()

