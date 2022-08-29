# jiren

jirenはテンプレートからテキストを生成するアプリケーションです。テンプレートのフォーマットはjinja2に基づいています。

[![PyPI](https://img.shields.io/pypi/v/jiren)](https://pypi.org/project/jiren/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/jiren)](https://pypi.org/project/jiren/)
[![Python Tests](https://github.com/speg03/jiren/actions/workflows/python-tests.yml/badge.svg)](https://github.com/speg03/jiren/actions/workflows/python-tests.yml)
[![codecov](https://codecov.io/gh/speg03/jiren/branch/main/graph/badge.svg?token=bFdpze6ELR)](https://codecov.io/gh/speg03/jiren)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/speg03/jiren/main.svg)](https://results.pre-commit.ci/latest/github/speg03/jiren/main)

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
echo "hello, {{ name }}" | jiren - -- --name=world
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

jiren template.j2 -- --name=world
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
echo "{{ message }}, {{ name }}" | jiren --help -
```
出力:
```
... （中略）

variables:
  --name NAME
  --message MESSAGE
```


### 変数のデフォルト値

値が指定されなかった変数に対して、デフォルト値を設定することができます。これはjinja2の仕様に基づきます。

コマンド:
```sh
echo "{{ message }}, {{ name | default('world') }}" | jiren - -- --message=hello
```
出力:
```
hello, world
```


### dataオプション

`--data` オプションを使うことで、構造的に変数を定義したファイルを渡すことができます。

コマンド:
```sh
cat <<EOF >data.yaml
greeting:
  message: hello
  name: world
EOF

echo "{{ greeting.message }}, {{ greeting.name }}" | jiren --data=data.yaml -
```
出力:
```
hello, world
```


### strictオプション

`--strict` オプションを `--data` オプションと同時に使用したとき、指定したデータファイルに定義された変数はすべてテンプレートの中で使用されていなければなりません。

コマンド:
```sh
cat <<EOF >data.yaml
message: hello
invalid_key: invalid
EOF

echo "{{ message }}" | jiren --data=data.yaml --strict -
```
出力:
```
jiren: error: the data file contains unknown variables: invalid_key
```


### requiredオプション

`--required` オプションを使うと、すべての変数の値を必ず指定しなければいけません。

コマンド:
```sh
echo "{{ message }}, {{ name }}" | jiren --required - -- --message=hello
```
出力:
```
jiren: error: the following variables are required: name
```
