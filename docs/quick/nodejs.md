# TypeScript with Node.js
TypeScriptは、Node.jsを公式にサポートしています。素早くNode.jsプロジェクトを設定する方法は次のとおりです。

> 注意：これらのステップの多くは実際にはNode.jsの設定手順です

1. Node.jsプロジェクト`package.json`をセットアップする。速い方法：`npm init -y`
1. TypeScriptを追加する(`npm install typescript --save-dev`)
1. `node.d.ts`を追加する(`npm install @types/node --save-dev`)
1. TypeScriptの設定ファイル`tsconfig.json`をいくつかの重要なオプションを使って初期化する(`npx tsc --init --rootDir src --outDir lib --esModuleInterop --resolveJsonModule --lib es6,dom --module commonjs`)。

それでおしまい!あなたのIDE(例えば`code .`)を起動して遊んでください。TypeScriptの安全性と開発者人間工学とあわせて、組み込みのすべてのノードモジュールを使用することができます(例：`import fs = require( 'fs');`)。

## ボーナス： ライブコンパイル+実行
* nodeでのライブコンパイル+実行のために使う`ts-node`を追加する(`npm install ts-node --save-dev`)
* ファイルが変更されるたびに`ts-node`を呼び出す`nodemon`を追加する(`npm install nodemon --save-dev`)

アプリケーションのエントリポイントに基づいて`script`ターゲットを`package.json`に追加するだけです。エントリポイントを`index.ts`と仮定した場合：

```json
  "scripts": {
    "start": "npm run build:live",
    "build:live": "nodemon --exec ./node_modules/.bin/ts-node -- ./index.ts"
  },
```

これで、`npm start`を実行し、`index.ts`を編集することができます：

* nodemonはそのコマンド(ts-node)を再実行する
* ts-nodeは自動的にtsconfig.jsonとインストールされたtypescriptバージョンを取得し、トランスパイルを行う
* ts-nodeは出力されたjavascriptをNode.jsで実行する

## TypeScriptのnode moduleを作成する

* [Typecriptのnodemoduleの作成に関するレッスン](https://egghead.io/lessons/typescript-create-high-quality-npm-packages-using-typescript)

TypeScriptで書かれたモジュールを使用することは、コンパイル時の安全性とオートコンプリートが得られるので、非常に楽しいことです。

高品質のTypeScriptモジュールの作成は簡単です。以下の望ましいフォルダ構造を仮定します。

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


* `tsconfig.json`について
  * `compilerOptions`に`"outDir": "lib"`と、`"declaration": true`を設定します < これは宣言ファイルとjsファイルをlibフォルダに生成します
  * `include：["./src / ** / *"]`を設定します < これは`src`ディレクトリからのすべてのファイルを対象に含めます

* `package.json`について
  * `"main"： "lib/index"` <これはNode.jsに`lib/index.js`をロードするように指示します
  * `"types"： "lib/index"` <これはTypeScriptに`lib/index.d.ts`をロードするように指示します


パッケージの例：
* `npm install typestyle` [for TypeStyle](https://www.npmjs.com/package/typestyle)
* 使用法：`import { style } from 'typestyle';`は、完全な型安全性を提供します

MORE:

* あなたのパッケージが他のTypeScriptで作られたパッケージに依存している場合は、そのまま生のJSパッケージと同様に`dependencies`/`devDependencies`/ `peerDependencies`に入れてください
* パッケージが他のJavaScript作成パッケージに依存していて、プロジェクトで型安全性を使用する場合は、それらの型定義(`@types/foo`など)を`devDependencies`に入れます。JavaScriptの型は、主なNPMの流れの*範囲外で*管理する必要があります。JavaScriptのエコシステムでは、セマンティックなバージョン管理が行われていない場合、型をあまりにも簡単に壊すので、ユーザーが型を必要とする場合は、それらに対応する`@types/foo`のバージョンをインストールする必要があります。

## ボーナスポイント

そのようなNPMモジュールは、browserify(tsifyを使用)またはwebpack(ts-loaderを使用)でうまく動作します。
