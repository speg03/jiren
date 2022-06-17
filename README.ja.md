# jiren

jirenはテンプレートからテキストを生成するアプリケーションです。テンプレートのフォーマットはjinja2に基づいています。

[![PyPI](https://img.shields.io/pypi/v/jiren.svg)](https://pypi.org/project/jiren/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jiren.svg)](https://pypi.org/project/jiren/)
[![Python Tests](https://github.com/speg03/jiren/workflows/Python%20Tests/badge.svg)](https://github.com/speg03/jiren/actions?query=workflow%3A%22Python+Tests%22)
[![codecov](https://codecov.io/gh/speg03/jiren/branch/main/graph/badge.svg)](https://codecov.io/gh/speg03/jiren)

## インストール

```sh
pip install jiren
```

## 使い方

### テキストの生成

`jiren` コマンドを使ってテンプレートからテキストを生成します。このコマンドは標準入力またはファイルからテンプレートを読み込むことができます。

標準入力からテンプレートを読み込む例です。

コマンド:
```sh
echo "hello, {{ name }}" | jiren -- --name=world
```
出力:
```
hello, world
```

ファイルからテンプレートを読み込む例です。

コマンド:
```sh
cat <<EOF >template.j2
hello, {{ name }}
EOF

jiren -i template.j2 -- --name=world
```
出力:
```
hello, world
```

この例では、テンプレートに `name` という変数が含まれています。 `jiren` コマンドに渡すプログラム引数を使って、テンプレート内の変数に値を指定できます。テンプレート内の変数は `--` より後ろで指定することに注意してください。

テンプレートの書式について詳しく知りたい場合は、jinja2のドキュメント ( http://jinja.pocoo.org/ ) を参照してください。


### テンプレート内の変数

ヘルプを使って、テンプレート内に定義された変数を確認することができます。

コマンド:
```sh
echo "{{ greeting }}, {{ name }}" | jiren -- --help
```
出力:
```
... （中略）

variables:
  --name NAME
  --greeting GREETING
```


### 変数のデフォルト値

値が指定されなかった変数に対して、デフォルト値を設定することができます。これはjinja2の仕様に基づきます。

コマンド:
```sh
echo "{{ greeting }}, {{ name | default('world') }}" | jiren -- --greeting=hello
```
出力:
```
hello, world
```


### requiredオプション

`--required` オプションを使うと、すべての変数の値を必ず指定しなければいけません。

コマンド:
```sh
echo "{{ greeting }}, {{ name }}" | jiren --required -- --greeting=hello
```
出力:
```
... （中略）

jiren: error: the following arguments are required: --name
```
