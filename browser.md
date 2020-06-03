# React クイックスタート

1. 手動でTypeScriptのプロジェクトをセットアップする場合と、2.Create React Appのテンプレートを利用する場合の両方について説明します。

## 1. ブラウザでのTypeScript

TypeScriptを使用してWebアプリケーションを作成する場合は、簡単なTypeScript + React\(UIフレームワーク\)のプロジェクトのセットアップを作成することをお勧めします。

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

* webpackが生成するindex.htmlのテンプレートとして使われる`src/templates/index.html`ファイルです。生成されたファイルは`public`フォルダに配置され、Webサーバーから提供されます：

```markup
<html>
  <body>
      <div id="root"></div>
  </body>
</html>
```

アプリケーションのエントリポイントである`src/app/app.tsx`は以下の通りです：

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

### すばらしいアプリケーションを開発するワークフロー

> 最新のパッケージを入手するには`npm install typescript@latest react@latest react-dom@latest @types/react@latest @types/react-dom@latest webpack@latest webpack-dev-server@latest webpack-cli@latest ts-loader@latest clean-webpack-plugin@latest html-webpack-plugin@latest --save-exact`を実行してください。

* `npm start`を実行してライブ開発を行います
  * [http://localhost:8080](http://localhost:8080) を参照してください
  * `src/app/app.tsx`\(または`src/app/app.tsx`に使われるts/tsxファイル\)を編集すれば、サーバーがLive Reloadします
  * `src/templates/index.html`を編集すれば、サーバーがLive Reloadします
* `npm run build`を実行して本番用のアセットをビルドします
  * Webサーバーを通じて`public`フォルダ\(ビルドされたアセットが配置される\)をサーブします


## 2. Create React Appの利用

TypeScriptを使用してReactのWebアプリケーションを作成する場合、最も一般的な方法は、[Create React App](https://github.com/facebook/create-react-app)を使うことです。このツールはReactの開発チームがメンテナンスを行っているツールです。公式にTypeScriptのテンプレートが提供されています。

### 簡単にプロジェクトをセットアップする

まず、Create React Appをインストールします。npmを利用して、`npm i -g create-react-app`というコマンドでローカルPCにグローバルにインストールできます。

Create React Appのインストールができたら、[Reactの公式Webサイト](https://reactjs.org/docs/static-type-checking.html#using-typescript-with-create-react-app)に書かれているように`npx create-react-app my-app --template typescript`というコマンドを実行します。`my-app`の部分には、プロジェクトに利用するフォルダ名を指定します。これで、最初からTypeScriptを利用可能なプロジェクトを簡単に作成できます。

```text
npm i -g create-react-app
npx create-react-app my-app --template typescript
cd my-app
npm start # または、yarn start
```

これで、開発用サーバが起動し、 [http://localhost:3000/](http://localhost:3000/) にアクセスして動作を確認しながら、開発を進めることができます。この開発用サーバーは、ファイルの更新を監視しているので、TypeScriptのコードを変更すれば、自動的にコンパイルされ、ブラウザがリロードされます。この仕組みをLive Reloadや、Hot Reloadと呼びます。

### プロジェクトの詳細設定

Create React Appでプロジェクトを作成すると、下記のような`tsconfig.json`が作成されます。これを必要に応じて修正し、TypeScriptのコンパイラの動作を、好みに合わせて調整することができます。

```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": [
      "dom",
      "dom.iterable",
      "esnext"
    ],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react"
  },
  "include": [
    "src"
  ]
}
```

## プロジェクトのビルド

`npm run build` または `yarn build` のコマンドで、本番環境用のビルドを実行できます。これで、Reactチームによって本番環境に最適化されたバンドルファイルを出力できます。
