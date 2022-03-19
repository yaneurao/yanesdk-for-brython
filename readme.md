日本語 / [English](readme-en.md)

# YaneuraoGameSDK for Brython

ブラウザゲームをPythonでお手軽に作れるゲームライブラリです。

# 特長

- Pythonで書ける。
- PC、Android/iOS両対応。
- 簡単に画像を表示したり、音を鳴らしたりできる。
- キーボード、マウス、スクリーンタッチを透過的に扱える。

# 原理

[Brython](https://brython.info/)という、ブラウザ上で書いたPythonのコードをJavaScriptに変換してくれるトランスパイラを利用しています。

# サンプルページ

実際に本ライブラリで作ったサンプルゲームを以下で公開しています。
キーボード、マウス、スクリーンタッチすべてに対応しています。

- [サンプルゲーム デモページ](https://yaneurao.github.io/yanesdk-for-brython/)
- [サンプルのソースコード](https://github.com/yaneurao/yanesdk-for-brython/blob/main/sample)

# 使い方

本GitHubの [yanesdk.py](https://github.com/yaneurao/yanesdk-for-brython/blob/main/yanesdk/yanesdk.py)をダウンロードしてお使いください。

以下のようにcdnからbrythonを読み込むようにして、bodyのonloadでbrython()を実行します。あとは、yanesdk.pyを読み込むようにすれば、これを利用したプログラムがPythonで書けます。

```sample.html
<html>
<head>
    <meta charset="utf-8">
    <script type="text/javascript"
        src="https://cdn.jsdelivr.net/npm/brython@3.10.5/brython.min.js">
    </script>
    <script type="text/javascript"
        src="https://cdn.jsdelivr.net/npm/brython@3.10.5/brython_stdlib.js">
    </script>
</head>

<body onload="brython()">

<canvas id="canvas" width="800" height="400" style="cursor:none"></canvas>

<script type="text/python" src="yanesdk.py">
<script type="text/python">

Canvas canvas
canvas.clear()
canvas.draw_rect(Vector2D(100,100),Vector2D(200,200),"white")

</body>
</html>
```

本ライブラリに関して、ドキュメント類は用意していないのですが、ソースコードにコメントがたくさん書いてあるので、サンプルゲームのソースコードと照らし合わせれば使い方はわかるかと思います。

## 注意点 : ローカル環境で開発する場合

上のサンプルプログラムはsrc="yanesdk.py"の部分で同じフォルダに配置されたyanesdk.pyを読み込むのはAjaxを用いて読み込まれるため、ローカル環境だとセキュリティエラーになることがあります。(例えば、Chrome 97以降) その場合、外部ファイルから読み込むのではなく、htmlファイルに埋め込む必要があります。

## 注意点 : VS Codeなどで開発する場合

VS Codeで開発する場合、html上に直接Pythonのコードを書いていくと入力補完が利かなくて面倒かも知れません。このため、私は、プリプロセッサを作成してそれで解決しています。[preprocessor.py](https://github.com/yaneurao/yanesdk-for-brython/blob/main/yanesdk/preprocessor.py)

このプリプロセッサの使い方(作る過程も含め)は、以下の本ライブラリの製作動画#1の冒頭にありますので、参考にしてみてください。

# 本ライブラリのガイダンス動画

coming soon..

# 本ライブラリの製作動画

このSDKを製作しながら、上記のサンプルゲームを作っていく過程を撮影した実況動画です。このSDK自体を作る工程も含まれているので、わりと専門的な内容もありますが、実際に作っていくときの参考になるかと思います。

[![alt設定](http://img.youtube.com/vi/CVWYS_9ZtfM/mqdefault.jpg)](https://www.youtube.com/watch?v=CVWYS_9ZtfM)

[![alt設定](http://img.youtube.com/vi/TviN9fnl89o/mqdefault.jpg)](https://www.youtube.com/watch?v=TviN9fnl89o)

第３回、第４回は準備中。
