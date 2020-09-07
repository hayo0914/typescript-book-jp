# Node.js & TypeScriptのプロジェクト作成

TypeScriptは、Node.jsを公式にサポートしています。素早くNode.jsプロジェクトを設定する方法は次のとおりです。

> 注意：これらのステップの多くは実際にはNode.jsの設定手順です

1. プロジェクトの依存関係設定ファイルである`package.json`をセットアップします。素早くこれを行う方法はこれです：`npm init -y`
2. TypeScriptをインストールします\(`npm install typescript --save-dev`\)
3. Node.jsのプログラムに必要な型宣言ファイル`node.d.ts`をインストールします\(`npm install @types/node --save-dev`\)
4. TypeScriptの設定ファイル`tsconfig.json`を初期化します\(`npx tsc --init --rootDir src --outDir lib --esModuleInterop --resolveJsonModule --lib es6,dom --module commonjs`\)

これだけです！これで、IDE\(例えばVSCode\)を起動して遊んでみてください。TypeScriptの安全性を得つつ、心地よく、Node.jsに組み込まれた標準モジュールを使用することができます\(例：`import * as fs from 'fs';`\)。

## ボーナス： 自動でコンパイルと実行を行う

* TypeScriptをコンパイルし、Node.jsで実行するために`ts-node`をインストールする\(`npm install ts-node --save-dev`\)
* ファイルが変更されるたびに`ts-node`を再起動するために`nodemon`をインストールする\(`npm install nodemon --save-dev`\)

アプリケーションのエントリポイントに基づいて下記のような`script`を`package.json`に追加するだけです。エントリポイントを`index.ts`と仮定した場合は次のようになります：

```javascript
  "scripts": {
    "start": "npm run build:live",
    "build": "tsc -p .",
    "build:live": "nodemon --watch 'src/**/*.ts' --exec 'ts-node' src/index.ts"
  },
```

これで、快適に開発を行うことができます。`npm start`を実行して、`index.ts`を変更する度に、次のことが自動的に行われます：

* nodemonが、ts-nodeを再実行する
* ts-nodeは自動的にtsconfig.jsonとTypeScriptバージョンを取得し、TypeScriptをコンパイルする
* ts-nodeは出力されたJavaScriptをNode.jsで実行する

JavaScriptアプリケーションをデプロイする準備が整ったら、`npm run build`を実行します。

## ポイント

このようなNPMモジュールは、browserify\(tsify\)や、webpack\(ts-loader\)を使っていても、問題なく動作します。

