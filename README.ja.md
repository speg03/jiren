# jiren

jirenはテンプレートからテキストを生成するアプリケーションです。テンプレートのフォーマットはjinja2に基づいています。

[![PyPI](https://img.shields.io/pypi/v/jiren.svg)](https://pypi.org/project/jiren/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jiren.svg)](https://pypi.org/project/jiren/)
[![Build Status](https://travis-ci.com/speg03/jiren.svg?branch=master)](https://travis-ci.com/speg03/jiren)
[![codecov](https://codecov.io/gh/speg03/jiren/branch/master/graph/badge.svg)](https://codecov.io/gh/speg03/jiren)

## インストール

```
pip install jiren
```

## 使い方

`jiren` コマンドを使ってテンプレートからテキストを生成します。 `jiren` コマンドは標準入力からテンプレートを読み込むことができます。

コマンド:
```
echo "hello, {{ message }}" | jiren --message=world
```
出力:
```
hello, world
```

この例では、テンプレートに `message` という変数が含まれています。テンプレートの書式について詳しく知りたい場合は、jinja2のドキュメント ( http://jinja.pocoo.org/ ) を参照してください。

ヘルプを使って、テンプレート内に定義された変数を確認することができます。

コマンド:
```
echo "hello, {{ message }}" | jiren --help
```
出力:
```
usage: jiren [-h] [--message MESSAGE]

optional arguments:
  -h, --help         show this help message and exit
  --message MESSAGE
```
