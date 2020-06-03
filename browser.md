# React クイックスタート

## ブラウザでのTypeScript

TypeScriptを使用してReactのWebアプリケーションを作成する場合、最も一般的な方法は、[Create React App](https://github.com/facebook/create-react-app)を使うことです。このツールはReactの開発チームがメンテナンスを行っているツールです。公式にTypeScriptのテンプレートが提供されています。


### 一般的なマシンのセットアップ

* [Node.js](https://nodejs.org/ja/download/)をインストールする。npmを利用するには、Node.jsをインストールする必要があります

### 素早くプロジェクトをセットアップする

まず、Create React Appをインストールします。npmを利用して、`npm i -g create-react-app`というコマンドでローカルPCにグローバルにインストールできます。

Create React Appのインストールができたら、[Reactの公式Webサイト](https://reactjs.org/docs/static-type-checking.html#using-typescript-with-create-react-app)に書かれているように`npx create-react-app my-app --template typescript`というコマンドを実行します。`my-app`の部分には、プロジェクトに利用するフォルダ名を指定します。これで、最初からTypeScriptを利用可能なプロジェクトを簡単に作成できます。

```text
npm i -g create-react-app
npx create-react-app my-app --template typescript
cd my-app
npm start # または、yarn start
```

これで、開発用サーバが起動し、 [http://localhost:3000/](http://localhost:3000/) にアクセスして動作を確認しながら、開発を進めることができます。

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
