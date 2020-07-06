# Why Cypress
Cypressは素晴らしいE2Eテストツールです。これを考慮する大きな理由は次のとおりです。

* 分離インストールが可能です
* TypeScriptの定義がそのままの状態で使えます
* 優れたインタラクティブなGoogle Chromeのデバッグ環境を提供します。これは、UI開発者が手動で作業する方法と非常によく似ています
* より強力なデバッグとテストの安定性を実現するコマンド実行セパレーションを持っています（詳細は後述）
* より脆いテストでより意味のあるデバッグエクスペリエンスを提供するための暗黙のアサーションがあります（詳細は以下のヒントを参照してください）。
* アプリケーションコードを変更することなく、バックエンドのXHRを簡単に模倣して観察する機能を提供します(以下のヒントで詳しく説明しています)。

## インストール

このインストールプロセスで提供される手順は、あなたの組織のボイラープレートとして使用できる素敵なe2eフォルダを提供します。

> 同じ手順を私の [youtubeチャンネル](https://www.youtube.com/watch?v=n3SvvZSWwfM)で動画で紹介しています。

e2eディレクトリを作成し、cypress、TypeScriptをインストールし、typescriptとcypressの設定ファイルを追加します。

```sh
mkdir e2e
cd e2e
npm init -y
npm install cypress typescript
npx tsc --init --types cypress --lib dom,es6
echo {} > cypress.json
```

> ここでは特にサイプレスのために別々の`e2e`フォルダを作成するいくつかの理由があります：
* 別のディレクトリや`e2e`を作成すると、`package.json`の依存関係を他のプロジェクトと簡単に分離することができます。これにより依存性の競合が少なくなります。
* テストフレームワークには、グローバルな名前空間を`describe` `it` `expect`などのもので汚染する慣習があります。グローバルな型定義の競合を避けるために、e2e `tsconfig.json`と`node_modules`をこの特別な`e2e`フォルダに保存することが最善です。

`e2e/package.json`ファイルにいくつかのスクリプトを追加します：

```json
  "scripts": {
    "cypress:open": "cypress open",
    "cypress:run": "cypress run"
  },
```

最初のテストを`cypress/integration/basic.ts`に書きます:

```ts
it('should perform basic google search', () => {
  cy.visit('https://google.com');
  cy.get('[name="q"]')
    .type('subscribe')
    .type('{enter}');
});
```

開発中は`npm run cypress:open`を、ビルドサーバーを起動するには`npm run cypress:run`を実行してください🌹

## キーとなるファイルの詳細
`e2e`フォルダの下に、次のファイルがあります：

* `/cypress.json`：Cypressを設定します。デフォルトは空で、必要なのはそれだけです。
* `/cypress`サブフォルダ：
    * `/integration`：あなたのすべてのテスト
        * より良い構成を作るためにサブフォルダの下にテストを作成することは自由です。例:`/someFeatureFolder/something.spec.ts`

## 最初のテスト
* 次の内容の`/cypress/integration/first.ts`ファイルを作成します：

```ts
describe('google search', () => {
  it('should work', () => {
    cy.visit('http://www.google.com');
    cy.get('#lst-ib').type('Hello world{enter}')
  });
});
```

## 開発中に実行する
次のコマンドを使用してcypress IDEを開きます。

```sh
npm run cypress:open
```

実行するテストを選択します。

## ビルドサーバーで実行する

ciモードでCypressテストを実行するには、次のコマンドを使用します。

```sh
npm run cypress:run
```

## ヒント: UIとテストの間でコードを共有する
Cypressテストはコンパイル/パックされ、ブラウザで実行されます。プロジェクトコードを自由にテストにインポートしてください。

たとえば、UIセレクタとテストの間でID値を共有して、CSSセレクタが壊れないようにすることができます。

```ts
import { Ids } from '../../../src/app/constants';

// Later
cy.get(`#${Ids.username}`)
  .type('john')
```

## ヒント: ページオブジェクトの作成

さまざまなテストがページで行う必要があるすべてのインタラクションに対して便利なハンドルを提供するオブジェクトを作成することは、一般的なテストの慣例です。getterとメソッドでTypeScriptクラスを使用してページオブジェクトを作成できます。

```ts
import { Ids } from '../../../src/app/constants';

class LoginPage {
  visit() {
    cy.visit('/login');
  }

  get username() {
    return cy.get(`#${Ids.username}`);
  }
}
const page = new LoginPage();

// Later
page.visit();

page.username.type('john');

```

## ヒント: 明示的なアサーション
Cypressには、ウェブ用のほんのいくつかのアサーションヘルプが付属しています。例えば、chai-jquery https://docs.cypress.io/guides/references/assertions.html#Chai-jQuery です。 それらを使うには、`.should`コマンドを使用して、chainerに文字列として渡します:

```
cy.get('#foo')
  .should('have.text', 'something')
```
> You get intellisense for `should` chainers as cypress ships with correct TypeScript definitions 👍🏻

The complete list of chainers is available here : https://docs.cypress.io/guides/references/assertions.html

If you want something complex you can even use `should(callback)` and e.g.

```
cy.get('div')
  .should(($div) => {
    expect($div).to.have.length(1);
    expect($div[0].className).to.contain('heading');
  })
// これは単なる例です。普通は`.should('have.class', 'heading')`のように書きます。
```

> ヒント: cypressにはcallbackの呼び出しにも自動リトライ機能があるため、普通の文字列のチェーンと同じように壊れにくいコードを書くことができます。

## ヒント: コマンドとチェーン
cypressチェーン内のすべての関数呼び出しは`command`です。`should`コマンドはアサーションです。チェーンとアクションの別々の*カテゴリ*を別々に開始することは慣習になっています:

```ts
// Don't do this
cy.get(/**something*/)
  .should(/**something*/)
  .click()
  .should(/**something*/)
  .get(/**something else*/)
  .should(/**something*/)

// Prefer separating the two gets
cy.get(/**something*/)
  .should(/**something*/)
  .click()
  .should(/**something*/)

cy.get(/**something else*/)
  .should(/**something*/)
```

他の何かのライブラリは、同時にこのコードを評価し、実行します。それらのライブラリは、単一のチェーンが必要になります。それはセレクタやアサーションが混在してデバッグを行うのが難しくなります。

Cypressのコマンドは、本質的に、コマンドを後で実行するためのCypressランタイムへの*宣言*です。端的な言葉：Cypressはより簡単にします

## ヒント: より容易なクエリのために`contains`を使う

下記に例を示します:
```ts
cy.get('#foo')
  // Once #foo is found the following:
  .contains('Submit')
  .click()
  // ^ will continue to search for something that has text `Submit` and fail if it times out.
  // ^ After it is found trigger a click on the HTML Node that contained the text `Submit`.
```

## ヒント: スマートディレイとリトライ
Cypressはたくさんの非同期のものに対して、自動的に待ち(そしてリトライし)ます。
```
// If there is no request against the `foo` alias cypress will wait for 4 seconds automatically
cy.wait('@foo')
// If there is no element with id #foo cypress will wait for 4 seconds automatically and keep retrying
cy.get('#foo')
```
これにより、テストコードフローに常に任意のタイムアウトのロジックを追加する必要がなくなります。

## ヒント: 暗黙のアサーション
Cypressには暗黙のアサーションという概念があります。1つ前のコマンドが原因でそれ移行のコマンドでエラーが発生したときに実行されます。These kick in if a future command is erroring because of a previous command. E.g. the following will error at `contains` (after automatic retries of course) as nothing found can get `click`ed:

```ts
cy.get('#foo')
  // Once #foo is found the following:
  .contains('Submit')
  .click()
  // ^ Error: #foo does not have anything that `contains` `'Submit'`
```

伝統的なフレームワークでは、`null`には`click`がないというような恐ろしいエラーを目にすることでしょう。Cypressの場合、`#foo`には`Submit`が含まれていないという親切なエラーが表示されます。このようなエラーは暗黙のアサーションの一種です。

## ヒント:  HTTPリクエストを待つ
アプリケーションが作るXHRに必要なすべてのタイムアウトが原因となり、多くのテストが脆くなりました。`cy.server`は次のことを簡単にします。
* バックエンド呼び出しのエイリアスを作成する
* それらが発生するのを待つ

例:

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

## ヒント: HTTPリクエストのレスポンスをモックする
`route`を使ってリクエストのレスポンスを簡単にモックすることもできます：

```ts
cy.server()
  .route('POST', 'https://example.com/api/application/load', /* Example payload response */{success:true});
```

### ヒント: HTTPリクエストのレスポンスをアサートする
リクエストのアサートは、モックを作らなくても`route`や`onRequest`/`onResponse`を使うことで実現できます。

```ts
cy.route({
  method: 'POST',
  url: 'https://example.com/api/application/load',
  onRequest: (xhr) => {
    // Example assertion
    expect(xhr.request.body.data).to.deep.equal({success:true});
  }
})
```

## ヒント: 時間をモックする
`wait`を使ってある時間テストを一時停止することができます。自動的に"あなたはログアウトされます"という通知画面をテストする例：

```ts
cy.visit('/');
cy.wait(waitMilliseconds);
cy.get('#logoutNotification').should('be.visible');
```

しかし、`cy.clock`と時間をモックし、`cy.tcl`を使用して時間を前倒しすることが推奨されます:

```ts
cy.clock();

cy.visit('/');
cy.tick(waitMilliseconds);
cy.get('#logoutNotification').should('be.visible');
```

## ヒント: アプリケーションコードのユニットテスト
あなたはCypressを使ってアプリケーションコードを分離してユニットテストを行うことも可能です。

```ts
import { once } from '../../../src/app/utils';

// Later
it('should only call function once', () => {
  let called = 0;
  const callMe = once(()=>called++);
  callMe();
  callMe();
  expect(called).to.equal(1);
});
```

## ヒント: ユニットテストにおけるモック
もしあなたがアプリケーショのモジュールをユニットテストしていたら、あなたは`cy.stub`を使ってモックを提供することが可能です。例えば、あなたは`navigate`が関数`foo`で呼ばれることを確認できます:

* `foo.ts`

```ts
import { navigate } from 'takeme';

export function foo() {
  navigate('/foo');
}
```

* 下記を`some.spec.ts`で行います

```ts
/// <reference types="cypress"/>

import { foo } from '../../../src/app/foo';
import * as takeme from 'takeme';

describe('should work', () => {
  it('should stub it', () => {
    cy.stub(takeme, 'navigate');
    foo();
    expect(takeme.navigate).to.have.been.calledWith('/foo');
  })
});
```

## ヒント: コマンド - 実行の分離
たとえば、`cy.get('#something')`のようなCypressのコマンド(またはアサーション)を呼び出したとき、関数は実際には何もアクションを行わずに即座に返ります。実際に関数が行うのは、Cypressのテストランナーに対して、あるアクション(この場合は`get`)をある時点で実行する必要があると伝えることです。

あなたが行うことは、基本的には、ランナーが将来実行することになるコマンドリストを書くことになります。このようにコマンドと実行が分離されていることは、次のようなシンプルなテストを書くことで確かめることができます。このテストを実行すると、ランナーがコマンドを*実行*する前に、`start / between / end`の`console.log`文がすぐに実行されることがわかります。

```ts
/// <reference types="cypress"/>

describe('Hello world', () => {
  it('demonstrate command - execution separation', () => {
    console.log('start');
    cy.visit('http://www.google.com');
    console.log('between');
    cy.get('.gLFyf').type('Hello world');
    console.log('end');
  });
});
```

このようなコマンドの実行の分離を行うことには、2つの利点があります。
* ランナーがコマンドを実行するときに、*脆さに耐えられる*やり方で自動リトライや暗黙のアサーションを実行できる。
* 非同期に書くコードを同期的に書くことができるため、コードのメンテナンスが難しくなってしまう常に*チェーンする*ような書き方をする必要がなくなる。

## ヒント: ブレークポイント
Cypressテストによって生成された自動スナップショット+コマンドログは、デバッグに最適です。とはいえ、それは、あなたが望むならテストの実行を一時停止できます。

まずChrome Developer Tools(愛情を込めてdev toolsと呼ばれています)をテストランナー(macでは`CMD + ALT + i`/windowsでは`F12`)で開いていることを確認してください。一度dev toolsを開けば、あなたはテストをリランすることができ、dev toolsは開いたままになります。もしdev toolsを開いていれば、あなたは2つの方法でテストを実行できます:

* アプリケーションコードのブレークポイント: `debugger`文をアプリケーションのコードを使うと、テストランナーは通常のweb開発のように、ちょうどそこで停止します。
* テストコードのブレークポイント: あなたは`.debug()`コマンドを使い、cypressのテスト実行をそこで停止できます。例えば、`.then(() => { debugger })`です。あなたはいくつかのエレメントを得ること(`cy.get('#foo').then(($ /* a reference to the dom element */) => { debugger; })`)や、ネットワーク呼び出し(`cy.request('https://someurl').then((res /* network response */) => { debugger });`)すら可能です。しかし、慣用的な方法は、`cy.get('#foo').debug()`です。そして、テストランナーが`debug`で止まったときに、`get`をコマンドログでクリックすると自動的に`console.log`にあなたが知りたい`.get('#foo')`に関する情報が出力されます(そして、デバッグに必要な他のコマンドでも似たようなものです)

## ヒント: サーバーを開始してテストを実行する
もしテストの前にローカルサーバーを起動したい場合は`start-server-and-test` [https://github.com/bahmutov/start-server-and-test](https://github.com/bahmutov/start-server-and-test) を依存関係に追加できます。それは次の引数を受け取ります。
* サーバーを実行するためのnpmスクリプト
* サーバーが起動しているかをチェックするためのエンドポイント
* テストを初期化するためのnpmスクリプト

package.jsonの例:
```json
{
    "scripts": {
        "start-server": "npm start",
        "run-tests": "mocha e2e-spec.js",
        "ci": "start-server-and-test start-server http://localhost:8080 run-tests"
    }
}
```

## リソース
* ウェブサイト：https://www.cypress.io/
* あなたの最初のCypressテストを書く(Cypress IDEの素晴らしいツアー)：https://docs.cypress.io/guides/getting-started/writing-your-first-test.html
* CI環境を設定する(例えば、そのまま`cypress run`で動く提供されたdockerイメージ)：https://docs.cypress.io/guides/guides/continuous-integration.html
* レシピ(説明付きのレシピの一覧です。レシピのソースコードに移動するには見出しをクリックしてください): https://docs.cypress.io/examples/examples/recipes.html
* Visual Testing: https://docs.cypress.io/guides/tooling/visual-testing.html
* Optionally set a `baseUrl` in cypress.json to [prevent an initial reload that happens after first `visit`.](https://github.com/cypress-io/cypress/issues/2542)
* Code coverage with cypress: [Webcast](https://www.youtube.com/watch?v=C8g5X4vCZJA)
