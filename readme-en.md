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

<image src="https://yaneurao.github.io/yanesdk-for-brython/gif/sample-thumb.png"/>

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


## Note: If you develop in a local environment

The sample program above loads yanesdk.py placed in the same folder in the src="yanesdk.py" section, which is loaded using Ajax, which may cause a security error in a local environment. (For example, Chrome 97 or later) In that case, you need to embed it in an html file instead of loading it from an external file.


## Notes : When developing with VS Code, etc.

When developing with VS Code, writing Python code directly on html may be troublesome because input completion is not available. For this reason, I have created a preprocessor and solved the problem with it. [preprocessor.py](yanesdk/preprocessor.py)

Please refer to the beginning of the production video #1 of this library below to learn how to use this preprocessor (including the process of making it).

# Guidance video for this library

coming soon..

# Video of this library in production (Japanese)

This is a live video of the process of making the above sample game while producing this SDK. The video includes the process of making this SDK itself, so some of the content is rather technical, but I think it will be helpful when actually making the game.

[![alt設定](http://img.youtube.com/vi/CVWYS_9ZtfM/mqdefault.jpg)](https://www.youtube.com/watch?v=CVWYS_9ZtfM)

[![alt設定](http://img.youtube.com/vi/TviN9fnl89o/mqdefault.jpg)](https://www.youtube.com/watch?v=TviN9fnl89o)

The 3rd and 4th editions are in preparation.

