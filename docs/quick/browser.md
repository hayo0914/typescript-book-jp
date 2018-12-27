# ブラウザでのTypeScript

TypeScriptを使用してWebアプリケーションを作成している場合は、簡単なTypeScript + React(私が選ぶUIフレームワーク)のプロジェクトのセットアップを取得することをお勧めします。

## 一般的なマシンのセットアップ

* [Node.js](https://nodejs.org/ja/download/)をインストールする
* [Git](https://git-scm.com/downloads)をインストールする

## 素早くプロジェクトをセットアップする
ベースとして [https://github.com/basarat/react-typescript](https://github.com/basarat/react-typescript) を使用してください。

```
git clone https://github.com/basarat/react-typescript.git
cd react-typescript
npm install
```

ここで、 [あなたのすばらしいアプリケーションを開発する](#あなたのすばらしいアプリケーションを開発する) にジャンプしてください。

## プロジェクトの詳細設定
そのプロジェクトがどのように作成されたかは下記の通りです。

* プロジェクトのディレクトリを作成する：

```
mkdir your-project
cd your-project
```

* `tsconfig.json`を作成する：

```json
{
  "compilerOptions": {
    "sourceMap": true,
    "module": "commonjs",
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

```json
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
    "@types/react": "16.4.2",
    "@types/react-dom": "16.0.6",
    "react": "16.4.1",
    "react-dom": "16.4.1",
    "ts-loader": "4.4.1",
    "typescript": "2.9.2",
    "webpack": "4.12.1",
    "webpack-cli": "3.0.8",
    "webpack-dev-server": "3.1.4"
  }
}
```

* すべてのリソースを含む単一の`app.js`ファイルにモジュールをバンドルするための`webpack.config.js`を作成する:

```js
module.exports = {
  entry: './src/app/app.tsx',
  output: {
    path: __dirname + '/public',
    filename: 'build/app.js'
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

* webpackが生成するindex.htmlのテンプレートとして使われる`src/templates/index.html`ファイルです。生成されたファイルは`public`フォルダに配置され、Webサーバを通じてサーブされます：

```html
<html>
  <body>
      <div id="root"></div>
      <script src="./build/app.js"></script>
  </body>
</html>
```

あなたのフロントエンドアプリケーションのエントリポイントである`src/app/app.tsx`：

```js
import * as React from 'react';
import * as ReactDOM from 'react-dom';

const Hello: React.SFC<{ compiler: string, framework: string }> = (props) => {
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

# あなたのすばらしいアプリケーションを開発する {#あなたのすばらしいアプリケーションを開発する}

> 最新のパッケージを入手するには`npm install typescript@latest react@latest react-dom@latest @types/react@latest @types/react-dom@latest webpack@latest webpack-dev-server@latest webpack-cli@latest ts-loader@latest clean-webpack-plugin@latest html-webpack-plugin@latest --save-exact`を実行してください。

* `npm start`を実行してライブ開発を行います
    *  [http://localhost:8080](http://localhost:8080) を参照してください
    * `src/app/app.tsx`(または`src/app/app.tsx`に使われるts/tsxファイル)を編集すれば、サーバーがライブリロードします
    * `src/templates/index.html`を編集すれば、サーバーがライブリロードします
* `npm run build`を実行して本番用のアセットをビルドします
    * Webサーバを通じて`public`フォルダ(ビルドされたアセットが配置される)をサーブします
