# なぜサイプレス
Cypressは素晴らしいE2Eテストツールです。これを考慮する大きな理由は次のとおりです。

* 隔離設置が可能です。
* TypeScriptの定義がそのままの状態で出荷されます。
* 優れたインタラクティブなGoogle Chromeのデバッグ環境を提供します。これは、UI開発者がほとんど手動で作業する方法と非常によく似ています。
* アプリケーションコードを変更することなく、バックエンドのXHRを簡単に模倣して観察する機能を提供します（以下のヒントで詳しく説明しています）。
* より脆弱なテストでより意味のあるデバッグ経験を提供するための暗黙のアサーションがあります（これについては以下のヒントを参照してください）。

## インストール

e2eディレクトリを作成し、cypressとその依存関係をTypeScript変換用にインストールします。

```sh
mkdir e2e
cd e2e
npm init -y
npm install cypress webpack @cypress/webpack-preprocessor typescript ts-loader
```

> ここでは特にサイプレスのために別々の `e2e`フォルダを作成するいくつかの理由があります：
* 別のディレクトリや `e2e`を作成すると、`package.json`の依存関係を他のプロジェクトと簡単に分離することができます。これにより依存性の競合が少なくなります。
* テストフレームワークには、グローバルな名前空間を「記述する」、「期待する」などのもので汚染する習慣があります。グローバルな型定義の競合を避けるために、e2e `tsconfig.json`と`node_modules`をこの特別な `e2e`フォルダに保存することが最善です。

セットアップタイプスクリプト `tsconfig.json`

```json
{
  "compilerOptions": {
    "strict": true,
    "sourceMap": true,
    "module": "commonjs",
    "target": "es5",
    "lib": [
      "dom",
      "es6"
    ],
    "jsx": "react",
    "experimentalDecorators": true
  },
  "compileOnSave": false
}
```

サイプレスの最初の乾いたランを行い、サイプレスのフォルダ構造を準備します。 Cypress IDEが開きます。ウェルカムメッセージが表示されたらそれを閉じることができます。

```sh
npx cypress open
```

`e2e / cypress / plugins / index.js`を次のように編集して、サイクロプスをタイプライティングするためのサイプレスをセットアップします：

```js
const wp = require('@cypress/webpack-preprocessor')
module.exports = (on) => {
  const options = {
    webpackOptions: {
      resolve: {
        extensions: [".ts", ".tsx", ".js"]
      },
      module: {
        rules: [
          {
            test: /\.tsx?$/,
            loader: "ts-loader",
            options: { transpileOnly: true }
          }
        ]
      }
    },
  }
  on('file:preprocessor', wp(options))
}
```


オプションで `e2e / package.json`ファイルにいくつかのスクリプトを追加します：

```json
  "scripts": {
    "cypress:open": "cypress open",
    "cypress:run": "cypress run"
  },
```

## キーファイルの詳細説明
`e2e`フォルダの下に、次のファイルがあります：

* `/ cypress.json`：サイプレスを設定します。デフォルトは空で、必要なのはそれだけです。
* `/ cypress`サブフォルダ：
    * `/ fixtures`：テストフィクスチャ
        * `example.json`が付属しています。削除しても構いません。
        *単純な `.json`ファイルを作成して、複数のテストでの使用にサンプルデータ（別名フィクスチャ）を提供することができます。
    * `/ integration`：すべてのテスト。
        * `examples`フォルダがあります。安全に削除することができます。
        * `.spec.ts`での名前テスト`何か.spec.ts`。
        *組織の改善のため、サブフォルダの下でテストを作成することは自由です。 `/ someFeatureFolder / something.spec.ts`です。

## 最初のテスト
* 次の内容の `/ cypress / integration / first.spec.ts`ファイルを作成します：

```ts
/// <reference types="cypress"/>

describe('google search', () => {
  it('should work', () => {
    cy.visit('http://www.google.com');
    cy.get('#lst-ib').type('Hello world{enter}')
  });
});
```

## 開発中のランニング
次のコマンドを使用してcypress IDEを開きます。

```sh
npm run cypress:open
```

実行するテストを選択します。

## ビルドサーバーで実行する

ciモードでサイプレステストを実行するには、次のコマンドを使用します。

```sh
npm run cypress:run
```

## ヒント：UIとテストの間でコードを共有する
Cypressテストはコンパイル/パックされ、ブラウザで実行されます。プロジェクトコードを自由にテストにインポートしてください。

たとえば、UIセレクタとテストの間でID値を共有して、CSSセレクタが壊れないようにすることができます。

```ts
import { Ids } from '../../../src/app/constants'; 

// Later 
cy.get(`#${Ids.username}`)
  .type('john')
```

## ヒント：暗黙のアサーション
サイプレスコマンドが失敗したときには、（他の多くのフレームワークでは `null`のようなものではなく）素晴らしいエラーが発生するので、すばやく失敗し、テストが失敗したときを正確に知ることができます。

```
cy.get('#foo') 
// If there is no element with id #foo cypress will wait for 4 seconds automatically 
// If still not found you get an error here ^ 
// \/ This will not trigger till an element #foo is found
  .should('have.text', 'something') 
```

## ヒント：明示的なアサーション
Cypressには、ウェブ用のいくつかのアサーションヘルプが付属しています。 chai-jquery https://docs.cypress.io/guides/references/assertions.html#Chai-jQuery chainerに文字列として渡す `.should`コマンドでそれらを使用します。

```
cy.get('#foo') 
  .should('have.text', 'something') 
```

## ヒント：コマンドと連鎖
cypressチェーン内のすべての関数呼び出しは `command`です。 `should`コマンドはアサーションです。チェーンとアクションの別々の*カテゴリ*を別々に開始することは従来通りです。

```ts
// Don't do this 
cy.get(/**something*/) 
  .should(/**something*/)
  .click()
  .should(/**something*/)
  .get(/**something else*/) 
  .should(/**something*/)

// Prefer seperating the two gets 
cy.get(/**something*/) 
  .should(/**something*/)
  .click()
  .should(/**something*/)

cy.get(/**something else*/) 
  .should(/**something*/)
```

コードを評価して同時に実行する他のライブラリ*。これにより、セレクタとアサーションが混在してデバッグするのが難しいかもしれない単一のチェーンが必要になります。

サイプレスコマンドは、本質的に、コマンドを後で実行するためのサイプレスランタイムへの*宣言*です。簡単な言葉：サイプレスはそれをより簡単にします。

## ヒント：HTTPリクエストを待っています
アプリケーションが作るXHRに必要なすべてのタイムアウトが原因で、多くのテストが脆弱です。 `cy.server`は簡単に
* バックエンド呼び出しのエイリアスを作成する
* それらが起こるのを待つ

例えば

```ts
cy.server()
  .route('POST', 'https://example.com/api/application/load')
  .as('load') // create an alias

// Start test
cy.visit('/')

// wait for the call
cy.wait('@load') 

// Now the data is loaded
```

## ヒント：HTTPリクエストレスポンスを嘲笑
`route`を使ってリクエストレスポンスを簡単に模倣することもできます：
```ts
cy.server()
  .route('POST', 'https://example.com/api/application/load', /* Example payload response */{success:true})
```

## ヒント：モッキング時間
`wait`を使ってある時間テストを一時停止することができます。自動的に「ログアウトしようとしています」という通知画面をテストする：

```ts
cy.visit('/');
cy.wait(waitMilliseconds);
cy.get('#logoutNotification').should('be.visible');
```

しかし、 `cy.tcl`を使用して`cy.clock`と転送時間を使って時間をモックすることが推奨されます。

```ts
cy.clock();

cy.visit('/');
cy.tick(waitMilliseconds);
cy.get('#logoutNotification').should('be.visible');
```

## ヒント：スマートディレイ
サイプレスは自動的に多くの非同期のものを待つでしょう。
```
// If there is no request against the `foo` alias cypress will wait for 4 seconds automatically 
cy.wait('@foo') 
// If there is no element with id #foo cypress will wait for 4 seconds automatically 
cy.get('#foo')
```
これにより、テストコードフローに常に任意のタイムアウトを追加する必要がなくなります。

## リソース
* ウェブサイト：https://www.cypress.io/
* あなたの最初のサイプレステストを書く（サイプレスIDEの素晴らしいツアーを与える）：https://docs.cypress.io/guides/getting-started/writing-your-first-test.html
* CI環境を設定する（例えば、 `cypress run`でボックスの外で動く提供されたドッカー画像）：https://docs.cypress.io/guides/guides/continuous-integration.html
* レシピ（説明付きのレシピを一覧表示します。レシピのソースコードに移動するには見出しをクリックしてください）：https://docs.cypress.io/examples/examples/recipes.html
