## 外部モジュール(External modules)
TypeScriptの外部モジュールパターンには大きなパワーと利便性があります。ここでは、そのパワーと実際の用途を知るためのパターンについて説明します。

### 説明：commonjs、amd、esモジュール、その他

最初に、その辺のモジュールシステムの(ひどい)矛盾を明確にする必要があります。私は私のオススメをあなたに伝え、ノイズを取り除くだけです。その他の動くかもしれない方法すべてを見せることはしません。

同じTypeScriptから`module`オプションに応じて異なるJavaScriptを生成することができます。無視できるものは次のとおりです(死んだ技術を説明することに興味はありません)：

* AMD：使用しないでください。ブラウザだけのものです
* SystemJS：良い実験でした。ESモジュールによって置き換えられました
* ESモジュール：まだ使えません

これはJavaScriptを生成するためのオプションです。これらのオプションの代わりに、`module：commonjs`を使ってください。

どのようにTypeScriptモジュールを書くかについても、ちょっと混乱があります。今日それを避けるには:

* `import foo = require( 'foo')`、つまり、`import/require`を避けて、代わりにESモジュールの構文を使用してください。

クール!ではESモジュールの構文を見てみましょう。

> 概要： `module：commonjs`を使い、ESモジュール構文を使ってモジュールをimport/export/作成します。

### ESモジュールの構文

* 変数(または型)のエクスポートは、キーワード`export`を前に置くだけなので簡単です。

```js
// file `foo.ts`
export let someVar = 123;
export type SomeType = {
  foo: string;
};
```

* 変数または型を専用の`export`文でエクスポートする

```js
// file `foo.ts`
let someVar = 123;
type SomeType = {
  foo: string;
};
export {
  someVar,
  SomeType
};
```
* 名前を変更して専用の`export`文で変数や型をエクスポートする

```js
// file `foo.ts`
let someVar = 123;
export { someVar as aDifferentName };
```

* `import`を使用して変数または型をインポートする

```js
// file `bar.ts`
import { someVar, SomeType } from './foo';
```

* 名前を変更して*import*を使って変数や型をインポートする

```js
// file `bar.ts`
import { someVar as aDifferentName } from './foo';
```

* `import * as`を使って1つの名前にモジュールすべてをインポートする
```js
// file `bar.ts`
import * as foo from './foo';
// you can use `foo.someVar` and `foo.SomeType` and anything else that foo might export.
```

* 副作用のためだけに一つのファイルをインポートする:

```js
import 'core-js'; // a common polyfill library
```

* 別のモジュールから全てのものを再エクスポートする

```js
export * from './foo';
```

* 別のモジュールから一部のものを再エクスポートする

```js
export { someVar } from './foo';
```

* 名前を変更して別のモジュールから一部のものだけを再エクスポートする

```js
export { someVar as aDifferentName } from './foo';
```

### デフォルトのexports/imports
あなたが後で知るように、私はデフォルトのexportが好きではありません。しかし、ここではexportの構文とデフォルトのexportの使い方を説明します。

* `export default`を使ってエクスポートする
  * 変数の前に(`let / const / var`は必要ありません)
  * 関数の前
  * クラスの前

```js
// some var
export default someVar = 123;
// OR Some function
export default function someFunction() { }
// OR Some class
export default class SomeClass { }
```

* `import someName using someModule`構文を使用してインポートする(インポートには任意の名前を付けることができます):

```js
import someLocalNameForThisFile from "../foo";
```

### モジュールのパス

> 私は `moduleResolution：commonjs`と仮定しようとしています。これはあなたのTypeScript設定に含めるべきオプションです。この設定は `module：commonjs`によって自動的に暗示されます。

2つの異なる種類のモジュールがあります。この区別は、インポート・ステートメントのパス・セクションによって行われます(たとえば、「これはパス・セクションです」からのインポートfoo)。

* 相対パスモジュール(パスは `.`で始まる`。/ someFile`や `../../ someFolder / someFile`など)
* その他の動的参照モジュール( ``core-js '`や` `typestyle``や` `react``や` `react / core``など)

主な違いは、モジュールがファイルシステム上でどのように解決されるかです。

> 私は、ルックアップパターンについて言及した後に説明する概念的な用語* place *を使用します。

#### 相対パスモジュール
簡単、ちょうど相対的なパスに従ってください:)

* `bar.ts`ファイルが`。* foo 'から `import * as foo'を実行した場合、`foo`を同じフォルダに置く必要があります。
* ファイル `bar.ts`が '../foo'から`import * as foo 'を実行する場合、 `foo`はフォルダ内に存在する必要があります。
* ファイル `bar.ts`が '../foo'から`foo 'としてインポートするのであれば、 `foo`の場所に`someFolder`というフォルダがなければなりません。

またはあなたが考えることができる他の相対的なパス:)

#### 動的ルックアップ

インポートパスが*相対でない場合、ルックアップは[*ノードスタイル解決*](https://nodejs.org/api/modules.html#modules_all_together)によって駆動されます。ここでは簡単な例を示します。

* あなたは `foo 'からfooとして` import *を持っています、以下はチェックされた場所です*順番に*
  * `。/ node_modules / foo`
  * `../ node_modules / foo`
  * `../../ node_modules / foo`
  *ファイルシステムのルートまで

* あなたは `something * / foo'`からfooとして` import *を持っています、以下はチェックされた場所です*順番に*
  * `。/ node_modules / something / foo`
  * `../ node_modules / something / foo`
  * `../../ node_modules / something / foo`
  *ファイルシステムのルートまで


### *とは何ですか？
私がチェックしている場所*を言うとき、私はその場所で次のことがチェックされていることを意味します。例えば`foo`の場所に対して：

* 場所がファイルの場合、たとえば`foo.ts`、hurray!
* 場所がフォルダで、 `foo / index.ts`ファイルがある場合は、hurray!
* 場所がフォルダで、 `foo / package.json`と存在するpackage.json内の`types`キーで指定されたファイルがある場合は、hurray!
* 他に場所がフォルダであり、存在するpackage.jsonに `main`キーで指定された`package.json`とファイルが存在する場合、その時ハレー!

ファイルでは、実際には `.ts`/` .d.ts`と `.js`を意味します。

以上です。あなたは今モジュールルックアップのエキスパートです(小さな偉業ではありません!)。

### 型のためだけにダイナミックルックアップを転覆する*
`declare module 'somePath'`を使ってあなたのプロジェクトのモジュール*をグローバルに宣言することができます。そして、importはそのパスに魔法のように*解決します

例えば
```ts
// globals.d.ts
declare module 'foo' {
  // Some variable declarations
  export var bar: number; /*sample*/
}
```

その後：
```ts
// anyOtherTsFileInYourProject.ts
import * as foo from 'foo';
// TypeScript assumes (without doing any lookup) that
// foo is {bar:number}

```

### `import / require`はタイプをインポートするだけです
次の文：

```ts
import foo = require('foo');
```

実際には* 2つのもの：

* fooモジュールのタイプ情報をインポートします。
* fooモジュールのランタイム依存性を指定します。

* タイプ情報*のみがロードされ、ランタイム依存性が発生しないように選択して選択することができます。続行する前に、本の[* declaration spaces *](../ project / declarationspaces.md)セクションを要約するとよいでしょう。

変数宣言空間でインポートされた名前を使用しないと、インポートは生成されたJavaScriptから完全に削除されます。これは例を用いて最もよく説明されています。これを理解すると、ユースケースを紹介します。

#### 例1
```ts
import foo = require('foo');
```
JavaScriptを生成します：

```js

```
そのとおり。 fooとしての* empty *ファイルは使用されません。

#### 例2
```ts
import foo = require('foo');
var bar: foo;
```
JavaScriptを生成します：
```js
var bar;
```
これは、 `foo`(または`foo.bas`などのプロパティ)が決して変数として使用されないためです。

#### 例3
```ts
import foo = require('foo');
var bar = foo;
```
JavaScriptを生成します(commonjsと仮定します)。
```js
var foo = require('foo');
var bar = foo;
```
これは `foo`が変数として使われているからです。


### 使用例：遅延読み込み
型推論は* upfront *する必要があります。これは、ファイル `bar`でファイル`foo`のある型を使用したい場合、次のようにしなければなりません：

```ts
import foo = require('foo');
var bar: foo.SomeType;
```
しかし、特定の条件下では、実行時に `foo`ファイルだけをロードしたいかもしれません。そのような場合には、 `import`という名前を*型注釈*と**変数*として**使用しないでください。これは、TypeScriptによって注入された* upfront *ランタイム依存性コードをすべて削除します。 *あなたのモジュールローダーに固有のコードを使って実際のモジュールを手動でインポートする*。

例として、次の `commonjs`ベースのコードを考えてみましょう。このコードでは、特定の関数呼び出しで` `foo``モジュールだけを読み込みます：

```ts
import foo = require('foo');

export function loadFoo() {
    // This is lazy loading `foo` and using the original module *only* as a type annotation
    var _foo: typeof foo = require('foo');
    // Now use `_foo` as a variable instead of `foo`.
}
```

amd(requirejsを使用)の同様のサンプルは次のようになります：
```ts
import foo = require('foo');

export function loadFoo() {
    // This is lazy loading `foo` and using the original module *only* as a type annotation
    require(['foo'], (_foo: typeof foo) => {
        // Now use `_foo` as a variable instead of `foo`.
    });
}
```

このパターンは一般的に使用されます。
* あなたが特定のルート上の特定のJavaScriptを読み込むWebアプリケーションでは、
* アプリケーションの起動を高速化するために、必要に応じて特定のモジュールのみをロードするノードアプリケーションでは*。

### ユースケース：円周の依存関係を壊す

レイジーロードの使用例と同様に、特定のモジュールローダ(commonjs / nodeとamd / requirejs)は循環依存性でうまく動作しません。そのような場合には、ある方向に* lazy loading *コードを持ち、他の方向にモジュールを先にロードすると便利です。

### ユースケース：インポートを確実にする

場合によっては、副作用のためだけにファイルをロードすることもできます(モジュールが[CodeMirror addons](https://codemirror.net/doc/manual.html#addons)などのライブラリに登録されるなど)。しかし、単に `import / require`を行うと、翻訳されたJavaScriptはモジュールへの依存関係を持たず、モジュールローダー(例えばwebpack)はインポートを完全に無視するかもしれません。このような場合、 `ensureImport`変数を使用して、コンパイルされたJavaScriptがモジュールに依存するようにすることができます。

```ts
import foo = require('./foo');
import bar = require('./bar');
import bas = require('./bas');
const ensureImport: any =
    foo
    || bar
    || bas;
```
