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

[![sample thumbnail](https://yaneurao.github.io/yanesdk-for-brython/gif/sample-thumb.png)](https://yaneurao.github.io/yanesdk-for-brython/)

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

# FAQ

## ローカル環境で開発すると上のサンプルコードがエラーになります。

上のサンプルプログラムはsrc="yanesdk.py"の部分で同じフォルダに配置されたyanesdk.pyを読み込むのはAjaxを用いて読み込まれるため、ローカル環境だとセキュリティエラーになることがあります。(例えば、Chrome 97以降) その場合、外部ファイルから読み込むのではなく、htmlファイルに埋め込む必要があります。

## VSCode(Visual Studio Code)で開発するときに入力補間が利かないです。

VS Codeで開発する場合、html上に直接Pythonのコードを書いていくと入力補完が利かなくて面倒かも知れません。このため、私は、プリプロセッサ([preprocessor.py](https://github.com/yaneurao/yanesdk-for-brython/blob/main/yanesdk/preprocessor.py))を作成してそれで解決しています。

## preprocessor.pyの使い方を教えてください。

以下のコマンドで、template.htmlを読み込み、そこにincludeとして書かれているPythonのプログラムを埋め込んでindex.htmlに出力できます。

```a.bat
python preprocessor.py template.html index.html
```

例えば、スキーゲームなら、その[template.html](https://github.com/yaneurao/yanesdk-for-brython/blob/main/sample/ski/template.html)で、#include "ski.py" と書いてあるところに [ski.py](https://github.com/yaneurao/yanesdk-for-brython/blob/main/sample/ski/ski.py) を読み込み、さらに、そのski.pyの冒頭で

```python
from yanesdk import * # done by preprocessor
```

と書いてあるので、ここで同じフォルダに配置されたyanesdk.pyが読み込まれ、最終的に [index.html](https://github.com/yaneurao/yanesdk-for-brython/tree/main/docs/ski/index.html) が出力されます。

// このプリプロセッサの使い方(作る過程も含め)は、以下の本ライブラリの製作動画#1の冒頭にありますので、参考にしてみてください。

## VS Codeで開発する時に、yanesdk.pyに対してPylanceが警告をたくさん出します。

importしているbrowserがBrythonで用意されているライブラリであるため、Pylanceはそれにアクセスできないためです。代わりにダミーの[browser.py](https://github.com/yaneurao/yanesdk-for-brython/blob/main/yanesdk/browser.py) を同じフォルダに配置すると警告は出なくなります。

## このrepositoryの sampleフォルダと docsフォルダには何故同じファイルがあるのですか？

sampleフォルダがもともとのソースコードです。これをpreprocessor.pyでyanesdk.pyを結合し、htmlファイルに埋め込んで最終的なhtmlにしています。この最終的なhtmlに、画像などの素材を加えたものが docsフォルダに配置されています。このdocsフォルダのhtmlが、[サンプルゲーム デモページ](https://yaneurao.github.io/yanesdk-for-brython/)から見えています。(これは、GitHubの静的ファイルのホスティング機能です。)

## サンプルのソースコードや画像素材もMIT Licenseが適用されますか？

- サンプルのソースコードにもMIT Licenseが適用されます。
- サンプルの画像素材は、[いらすとや](https://www.irasutoya.com/)の素材をリサイズしています。再配布自体は問題ないですが、この画像の著作権は、いらすとやにあります。
- サンプルの音声素材は、フリー素材を加工したもので、再配布自体は問題ないですが、これも著作権自体は放棄していません。

# 本ライブラリのガイダンス動画

coming soon..

# 本ライブラリの製作動画

このSDKを製作しながら、上記のサンプルゲームを作っていく過程を撮影した実況動画です。このSDK自体を作る工程も含まれているので、わりと専門的な内容もありますが、実際に作っていくときの参考になるかと思います。

[![alt設定](http://img.youtube.com/vi/CVWYS_9ZtfM/mqdefault.jpg)](https://www.youtube.com/watch?v=CVWYS_9ZtfM)

[![alt設定](http://img.youtube.com/vi/TviN9fnl89o/mqdefault.jpg)](https://www.youtube.com/watch?v=TviN9fnl89o)

第３回、第４回は準備中。
