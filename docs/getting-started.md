* [TypeScript入門]（#getting-started-with-typescript）
* [TypeScriptのバージョン]（#typescript-version）

# TypeScriptを始める

TypeScriptはJavaScriptにコンパイルされます。実際に実行されるのは、JavaScriptです（ブラウザ上、でも、サーバー上でも）。したがって、次のものが必要です：

* TypeScriptコンパイラ（OSSが[ソース](https://github.com/Microsoft/TypeScript/）および[NPM]（https://www.npmjs.com/package/typescript）で利用可能）
* TypeScriptエディタ（望めばメモ帳を使えますが、私は[vscode🌹]（https://code.visualstudio.com/）を[私が作成したプラグイン]（https：// marketplace.visualstudio.com/items?itemName=basarat.god）を一緒に使います。　また、[様々なIDE]（https://github.com/Microsoft/TypeScript/wiki/TypeScript-Editor-Support）がサポートされています。）


## TypeScriptのバージョン
安定版のTypeScriptコンパイラを使用する代わらに、本書ではバージョン番号に関連付けられていないたくさんの新しいものを紹介します。コンパイラのテスト環境は時間経過とともにより多くのバグを見つけたため、私は一般的に夜間ビルドの最新版を使用することを勧めます。

次のコマンドでインストールができます。

```
npm install -g typescript@next
```

そして、今、`tsc`コマンドは最新かつ最高のものです。あらゆるIDEもサポートしています。

* vscodeで利用するTypeScriptのバージョンは `.vscode / settings.json`に以下の内容を保存することで指定できます

```json
{
  "typescript.tsdk": "./node_modules/typescript/lib"
}
```

## ソースコード取得
この書籍のソースは、githubのリポジトリ https://github.com/basarat/typescript-book/tree/master/code にあります。
ほっとんどのコードサンプルをvscodeにコピーしてそのまま使用することができます。追加設定が必要なコードサンプル（例：npmモジュール）で、コードを表示する前にサンプルにのリンクを提示します。例えば

`this/will/be/the/link/to/the/code.ts`
```ts
// 議論中のコード
```

開発用設定をして、TypeScriptのシンタックスを見ていきましょう。
