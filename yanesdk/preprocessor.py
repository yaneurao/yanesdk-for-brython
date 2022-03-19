from io import TextIOWrapper
import sys
import re

if len(sys.argv) < 3:
    print("python preprocessor.py src.html dst.html")
    sys.exit()

    # src = "game-template.html"
    # dst = "sakeru.html"
    # import os
    # os.chdir("akikun\\brython\\sakeru")

else:
    src = sys.argv[1]
    dst = sys.argv[2]

print(f"preprocessor : {src} -> {dst}")

# ファイルを読み込みながらfwに書き出していく。
def read_script(filename:str, fw:TextIOWrapper ):
    print(f"open : {filename}")
    with open(filename, "r", encoding="utf_8_sig") as fr:
        lines = fr.readlines()
        for line in lines:
            # includeと書いてあったら、そのファイルを丸読み(ただしこの時にもincludeとかfrom yanesdk import *の処理は行う)
            m = re.match('.*?#include "(.*?)"', line)
            if m and m.group():
                read_script(m.group(1),fw)
                continue

            m = re.match('.*?from (.*?) import \\* # done by preprocessor',line)
            if m and m.group():
                # このpythonファイルをここに埋め込む。
                read_script(f"{m.group(1)}.py",fw)
                continue

            # htmlからは改行を無くすことで、例外が出た時の行数が狂わないようにする。
            if filename==src:
                line = line.strip()

            fw.write(line)

with open(dst, "w", encoding="utf_8_sig") as fw:
    read_script(src,fw)

print("end preprocessing")
