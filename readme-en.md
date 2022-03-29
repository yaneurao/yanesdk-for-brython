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

You can load brython from cdn as follows, and execute brython() in onload of body. you can load another file written in python called sample.py and import yanesdk at the beginning of it.

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
<script type="text/python" src="sample.py">
</body>
</html>
```

```sample.py
# sample.py
from yanesdk import *

Canvas canvas
canvas.clear()
canvas.draw_rect(Vector2D(100,100),Vector2D(200,200),"white")
```

We have not prepared any documentation for this library, but you should be able to understand it by looking at the source code of a sample game.


# FAQ

## The sample code above will cause an error when developed in a local environment.

The sample program above specifies sample.py as an external script, but since this part is loaded using Ajax, it may cause a security error in a local environment. (For example, Chrome 97 or later) In that case, you need to embed it in the html file instead of loading it from an external file.

If you are using VSCode, it is recommended to set up a local server with the Live Server extension.

## Input completion does not work when developing in VSCode (Visual Studio Code).

When developing with VS Code, writing Python code directly on html is troublesome because input completion does not work.

## When developing in VS Code, Pylance gives a lot of warnings for yanesdk.py.

This is because the browser you are importing from yanesdk.py is a library provided by Brython and Pylance cannot access it. If you place a dummy [browser.py](https://github.com/yaneurao/yanesdk-for-brython/blob/main/yanesdk/browser.py) in the same folder instead, the warnings will not appear.

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

