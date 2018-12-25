* [TypeScript入門](#getting-started-with-typescript)
* [TypeScriptのバージョン](#typescript-version)

# TypeScriptを始めよう

TypeScriptはJavaScriptにコンパイルされます。実際に実行されるのは、JavaScriptです(ブラウザでもサーバーでも)。よって、次のものが必要です：

* TypeScriptコンパイラ(OSSが[ソース](https://github.com/Microsoft/TypeScript/)と[NPM](https://www.npmjs.com/package/typescript)で利用可能です)
* TypeScriptエディタ(そうしたければ、メモ帳を使えますが、私は [vscode🌹](https://code.visualstudio.com/) を [私が作成したプラグイン](https://marketplace.visualstudio.com/items?itemName=basarat.god) とともに使います。また、[様々なIDE](https://github.com/Microsoft/TypeScript/wiki/TypeScript-Editor-Support)がサポートされています。)


## TypeScriptのバージョン
安定版のTypeScriptコンパイラを使用する代わりに、本書ではバージョン番号に関連付けられていない多くの新規要素を紹介します。コンパイラのテスト環境は時間が経過するほど多くのバグを見つけるため、私は一般的に夜間ビルド(nightly version)の最新版を使用することを推奨します。

次のコマンドでインストールできます。

```
npm install -g typescript@next
```

そして、今、`tsc`コマンドは最新かつ至高のものです。様々なIDEもそれを可能にしています。例:

* vscodeで利用するTypeScriptのバージョンのパスを `.vscode/settings.json`で指定できます

```json
{
  "typescript.tsdk": "./node_modules/typescript/lib"
}
```

## ソースコード取得
この書籍のソースコードは、githubのリポジトリ https://github.com/basarat/typescript-book/tree/master/code にあります。
ほとんどのコードサンプルは、vscodeにコピーしてそのまま実行できます。追加設定が必要なコードサンプル(例：npmモジュール)では、そのコードを表示する前にコードサンプルのパスにリンクします。例:

`this/will/be/the/link/to/the/code.ts`
```ts
// 議論中のコード
```

開発設定をして、TypeScriptの構文を見ていきましょう。
