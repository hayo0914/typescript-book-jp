# タイプスクリプトをブラウザに

TypeScriptを使用してWebアプリケーションを作成している場合は、クイックTypeScript + React（自分のUIフレームワークを選択）プロジェクトセットアップを取得することをお勧めします。

## 一般的なマシンセットアップ

* [Node.js]をインストールする（https://nodejs.org/ja/download/）
* [Git]（https://git-scm.com/downloads）をインストールする

## プロジェクトセットアップのクイック
ベースとして[https://github.com/basarat/react-typescript](https://github.com/basarat/react-typescript）]を使用してください。

```
git clone https://github.com/basarat/react-typescript.git
cd react-typescript
npm install
```

今すぐ[あなたのすばらしいアプリケーションを開発する]にジャンプしてください（#あなたのすばらしいアプリケーションを開発する）

## プロジェクトの詳細設定
そのプロジェクトがどのように作成されたかを見るには、下記の通りです。

* プロジェクトディレクトリを作成する：

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

* `package.json`を作成します。

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

* すべてのリソースを含む単一の `app.js`ファイルにモジュールをバンドルする`webpack.config.js`を作成します：

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

* あなたのウェブサーバから提供される `public / index.html`ファイル：

```html
<html>
  <body>
      <div id="root"></div>
      <script src="./build/app.js"></script>
  </body>
</html>
```

あなたのフロントエンドアプリケーションのエントリポイントである `src / app / app.tsx`：

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

# すばらしいアプリケーションを開発する

> 最新のパッケージを入手するには `npm install typescript @ latest react @最新のreact-dom @ latest @ types / react @ latest @ types / react-dom @最新webpack @最新ts-loader @最新webpack-dev-server @最新のwebpack-cli @ latest --save-exact`

* `npm start`を実行してライブ開発を行います。
    * [http：// localhost：8080]（http：// localhost：8080）を参照してください。
    * `app.tsx`（または`src`のts / tsxファイル）とアプリケーションライブリロードを編集します。
* `npm run build`を実行して生産アセットを構築します。
    *あなたのサーバから `public`フォルダ（構築されたアセットを含む）を提供します。
