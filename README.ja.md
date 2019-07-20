# jiren

jirenはテンプレートからテキストを生成するアプリケーションです。テンプレートのフォーマットはjinja2に基づいています。

[![PyPI](https://img.shields.io/pypi/v/jiren.svg)](https://pypi.org/project/jiren/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jiren.svg)](https://pypi.org/project/jiren/)
[![Build Status](https://travis-ci.com/speg03/jiren.svg?branch=master)](https://travis-ci.com/speg03/jiren)
[![codecov](https://codecov.io/gh/speg03/jiren/branch/master/graph/badge.svg)](https://codecov.io/gh/speg03/jiren)

## インストール

```sh
pip install jiren
```

## 使い方

`jiren` コマンドを使ってテンプレートからテキストを生成します。このコマンドは標準入力またはファイルからテンプレートを読み込むことができます。

標準入力からテンプレートを読み込む例です。

コマンド:
```sh
echo "hello, {{ message }}" | jiren --var.message=world
```
出力:
```
hello, world
```

ファイルからテンプレートを読み込む例です。

コマンド:
```sh
cat <<EOF >template.j2
hello, {{ message }}
EOF
jiren template.j2 --var.message=world
```
出力:
```
hello, world
```

この例では、テンプレートに `message` という変数が含まれています。 `jiren` コマンドに渡すプログラム引数を使って `message` 変数に値を設定できます。プログラム引数の名前は先頭に `--var.` をつける必要があることに注意してください。

テンプレートの書式について詳しく知りたい場合は、jinja2のドキュメント ( http://jinja.pocoo.org/ ) を参照してください。

ヘルプを使って、テンプレート内に定義された変数を確認することができます。

コマンド:
```sh
echo "hello, {{ message }}" | jiren --help
```
出力:
```
usage: jiren [-h] [--var.message VAR.MESSAGE] [infile]

positional arguments:
  infile

optional arguments:
  -h, --help            show this help message and exit

variables:
  --var.message VAR.MESSAGE
```
