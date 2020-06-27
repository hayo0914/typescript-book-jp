# TypeScript入門 & 環境構築

* [TypeScript入門](./#typescriptwomeyou)
* [TypeScriptのバージョン](./#typescriptnobjon)

## TypeScript 入門 & 環境構築

TypeScriptは、 最終的にJavaScriptにコンパイルされます。実際に実行されるのは、JavaScriptです。開発をするときは、TypeScriptを書きますが、ブラウザで実行する時には、TypeScriptをコンパイルして作成されたJavaScriptを実行する、ということです\(Node.jsでも同じです\)。なので、TypeScriptを利用するには、次のものが必要です：

* TypeScriptコンパイラ \([NPM](https://www.npmjs.com/package/typescript)のパッケージとして提供されています。または、OSS\(オープンソースソフトウェア\)の[ソース](https://github.com/Microsoft/TypeScript/)をローカル環境でビルドして利用することもできます\)
* TypeScriptのエディタ \(メモ帳でも開発できますが、TypeScriptをデフォルトでサポートしている[Visual Studio Code \(VSCode\)](https://code.visualstudio.com/) をお勧めします。また、他にも[様々なIDE\(統合開発環境\)](https://github.com/Microsoft/TypeScript/wiki/TypeScript-Editor-Support)でTypeScriptがサポートされています。\)

### TypeScriptのバージョン

Macであればターミナル、Windowsであればコマンドプロンプトを開いて、次のコマンドを実行すれば、インストールできます。`npm`コマンドは [Node.js](https://nodejs.org/ja/) をインストールすると利用できます。インストール方法は [TypeScriptの公式サイト](https://www.typescriptlang.org/#installation) にも記載されています。

```text
npm install -g typescript
```

より最新の機能を試したい場合は、夜間ビルド\(nightly version\)の最新版を利用することもできます。夜間ビルドのバージョンは、次のコマンドでインストールできます。

```text
npm install -g typescript@next
```

これで`tsc`コマンドを利用できます。`tsc` はTypeScriptのコンパイラを起動するコマンドです。`tsc app.ts`のように実行して、TypeScriptのファイルをJavaScriptにコンパイルできます。

VSCodeが利用するTypeScriptの場所をプロジェクトごとに設定することができます。下記はその例です。ほとんどの場合、このような設定をする必要はありませんが、紹介しておきます:

* VSCodeで利用するTypeScriptのバージョンのパスを `.vscode/settings.json`で指定できます

```javascript
{
  "typescript.tsdk": "./node_modules/typescript/lib"
}
```

### サンプルのソースコードについて

ここで紹介しているソースコードは、[githubのリポジトリ](https://github.com/basarat/typescript-book/tree/master/code) にあります。 ほとんどのコードサンプルは、VSCodeにコピーしてそのまま実行できます。追加設定が必要なコードサンプル\(例：npmモジュールのインストールが必要な場合\)では、そのコードにリンクを記載します。下記はその例です:

`hoge/hoge/code.ts`

```typescript
// 対象のコード
```

では、TypeScriptで開発するための設定を行いましょう。そして、TypeScriptの構文を見ていきましょう。

