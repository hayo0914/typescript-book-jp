# React クイックスタート

## ブラウザでのTypeScript

TypeScriptを使用してWebアプリケーションを作成している場合は、簡単なTypeScript + React\(私が選ぶUIフレームワーク\)のプロジェクトのセットアップを取得することをお勧めします。

### 一般的なマシンのセットアップ

* [Node.js](https://nodejs.org/ja/download/)をインストールする
* [Git](https://git-scm.com/downloads)をインストールする

### 素早くプロジェクトをセットアップする

ベースとして [https://github.com/basarat/react-typescript](https://github.com/basarat/react-typescript) を使用してください。

```text
git clone https://github.com/basarat/react-typescript.git
cd react-typescript
npm install
```

ここで、 [あなたのすばらしいアプリケーションを開発する](browser.md#あなたのすばらしいアプリケーションを開発する) にジャンプしてください。

### プロジェクトの詳細設定

そのプロジェクトがどのように作成されたかは下記の通りです。

* プロジェクトのディレクトリを作成する：

```text
mkdir your-project
cd your-project
```

* `tsconfig.json`を作成する：

```javascript
{
  "compilerOptions": {
    "sourceMap": true,
    "module": "commonjs",
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "experimentalDecorators": true,
    "target": "es5",
    "jsx": "react",
    "lib": [
      "dom",
      "es6"
    ]
  },
  "include": [
    "src"
  ],
  "compileOnSave": false
}
```

* `package.json`を作成する:

```javascript
{
  "name": "react-typescript",
  "version": "0.0.0",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/basarat/react-typescript.git"
  },
  "scripts": {
    "build": "webpack -p",
    "start": "webpack-dev-server -d --content-base ./public"
  },
  "dependencies": {
    "@types/react": "16.4.10",
    "@types/react-dom": "16.0.7",
    "clean-webpack-plugin": "0.1.19",
    "html-webpack-plugin": "3.2.0",
    "react": "16.4.2",
    "react-dom": "16.4.2",
    "ts-loader": "4.4.2",
    "typescript": "3.0.1",
    "webpack": "4.16.5",
    "webpack-cli": "3.1.0",
    "webpack-dev-server": "3.1.5"
  }
}
```

* すべてのリソースを含む単一の`app.js`ファイルにモジュールをバンドルするための`webpack.config.js`を作成する:

```javascript
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './src/app/app.tsx',
  plugins: [
    new CleanWebpackPlugin({
      cleanAfterEveryBuildPatterns: ['public/build']
    }),
    new HtmlWebpackPlugin({
      template: 'src/templates/index.html'
    }),
  ],
  output: {
    path: __dirname + '/public',
    filename: 'build/[name].[contenthash].js'
  },
  resolve: {
    extensions: ['.ts', '.tsx', '.js']
  },
  module: {
    rules: [
      { test: /\.tsx?$/, loader: 'ts-loader' }
    ]
  }
}
```

* webpackが生成するindex.htmlのテンプレートとして使われる`src/templates/index.html`ファイルです。生成されたファイルは`public`フォルダに配置され、Webサーバーを通じてサーブされます：

```markup
<html>
  <body>
      <div id="root"></div>
  </body>
</html>
```

あなたのフロントエンドアプリケーションのエントリポイントである`src/app/app.tsx`：

```typescript
import * as React from 'react';
import * as ReactDOM from 'react-dom';

const Hello: React.FunctionComponent<{ compiler: string, framework: string }> = (props) => {
  return (
    <div>
      <div>{props.compiler}</div>
      <div>{props.framework}</div>
    </div>
  );
}

ReactDOM.render(
  <Hello compiler="TypeScript" framework="React" />,
  document.getElementById("root")
);
```

## あなたのすばらしいアプリケーションを開発する <a id="&#x3042;&#x306A;&#x305F;&#x306E;&#x3059;&#x3070;&#x3089;&#x3057;&#x3044;&#x30A2;&#x30D7;&#x30EA;&#x30B1;&#x30FC;&#x30B7;&#x30E7;&#x30F3;&#x3092;&#x958B;&#x767A;&#x3059;&#x308B;"></a>

> 最新のパッケージを入手するには`npm install typescript@latest react@latest react-dom@latest @types/react@latest @types/react-dom@latest webpack@latest webpack-dev-server@latest webpack-cli@latest ts-loader@latest clean-webpack-plugin@latest html-webpack-plugin@latest --save-exact`を実行してください。

* `npm start`を実行してライブ開発を行います
  * [http://localhost:8080](http://localhost:8080) を参照してください
  * `src/app/app.tsx`\(または`src/app/app.tsx`に使われるts/tsxファイル\)を編集すれば、サーバーがライブリロードします
  * `src/templates/index.html`を編集すれば、サーバーがライブリロードします
* `npm run build`を実行して本番用のアセットをビルドします
  * Webサーバーを通じて`public`フォルダ\(ビルドされたアセットが配置される\)をサーブします

