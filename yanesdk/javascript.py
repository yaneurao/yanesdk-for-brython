# Brythonで警告を出さないためのダミーヘッダー
# preprocessor.pyで、このファイルはhtmlに埋め込まない。

class Date:
    @staticmethod
    def now()->int:
        return 0

class Math:
    PI = 3.14159

    @staticmethod
    def floor(x:float|int)->int:
        return 0

    @staticmethod
    def sin(x:float|int)->float:
        return 0.0
    
    @staticmethod
    def cos(x:float|int)->float:
        return 0.0

    @staticmethod
    def sqrt(x:float|int)->float:
        return 0.0

    @staticmethod
    def atan2(x:float|int, y:float|int)->float:
        return 0.0

    @staticmethod
    def random()->float:
        return 0.0
