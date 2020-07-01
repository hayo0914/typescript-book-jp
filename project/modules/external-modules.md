# ファイルモジュールの詳細

TypeScriptのモジュール機能は非常に強力であり、便利な機能です。ここでは、その強力さと実際のユースケースを説明します。

## 説明：commonjs、amd、esモジュール、その他

最初に、このあたりのモジュールシステムの分かりづらい矛盾を明確にする必要があります。私は単に推奨を伝え、このノイズを取り除きたいと思います。その他の動くかもしれない方法をすべて説明することはしません。

同じTypeScriptのコードから`module`オプションに応じて異なるJavaScriptを生成されます。無視できるものは次のとおりです\(既に過去のものとなった技術については詳しく説明しません\)：

* AMD：使用しないでください。ブラウザでしか使えませんでした。
* SystemJS：良い実験でしたが、ESモジュールによって置き換えられました。
* ESモジュール：モダンなブラウザでのみ利用できます。

これはJavaScriptを生成するためのオプションです。これらのオプションの代わりに、`module:commonjs`を使うことをおすすめします。

どのようにTypeScriptモジュールを書くかについては、まだ意見が完全には、まとまっていません。将来問題が起きることを避けるには下記のようにしてください:

* `import foo = require('foo')`、つまり、`import/require`を避けて、ESモジュールの構文を使用してください。

それではESモジュールの構文を見てみましょう。

> 概要： `module:commonjs`を使い、ESモジュールの構文を使ってモジュールをimport/export/作成します。

## ESモジュールの構文

* 変数\(または型\)のエクスポートは、キーワード`export`を前に置くだけです。簡単です。

```javascript
// `foo.ts`ファイル
export let someVar = 123;
export type SomeType = {
  foo: string;
};
```

* 変数または型を専用の`export`文でエクスポートする

```javascript
// `foo.ts`ファイル
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

```javascript
// `foo.ts`ファイル
let someVar = 123;
export { someVar as aDifferentName };
```

* `import`を使用して変数または型をインポートする

```javascript
// `foo.ts`ファイル
import { someVar, SomeType } from './foo';
```

* 名前を変更して_import_を使って変数や型をインポートする

```javascript
// `bar.ts`ファイル
import { someVar as aDifferentName } from './foo';
```

* `import * as`を使って1つの名前にモジュールすべてをインポートする

  ```javascript
  // `bar.ts`ファイル
  import * as foo from './foo';
  // `foo.someVar`や`foo.SomeType`など`foo.ts`がエクスポートしているものを何でも利用できます
  ```

* 副作用のためだけに1つのファイルをインポートする:

```javascript
import 'core-js'; // 共通のpolyfillライブラリ
```

* 別のモジュールからすべてのものを再エクスポートする

```javascript
export * from './foo';
```

* 別のモジュールから一部のものを再エクスポートする

```javascript
export { someVar } from './foo';
```

* 名前を変更して別のモジュールから一部のものだけを再エクスポートする

```javascript
export { someVar as aDifferentName } from './foo';
```

## デフォルトエクスポート/インポート

あなたが後で知るように、私はデフォルトエクスポートが好きではありません。しかし、知っておく必要があります。そのため、ここで、デフォルトエクスポートの使い方を説明します。

* `export default`を使ってエクスポートする
  * 変数の前に\(`let / const / var`は必要ありません\)
  * 関数の前
  * クラスの前

```javascript
// 何らかの変数
export default someVar = 123;
// または関数
export default function someFunction() { }
// またはクラス
export default class SomeClass { }
```

* `import someName from "someModule"`という構文を使用してインポートする\(インポートしたものには任意の名前を付けることができます\):

```javascript
import someLocalNameForThisFile from "../foo";
```

## モジュールのパス解決

> 私は`moduleResolution: commonjs`を指定することを前提にしています。これはあなたのTypeScript設定にも追加しておくべきオプションです。この設定は`module:commonjs`を設定していれば、暗黙的に設定されます。

2つの異なる種類のモジュールがあります。それらは、import文のパス部分によって区別されます\(たとえば、`import foo from 'パス'`\)。

* 相対パスのモジュール\(`.`で始まるパス:`./someFile`、`../../someFolder/someFile`など\)
* 動的に参照されるモジュール\(`'core-js'`、`'typestyle'`、`'react'`、`'react / core'`など\)

主な違いは、モジュールがファイルシステム上でどのように解決されるかです。

### 相対パスの解決

簡単です。単に相対的なパスに従います :\)

* ファイル`bar.ts`が`import * as foo from './foo';`を実行した場合、`foo`を同じフォルダに置く必要がある
* ファイル`bar.ts`が`import * as foo from '../foo';`を実行する場合、`foo`は1つ上のフォルダ内に存在する必要がある
* ファイル`bar.ts`が`import * as foo from '../someFolder/foo';`を実行する場合、1つ上のフォルダにfooが存在する`someFolder`というフォルダが存在する必要がある

もしくは他に思いついた相対パスが使えます :\)

### 動的な解決

インポートパスが相対でない場合、検索は [Node.jsスタイルのモジュール解決](https://nodejs.org/api/modules.html#modules_all_together) によって行われます。ここでは簡単な例を示します。

* `import * as foo from 'foo'`と書いた場合、以下の場所が順番にチェックされます
  * `./node_modules/foo`
  * `../node_modules/foo`
  * `../../node_modules/foo`
  * ファイルシステムのルートに到達するまで続く
* `import * as foo from 'something/foo'`と書いた場合、以下の場所が順番にチェックされます
  * `./node_modules/something/foo`
  * `../node_modules/something/foo`
  * `../../node_modules/something/foo`
  * ファイルシステムのルートに到達するまで続く

## どのようにパスが解決されるか

上記で言及している場所が「チェックされる」とは、下記のように、その場所がチェックされることを意味しています。例えば`foo`というパスを指定しているとします:

* その場所に、`foo.ts`があれば、解決されます。
* その場所がフォルダで、`foo/index.ts`ファイルがある場合、解決されます。
* その場所がフォルダで、`foo/package.json`が存在し、package.jsonの`types`キーで指定されたファイルがある場合は、解決されます。
* その場所がフォルダで、`package.json`が存在し、package.jsonの`main`キーで指定されたファイルが存在する場合、解決されます。

私が言うファイルは、実際には`.ts`/`.d.ts`と`.js`を意味しています。

以上です。あなたは既にモジュール解決のエキスパートです。

## 型の動的検索を上書きする

あなたは、`declare module '何らかのパス'`を使ってプロジェクトのモジュールをグローバルに宣言することができます。そして、import文はそのパスを魔法のように解決します。

例：

```typescript
// globals.d.ts
declare module 'foo' {
  // 何らかの変数の宣言
  export var bar: number; /* 例 */
}
```

そして、このようにすることができます：

```typescript
// anyOtherTsFileInYourProject.ts
import * as foo from 'foo';
// 動的ルックアップを行わない場合、TypeScriptは、 foo を {bar:number} と推測します:
```

## 型だけを`import/require`する

次の文は:

```typescript
import foo = require('foo');
```

実際には2つのことをしています:

* fooモジュールの型情報をインポートする
* fooモジュールの実行時の依存関係を指定する

開発者は、型情報のみをロードし、実行時の依存関係が発生しないようにすることも可能です。この先を理解する前に、[宣言空間](../declarationspaces.md)を読んでおくとよいでしょう。

変数宣言空間にインポートされた名前を使用しない場合、そのインポートは、生成されたJavaScriptから完全に削除されます。例を見るのが最も簡単です。これが理解できたら、ユースケースを紹介します。

### 例1

```typescript
import foo = require('foo');
```

生成されるJavaScript：

```javascript

```

想像の通り、fooが使われないため、空ファイルが生成されます。

### 例2

```typescript
import foo = require('foo');
var bar: foo;
```

生成されるJavaScript：

```javascript
var bar;
```

これは、`foo`\(または`foo.bas`などのプロパティ\)が変数として一度も使用されないためです。

### 例3

```typescript
import foo = require('foo');
var bar = foo;
```

生成されるJavaScript\(commonjsと仮定します\):

```javascript
var foo = require('foo');
var bar = foo;
```

これは`foo`が変数として使われているためです。

## ユースケース： 遅延ロード\(Lazy loading\)

型推論は事前に行う必要があります。これは、ファイル`bar`でファイル`foo`のある型を使用したい場合、次のようにしなければならないことを意味します：

```typescript
import foo = require('foo');
var bar: foo.SomeType;
```

しかし、あるいは実行時に特定の場合だけ`foo`をロードしたいかもしれません。そのような場合には、`import`した名前を型アノテーションとしてのみ使用し、変数として使用しないでください。これにより、TypeScriptにより挿入される実行時依存関係をすべて削除します。そして、あなたは独自のモジュールローダーに固有のコードを書いて実際のモジュールを手動でインポートします。

例として、次の`commonjs`ベースのコードを考えてみましょう。このコードでは、特定の関数が呼び出された時だけ`'foo'`モジュールをロードします：

```typescript
import foo = require('foo');

export function loadFoo() {
    // `foo` を遅延ロードします。そして、オリジナルのモジュールは型アノテーションとして *だけ* 利用します。
    var _foo: typeof foo = require('foo');
    // これで、 `foo` の代わりに `_foo` を変数として扱うことができます。
}
```

`amd`\(requirejsを使用\)での同様のサンプルは次のようになります：

```typescript
import foo = require('foo');

export function loadFoo() {
    // `foo` を遅延ロードします。そして、オリジナルのモジュールは型アノテーションとして *だけ* 利用します。
    require(['foo'], (_foo: typeof foo) => {
        // これで、 `foo` の代わりに `_foo` を変数として扱うことができます。
    });
}
```

このパターンは一般的に使用されます。

* Webアプリケーションにおいて、特定のルートの場合のみ特定のJavaScriptをロードする
* Nodeアプリケーションにおいて、アプリケーションの起動を高速化したい場合に、特定のモジュールだけをロードする

## ユースケース：循環依存を避ける

遅延ロードの使用例と同様に、特定のモジュールローダ\(commonjs/nodeと、amd/requirejs\)は循環依存のため、うまく動作しません。そのような場合には、1つの方向に遅延ロードを行うようにし、反対方向のロードの前にロードしておくと便利です。

## ユースケース：確実にインポートする

場合によっては、副作用のためだけにファイルをロードすることもできます\(例えば[CodeMirror addons](https://codemirror.net/doc/manual.html#addons)のように、モジュールを他のライブラリに登録させる場合など\)。しかし、単に`import/require`を行うと、コンパイルされたJavaScriptがモジュールに依存しておらず、モジュールバンドラ\(例えばwebpack\)が、そのインポートを完全に無視してしまうかもしれません。このような場合、例えば下記のように `ensureImport`変数を使用して、コンパイルされたJavaScriptがモジュールに依存するようにすることができます。

```typescript
import foo = require('./foo');
import bar = require('./bar');
import bas = require('./bas');
const ensureImport: any =
    foo
    || bar
    || bas;
```

