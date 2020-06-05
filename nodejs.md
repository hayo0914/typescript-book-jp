# Node.js & TypeScriptクイックスタート

TypeScriptは、Node.jsを公式にサポートしています。素早くNode.jsプロジェクトを設定する方法は次のとおりです。

> 注意：これらのステップの多くは実際にはNode.jsの設定手順です

1. Node.jsプロジェクト`package.json`をセットアップする。速い方法：`npm init -y`
2. TypeScriptを追加する\(`npm install typescript --save-dev`\)
3. `node.d.ts`を追加する\(`npm install @types/node --save-dev`\)
4. TypeScriptの設定ファイル`tsconfig.json`をいくつかの重要なオプションを使って初期化する\(`npx tsc --init --rootDir src --outDir lib --esModuleInterop --resolveJsonModule --lib es6,dom --module commonjs`\)。

それでおしまい!あなたのIDE\(例えば`code .`\)を起動して遊んでください。TypeScriptの安全性と開発者人間工学とあわせて、組み込みのすべてのノードモジュールを使用することができます\(例：`import * as fs from 'fs';`\)。

## ボーナス： ライブコンパイル+実行

* nodeでのライブコンパイル+実行のために使う`ts-node`を追加する\(`npm install ts-node --save-dev`\)
* ファイルが変更されるたびに`ts-node`を呼び出す`nodemon`を追加する\(`npm install nodemon --save-dev`\)

アプリケーションのエントリポイントに基づいて`script`ターゲットを`package.json`に追加するだけです。エントリポイントを`index.ts`と仮定した場合：

```javascript
  "scripts": {
    "start": "npm run build:live",
    "build": "tsc -p .",
    "build:live": "nodemon --watch 'src/**/*.ts' --exec 'ts-node' src/index.ts"
  },
```

これで、`npm start`を実行し、`index.ts`を編集することができます：

* nodemonはそのコマンド\(ts-node\)を再実行する
* ts-nodeは自動的にtsconfig.jsonとインストールされたTypeScriptバージョンを取得し、トランスパイルを行う
* ts-nodeは出力されたJavaScriptをNode.jsで実行する

JavaScriptアプリケーションのデプロイの準備が完了したが、`npm run build`を実行します。

## ボーナスポイント

そのようなNPMモジュールは、browserify\(tsifyを使用\)またはwebpack\(ts-loaderを使用\)でうまく動作します。

