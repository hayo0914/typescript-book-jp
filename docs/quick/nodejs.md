# TypeScript with Node.js
TypeScriptは、最初からNode.jsをサポートしています*。クイックNode.jsプロジェクトを設定する方法は次のとおりです。

> 注意：これらのステップの多くは実際にはNode.jsの設定手順

1. Node.jsプロジェクト `package.json`をセットアップします。速いもの： `npm init -y`
1. TypeScriptを追加する( `npm install typescript --save-dev`)
1. `node.d.ts`を追加します(`npm install @ types / node --save-dev`)
1. TypeScriptオプションの `tsconfig.json`を起動します(`npx tsc --init`)。
1. tsconfig.jsonに `compilerOptions.module：commonjs`があることを確認します

それでおしまい!あなたのIDE(例えば `alm -o`)を起動して遊んでください。 TypeScriptのすべての安全性と開発者の人間工学に合わせて、組み込みのすべてのノードモジュールを使用することができます(例： `import fs = require( 'fs');`)。

## ボーナス：ライブコンパイル+実行
* ライブコンパイル+をノード( `npm install ts-node --save-dev`)で実行する`ts-node`を追加する
* ファイルが変更されるたびに `ts-node`を呼び出す`nodemon`を追加します( `npm install nodemon --save-dev`)

アプリケーションのエントリに基づいて `script`ターゲットを`package.json`に追加するだけです。その `index.ts`を仮定します：

```json
  "scripts": {
    "start": "npm run build:live",
    "build:live": "nodemon --exec ./node_modules/.bin/ts-node -- ./index.ts"
  },
```

したがって、 `npm start`を実行し、`index.ts`を編集することができます：

* nodemonはそのコマンドを再実行します(ts-node)
* ts-nodeは自動的にtsconfig.jsonとインストールされたtypescriptバージョンを取得し、
* ts-nodeはNode.jsを介して出力javascriptを実行します。

## TypeScriptノードモジュールを作成する

* [Typecriptノードモジュールの作成に関するレッスン](https://egghead.io/lessons/typescript-create-high-quality-npm-packages-using-typescript)

TypeScriptで書かれたモジュールを使用することは、コンパイル時の安全性とオートコンプリート(基本的に実行可能なドキュメント)が得られるので面白いことです。

高品質のTypeScriptモジュールの作成は簡単です。あなたのパッケージには、以下の希望のフォルダ構造が仮定されます。

```text
package
├─ package.json
├─ tsconfig.json
├─ src
│  ├─ All your source files
│  ├─ index.ts
│  ├─ foo.ts
│  └─ ...
└─ lib
  ├─ All your compiled files
  ├─ index.d.ts
  ├─ index.js
  ├─ foo.d.ts
  ├─ foo.js
  └─ ...
```


* あなたの `tsconfig.json`
  * libディレクトリに宣言ファイルとjsファイルを生成します。
  * include：["./src / ** / *"] `<これは`src`ディレクトリからのすべてのファイルを含みます。

* あなたの `package.json`には
  * ``main "：" lib / index "` <これはNode.jsに `lib / index.js`をロードするように指示します。
  * `" types "：" lib / index "`<これはTypeScriptに `lib / index.d.ts`をロードするように指示します。


パッケージ例：
* `npm install typestyle` [for TypeStyle](https://www.npmjs.com/package/typestyle)
* 使用法： `typestyle 'からの`import {style}; `は完全な型安全です。

もっと：

* あなたのパッケージが他のTypeScriptのオーサリングされたパッケージに依存している場合は、そのままraw JSパッケージと同様に `dependencies`/` devDependencies`/ `peerDependencies`に入れてください。
* パッケージが他のJavaScript作成パッケージに依存していて、プロジェクトで型安全性を使用する場合は、そのタイプ( `@ types / foo`など)を`devDependencies`に入れます。 JavaScriptのタイプは、メインのNPMストリームから*範囲外で*管理する必要があります。 JavaScriptのエコシステムでは、意味論的なバージョン管理があまり一般的でない型を壊すので、ユーザーが型を必要とする場合は、それらに対応する `@ types / foo`バージョンをインストールする必要があります。

## ボーナスポイント

そのようなNPMモジュールは、browserify(tsifyを使用)またはwebpack(ts-loaderを使用)でうまく動作します。
