## 外部モジュール(External modules)
TypeScriptの外部モジュールパターンには大きなパワーと利便性があります。ここでは、そのパワーと実際の用途を知るためのパターンについて説明します。

### 説明：commonjs、amd、esモジュール、その他

最初に、その辺のモジュールシステムの(ひどい)矛盾を明確にする必要があります。私は私のオススメをあなたに伝え、ノイズを取り除くだけです。その他の動くかもしれない方法すべてを見せることはしません。

同じTypeScriptから`module`オプションに応じて異なるJavaScriptを生成することができます。無視できるものは次のとおりです(死んだ技術を説明することに興味はありません)：

* AMD：使用しないでください。ブラウザだけのものでした。
* SystemJS：良い実験でした。ESモジュールによって置き換えられました。
* ESモジュール：まだ使えません。

これはJavaScriptを生成するためのオプションです。これらのオプションの代わりに、`module:commonjs`を使ってください。

どのようにTypeScriptモジュールを書くかについても、少し混乱があります。今日それを避けるには:

* `import foo = require('foo')`、つまり、`import/require`を避けて、代わりにESモジュールの構文を使用してください。

それではESモジュールの構文を見てみましょう。

> 概要： `module:commonjs`を使い、ESモジュールの構文を使ってモジュールをimport/export/作成します。

### ESモジュールの構文

* 変数(または型)のエクスポートは、キーワード`export`を前に置くだけです。簡単です。

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

* 副作用のためだけに1つのファイルをインポートする:

```js
import 'core-js'; // a common polyfill library
```

* 別のモジュールからすべてのものを再エクスポートする

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

* `import someName from "someModule"`構文を使用してインポートする(インポートには任意の名前を付けることができます):

```js
import someLocalNameForThisFile from "../foo";
```

### モジュールのパス

> 私は`moduleResolution: commonjs`を仮定しています。これはあなたのTypeScript設定に含めるべきオプションです。この設定は`module:commonjs`によって暗黙的に設定されます。

2つの異なる種類のモジュールがあります。この区別は、import文のパスセクション(path section)によって行われます(たとえば、`import foo from 'これがパスセクションです'`)。

* 相対パスモジュール(`.`で始まるパス:`./someFile`、`../../someFolder/someFile`など)
* その他の動的参照モジュール(`'core-js'`、`'typestyle'`、`'react'`、`'react / core'`など)

主な違いは、モジュールがファイルシステム上でどのように解決されるかです。

#### 相対パスモジュール(Relative path modules)
簡単です。単に相対的なパスに従います :)

* ファイル`bar.ts`が`import * as foo from './foo';`を実行した場合、`foo`を同じフォルダに置く必要がある
* ファイル`bar.ts`が`import * as foo from '../foo';`を実行する場合、`foo`は1つ上のフォルダ内に存在する必要がある
* ファイル`bar.ts`が`import * as foo from '../someFolder/foo';`を実行する場合、1つ上のフォルダにfooが存在する`someFolder`というフォルダが存在する必要がある

もしくは他に思いついた相対パスが使えます :)

#### 動的ルックアップ(Dynamic lookup)

インポートパスが相対でない場合、検索は [Node.jsスタイルのモジュール解決](https://nodejs.org/api/modules.html#modules_all_together) によって行われます。ここでは簡単な例を示します。

* あなたが`import * as foo from 'foo'`を書いた場合、以下の場所が順番にチェックされます
  * `./node_modules/foo`
  * `../node_modules/foo`
  * `../../node_modules/foo`
  * ファイルシステムのルートに到達するまで続く

* あなたが`import * as foo from 'something/foo'`を書いた場合、以下の場所が順番にチェックされます
  * `./node_modules/something/foo`
  * `../node_modules/something/foo`
  * `../../node_modules/something/foo`
  * ファイルシステムのルートに到達するまで続く

### 場所(place)とは何か
私が「チェックされる場所」について言及する時、私は、次のことが、その場所でチェックされていることを意味しています。例えば`foo`の場所に対して：

* 場所がファイルを指している場合、たとえば`foo.ts`があれば、解決されます。
* 場所がフォルダで、`foo/index.ts`ファイルがある場合、解決されます。
* 場所がフォルダで、`foo/package.json`が存在し、package.jsonの`types`キーで指定されたファイルがある場合は、解決されます。
* 場所がフォルダで、`package.json`が存在し、package.jsonの`main`キーで指定されたファイル存在する場合、解決されます。

私が言うファイルは、実際には`.ts`/`.d.ts`と`.js`を意味しています。

以上です。あなたは今モジュール解決のエキスパートです(なかなかの成果です!)。

### 型について動的検索を上書きする
あなたは、`declare module 'somePath'`を使ってプロジェクトのモジュールをグローバルに宣言することができます。そして、importはそのパスに魔法のように解決します。

例
```ts
// global.d.ts
declare module 'foo' {
  // Some variable declarations
  export var bar: number; /*sample*/
}
```

そして：
```ts
// anyOtherTsFileInYourProject.ts
import * as foo from 'foo';
// TypeScript assumes (without doing any lookup) that
// foo is {bar:number}

```

### 型だけを`import/require`する

次の文は:
```ts
import foo = require('foo');
```

実際には2つのことをします:
* fooモジュールの型情報をインポートする
* fooモジュールの実行時の依存関係を指定する

開発者は、型情報のみをロードし、実行時の依存関係が発生しないようにすることも可能です。続ける前に、[宣言空間](../project/declarationspaces.md)を読んでおくとよいでしょう。


変数宣言空間にインポートされた名前を使用しない場合、そのインポートは、生成されたJavaScriptから完全に削除されます。例を見るのが最も簡単です。これが理解できたら、ユースケースを紹介します。

#### 例1
```ts
import foo = require('foo');
```
生成されるJavaScript：

```js

```
そのとおり。fooが使われないため、空ファイルです。

#### 例2
```ts
import foo = require('foo');
var bar: foo;
```
生成されるJavaScript：
```js
var bar;
```
これは、`foo`(または`foo.bas`などのプロパティ)が変数として一度も使用されないためです。

#### 例3
```ts
import foo = require('foo');
var bar = foo;
```
生成されるJavaScript(commonjsと仮定します):
```js
var foo = require('foo');
var bar = foo;
```
これは`foo`が変数として使われているためです。


### ユースケース： 遅延ロード(Lazy loading)
型推論は事前に行う必要があります。これは、ファイル`bar`でファイル`foo`のある型を使用したい場合、次のようにしなければならないことを意味します：

```ts
import foo = require('foo');
var bar: foo.SomeType;
```
しかし、あるいは実行時に特定条件下の場合だけ`foo`をロードしたいかもしれません。そのような場合には、`import`した名前を型アノテーションとしてのみ使用し、変数として使用しないでください。これにより、TypeScriptにより挿入される実行時依存関係をすべて削除します。そして、あなたは独自のモジュールローダーに固有のコードを書いて実際のモジュールを手動でインポートします。

例として、次の`commonjs`ベースのコードを考えてみましょう。このコードでは、特定の関数が呼び出された時だけ`'foo'`モジュールをロードします：

```ts
import foo = require('foo');

export function loadFoo() {
    // This is lazy loading `foo` and using the original module *only* as a type annotation
    var _foo: typeof foo = require('foo');
    // Now use `_foo` as a variable instead of `foo`.
}
```

同様の`amd`(requirejsを使用)のサンプルは次のようになります：
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
* Webアプリケーションにおいて、特定のルートの場合のみ特定のJavaScriptをロードする
* nodeアプリケーションにおいて、アプリケーションの起動を高速化したい場合に、特定のモジュールだけをロードする

### ユースケース：循環依存を避ける

遅延ロードの使用例と同様に、特定のモジュールローダ(commonjs/nodeと、amd/requirejs)は循環依存のため、うまく動作しません。そのような場合には、1つの方向に遅延ロードを行うようにし、反対方向のロードの前にロードしておくと便利です。

### ユースケース：確実にインポートする

場合によっては、副作用(side effect)のためだけにファイルをロードすることもできます(例えば[CodeMirror addons](https://codemirror.net/doc/manual.html#addons)のように、モジュールを他のライブラリに登録させる場合など)。しかし、単に`import/require`を行うと、トランスパイルされたJavaScriptはモジュールへの依存関係を持たず、モジュールローダー(例えばwebpack)はインポートを完全に無視するかもしれません。このような場合、 `ensureImport`変数を使用して、コンパイルされたJavaScriptがモジュールに依存するようにすることができます。

```ts
import foo = require('./foo');
import bar = require('./bar');
import bas = require('./bas');
const ensureImport: any =
    foo
    || bar
    || bas;
```
