[日本語](readme.md) / English

# YaneuraoGameSDK for Brython

This is a game library that makes it easy to create browser games in Python.

# Features

- Can be written in Python.
- Compatible with PC and both Android/iOS.
- Easily display images and play sounds.
- Transparently handles keyboard, mouse, and screen touch.

# Principle

It uses [Brython](https://brython.info/), a transpiler that converts Python code written in the browser into JavaScript.

# Sample page

A sample game actually made with this library is available below.
Keyboard, mouse, and screen touch are all supported.

[![sample thumbnail](https://yaneurao.github.io/yanesdk-for-brython/gif/sample-thumb.png)](https://yaneurao.github.io/yanesdk-for-brython/)

- [Sample game demo page](https://yaneurao.github.io/yanesdk-for-brython/)
- [Sample source code](sample)

# Usage

Please download and use [yanesdk.py](yanesdk/yanesdk.py) from this GitHub.

Load brython from cdn as follows, and execute brython() with onload of body. After that, you can write a program using it in Python by loading yanesdk.py.

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

We have not prepared any documentation for this library, but you should be able to understand it by looking at the source code of a sample game.


# FAQ

## The sample code above causes an error when developed in a local environment.

The sample program above may cause a security error in a local environment because it uses Ajax to load yanesdk.py placed in the same folder in the "src="yanesdk.py" section. (e.g., Chrome 97 or later) In that case, you need to embed it in an html file instead of loading it from an external file.

## Input interpolation does not work when developing with VSCode (Visual Studio Code).

When developing with VS Code, writing Python code directly on html may be troublesome because input completion does not work. For this reason, I created a preprocessor ([preprocessor.py](https://github.com/yaneurao/yanesdk-for-brython/blob/main/yanesdk/preprocessor.py)) to solve this problem.

## How do I use preprocessor.py?

With the following command, you can load template.html, embed the Python program written as include in it, and output it to index.html.

```a.bat
python preprocessor.py template.html index.html
```

For example, for a ski game, in its [template.html](https://github.com/yaneurao/yanesdk-for-brython/blob/main/sample/ski/template.html), #include "ski.py" where it says [ski.py](https://github.com/yaneurao/yanesdk-for-brython/blob/main/sample/ski/ski.py) is loaded, and then at the beginning of that ski.py

```python
from yanesdk import * # done by preprocessor
```

so yanesdk.py placed in the same folder is read here, and finally [index.html](https://github.com/yaneurao/yanesdk-for-brython/tree/main/docs/ski/index.html) is output.

// Please refer to the beginning of the following video #1 of the production of this library for the usage of this preprocessor (including the process of making it).

## When developing with VS Code, Pylance gives a lot of warnings for yanesdk.py.

This is because the browser you are importing is library provided by Brython, and Pylance cannot access them. Instead, if you place dummy [browser.py](https://github.com/yaneurao/yanesdk-for-brython/blob/main/yanesdk/browser.py) in the same folder, the warning will not appear.

## Why are there the same files in the sample and docs folders of this repository?

The "sample" folder is the original source code. This is combined with yanesdk.py in preprocessor.py and embedded in an html file to make the final html. This final html, plus images and other materials, is placed in the "docs" folder. The html in this docs folder is visible from the [sample game demo page](https://yaneurao.github.io/yanesdk-for-brython/). (This is GitHub's static file hosting feature.)

## Does the MIT License also apply to the sample source code and image material?

- The MIT License also applies to the sample source code.
- The image materials in the samples are resized from materials from [Irastoya](https://www.irasutoya.com/). Redistribution itself is not a problem, but the copyright of this image belongs to Irastoya.
- The audio material in the sample is processed from free material. Redistribution itself is not a problem, but the copyright itself is not renounced in this case either.

# Guidance video for this library

coming soon..

# Video of this library in production (Japanese)

This is a live video of the process of making the above sample game while producing this SDK. The video includes the process of making this SDK itself, so some of the content is rather technical, but I think it will be helpful when actually making the game.

[![alt設定](http://img.youtube.com/vi/CVWYS_9ZtfM/mqdefault.jpg)](https://www.youtube.com/watch?v=CVWYS_9ZtfM)

[![alt設定](http://img.youtube.com/vi/TviN9fnl89o/mqdefault.jpg)](https://www.youtube.com/watch?v=TviN9fnl89o)

The 3rd and 4th editions are in preparation.

