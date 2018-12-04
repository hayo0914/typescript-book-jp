* [lib.d.ts]（#libdts）
* [使用例]（#example-usage）
* [内部外観]（#libdts-inside-look）
* [Modifying Native types]（#modification-native-types）
* [カスタムlib.d.tsの使用]（#独自のカスタムlibdtsを使用）
* [lib.d.tsに対するコンパイラ `target`の影響]（#compiler-target-effect-on-libdts）
* [`lib`オプション]（#lib-option）
* [古いJavaScriptエンジンのためのPolyfill]（古いpolyfill-for-javascript-engines）

## `lib.d.ts`

特別な宣言ファイル `lib.d.ts`はTypeScriptのすべてのインストールに付属しています。このファイルには、JavaScriptのランタイムとDOMに存在するさまざまな一般的なJavaScript構文のアンビエント宣言が含まれています。

* このファイルは、TypeScriptプロジェクトのコンパイルコンテキストに自動的に含まれます。
* このファイルの目的は*チェックされた* JavaScriptコードの書き方を簡単に始めることです。

コンパイルコンテキストから `--noLib`コンパイラコマンドラインフラグ（` `tsconfig.json`に` `noLib：true``）を指定することで、このファイルをコンパイルコンテキストから除外することができます。

### 使用例

いつものように、実際に使用されているこのファイルの例を見てみましょう：

```ts
var foo = 123;
var bar = foo.toString();
```
このコードタイプは、すべてのJavaScriptオブジェクトに対して `toString`関数が`lib.d.ts`で定義されているため、上質であるかチェックします。

`noLib`オプションで同じサンプルコードを使用すると、型チェックエラーが発生します：

```ts
var foo = 123;
var bar = foo.toString(); // ERROR: Property 'toString' does not exist on type 'number'.
```
だからあなたは `lib.d.ts`の重要性を理解したので、その内容はどうなっていますか？そのことを次に検討する。

### `lib.d.ts`内部の見た目

`lib.d.ts`の内容は、主に変数*宣言の束です。 `window`、`document`、 `math`と同様の* interface *宣言の束です。 `Window`、`Document`、 `Math`です。

コード*の中に何が入力されているかを発見する最も簡単な方法は、あなたが知っていることです*。 `Math.floor`を実行した後、IDEを使ってF12（定義に移動）します（atom-typescriptはこれを大きくサポートしています）。

サンプル*変数*宣言を見てみましょう。 `window`は次のように定義されます：
```ts
declare var window: Window;
```
これは単純な `declare var`の後に変数名（ここでは`window`）とタイプアノテーションのインターフェース（ここで `Window`インターフェース）が続きます。これらの変数は、一般的にいくつかのグローバル*インターフェース*を指し示します。ここには（実際には非常に大規模な） `Window`インタフェースの小さなサンプルがあります：

```ts
interface Window extends EventTarget, WindowTimers, WindowSessionStorage, WindowLocalStorage, WindowConsole, GlobalEventHandlers, IDBEnvironment, WindowBase64 {
    animationStartTime: number;
    applicationCache: ApplicationCache;
    clientInformation: Navigator;
    closed: boolean;
    crypto: Crypto;
    // so on and so forth...
}
```
これらのインターフェースには、タイプ情報の*ロット*があることがわかります。 TypeScriptが存在しない場合、*あなたの頭に*これを保持する必要があります。コンパイルの知識を、Intellisenseのようなものを使って容易にアクセスできるようにすることができます。

これらのグローバルに* interfaces *を使用するのは正当な理由があります。 `lib.d.ts`を変更することなく*これらのグローバルに*プロパティを追加することができます。次に、このコンセプトについて説明します。

### ネイティブタイプを変更する

TypeScriptの `interface`はオープンされているので、これは`lib.d.ts`で宣言されたインターフェースにメンバーを追加するだけで、TypeScriptはその追加を受け取ります。これらのインタフェースを `lib.d.ts`に関連付けるには、これらの変更を[* global module *]（../ project / modules.md）で行う必要があることに注意してください。このために、[`globals.d.ts`]（../ project / globals.md）という特別なファイルを作成することをお勧めします。

ここでは、 `window`、`Math`、 `Date`に要素を追加する例をいくつか示します：

#### 例 `window`

`Window`インターフェースに物を追加するだけです：

```ts
interface Window {
    helloWorld(): void;
}
```

これにより、あなたはそれを*安全な方法で使うことができます：

```ts
// Add it at runtime
window.helloWorld = () => console.log('hello world');
// Call it
window.helloWorld();
// Misuse it and you get an error:
window.helloWorld('gracius'); // Error: Supplied parameters do not match the signature of the call target
```

#### 例題 `数学
グローバル変数 `Math`は`lib.d.ts`で定義されています（あなたの開発ツールを使って定義に移動します）：

```ts
/** An intrinsic object that provides basic mathematics functionality and constants. */
declare var Math: Math;
```

すなわち、変数「数学」は「数学」インターフェースのインスタンスである。 `Math`インターフェースは次のように定義されています：

```ts
interface Math {
    E: number;
    LN10: number;
    // others ...
}
```

つまり、 `Math`グローバル変数に物を追加したいのであれば、それを`Math`グローバルインターフェースに追加するだけです。 [`seedrandom`プロジェクト]（https://www.npmjs.com/package/seedrandom）を参考にして、グローバル`Math`オブジェクトに `seedrandom`関数を追加してください。これは非常に簡単に宣言できます：

```ts
interface Math {
    seedrandom(seed?: string);
}
```

そして、あなたはそれを使うことができます：

```ts
Math.seedrandom();
// or
Math.seedrandom("Any string you want!");
```

#### 例題 `Date`

`lib.d.ts`の`Date` *変数*の定義を見ると、次のようになります：

```ts
declare var Date: DateConstructor;
```
`DateConstructor`というインターフェースは、`Date`グローバル変数を使って使うことができるメンバーが含まれている点で、 `Math`と`Window`で以前見たものに似ています。 `Date.now（）`。これらのメンバーに加えて、 `Date`インスタンス（例えば`new Date（） `）を作成するための*構造*シグネチャが含まれています。 `DateConstructor`インターフェースのスニペットを以下に示します：

```ts
interface DateConstructor {
    new (): Date;
    // ... other construct signatures

    now(): number;
    // ... other member functions
}
```

プロジェクト[`datejs`]（https://github.com/abritinthebay/datejs）を考えてみましょう。 DateJSは、メンバを `Date`グローバル変数と`Date`インスタンスの両方に追加します。したがって、このライブラリのTypeScriptの定義は、（この場合、コミュニティはすでにあなたのためにこれを書いています）（https://github.com/DefinitelyTyped/DefinitelyTyped/blob/master/types/datejs/index.d）のようになります。 ts））：

```ts
/** DateJS Public Static Methods */
interface DateConstructor {
    /** Gets a date that is set to the current date. The time is set to the start of the day (00:00 or 12:00 AM) */
    today(): Date;
    // ... so on and so forth
}

/** DateJS Public Instance Methods */
interface Date {
    /** Adds the specified number of milliseconds to this instance. */
    addMilliseconds(milliseconds: number): Date;
    // ... so on and so forth
}
```
これにより、TypeSafeの方法で次のようなことができます：

```ts
var today = Date.today();
var todayAfter1second = today.addMilliseconds(1000);
```

#### 例 `string`

文字列の `lib.d.ts`を調べると、`Date`（ `String`グローバル変数、`StringConstructor`インターフェース、 `String`インターフェース）のようなものが見つかるでしょう。しかし、注意すべき点の1つは、以下のコードサンプルで示すように、 `String`インターフェースも文字列*リテラル*に影響を与えます。

```ts

interface String {
    endsWith(suffix: string): boolean;
}

String.prototype.endsWith = function(suffix: string): boolean {
    var str: string = this;
    return str && str.indexOf(suffix, str.length - suffix.length) !== -1;
}

console.log('foo bar'.endsWith('bas')); // false
console.log('foo bas'.endsWith('bas')); // true
```

同様の変数とインタフェースは、 `Number`、`Boolean`、 `RegExp`などの静的メンバーとインスタンスメンバーの両方を持つ他のものにも存在し、これらのインターフェースはこれらの型のリテラルインスタンスにも影響します。

### 例 `string` redux

メンテナンス上の理由から、 `global.d.ts`を作成することを推奨しました。しかし、あなたが望むのであれば*ファイルモジュール*の中からグローバルな名前空間*に侵入することができます。これは `declare global {/ * global namespace here * /}`を使って行います。例えば。前の例は次のようにすることもできます：

```ts
// Ensure this is treated as a module.
export {};

declare global {
    interface String {
        endsWith(suffix: string): boolean;
    }
}

String.prototype.endsWith = function(suffix: string): boolean {
    var str: string = this;
    return str && str.indexOf(suffix, str.length - suffix.length) !== -1;
}

console.log('foo bar'.endsWith('bas')); // false
console.log('foo bas'.endsWith('bas')); // true
```

### 独自のカスタムlib.d.tsを使用する
前に述べたように、 `--noLib`ブールコンパイラフラグを使用すると、TypeScriptは自動的に`lib.d.ts`の包含を除外します。これが有用な機能である理由はさまざまです。一般的なもののいくつかを以下に示します。

* 標準ブラウザベースのランタイム環境とは大きく異なる*カスタムJavaScript環境で実行しています。
* コード内で使用可能な*グローバル*を厳密に制御することができます。例えば。 lib.d.tsは `item`を大域変数として定義しており、これをあなたのコードに漏らさないようにします。

デフォルトの `lib.d.ts`を除外すると、コンパイルコンテキストに同様の名前のファイルを含めることができ、TypeScriptはタイプチェックのためにそれを取り込みます。

> 注意： `--noLib`には注意してください。あなたがnoLibの土地にいると、あなたのプロジェクトを他の人と共有することを選択すると、noLib土地に（またはあなたの土地に）強制されます。さらに悪いことに、*自分の*コードをプロジェクトに持っていくと、lib *ベースのコードに移植する必要があるかもしれません。

### コンパイラの `lib.d.ts`に対する効果

コンパイラのターゲットを `es6`に設定すると`lib.d.ts`は `Promise`のようなより現代的なもの（es6）のための* ambient宣言を追加します。コンパイラターゲットがコードの*雰囲気*を変えるという魔法の効果は、一部の人にとっては望ましいことです。他の人にとっては、*コード生成*と*コードの雰囲気*を融合させるために問題があります。

しかし、あなたの環境をきめ細かく制御したいなら、次に述べる `--lib`オプションを使うべきです。

### libオプション

場合によっては、コンパイル対象（生成されたJavaScriptバージョン）とアンビエントライブラリサポートの関係を切り離したい場合があります。一般的な例は、「約束」である。今日（2016年6月）、 `--target es5`をしたいと思うかもしれませんが、`Promise`のような最新の機能を使います。これをサポートするために、 `lib`コンパイラオプションを使って`lib`を明示的に制御することができます。

> 注意： `--lib`を使うと、`--target`のlibの魔法を切り離して、より良い制御ができます。

このオプションをコマンドラインまたは `tsconfig.json`に指定することができます（推奨）。

** コマンドライン**：
```
tsc --target es5 --lib dom,es6
```
** tsconfig.json **：
```json
"compilerOptions": {
    "lib": ["dom", "es6"]
}
```

libsは次のように分類できます。

* JavaScriptのバルク機能：
    * es5
    * es6
    * es2015
    * es7
    * es2016
    * es2017
    * esnext
* 実行時環境
    * dom
    * dom.iterable
    * webworker
    *スクリプトホスト
* ESNext By Featureオプション（バルク機能よりも小さい）
    * es2015.core
    * es2015.collection
    * es2015.generator
    * es2015.iterable
    * es2015.promise
    * es2015.proxy
    * es2015.reflect
    * es2015.symbol
    * es2015.symbol.wellknown
    * es2016.array.include
    * es2017.object
    * es2017.sharedmemory
    * esnext.asynciterable

> 注意： `--lib`オプションは非常に細かいチューニングされたコントロールを提供します。したがって、バルク+環境カテゴリから項目を選択する可能性が最も高いです。
> --libが指定されていない場合、デフォルトのライブラリが注入されます：
   -   - ターゲットの場合es5 => es5、dom、scripthost
   - の場合--target es6 => es6、dom、dom.iterable、scripthost

私の個人的な勧告：

```json
"compilerOptions": {
    "target": "es5",
    "lib": ["es6", "dom"]
}
```

ES5にシンボルを含む例：

ターゲットがes5の場合、Symbol APIは含まれません。実際、次のようなエラーが表示されます。[ts]名前 'シンボル'が見つかりません。
"target"： "es5"と "lib"を組み合わせて、TypeScriptにSymbol APIを提供することができます：

```json
"compilerOptions": {
    "target": "es5",
    "lib": ["es5", "dom", "scripthost", "es2015.symbol"]
}
```

## 古いJavaScriptエンジン用のPolyfill

> [この件に関するEgghead PRO Video]（https://egghead.io/lessons/typescript-using-es6-and-esnext-with-typescript）

`Map`/` Set`や、 `Promise`（このリストはもちろん変更されるでしょう）のようなランタイム機能は、現代の`lib`オプションで使用できるものがかなりあります。これらを使うには `core-js 'を使うだけです。単にインストールしてください：

```
npm install core-js --save-dev
```
また、アプリケーションのエントリポイントにインポートを追加します。

```js
import "core-js";
```

そして、あなたのためにこれらのランタイム機能をポリファイリングする必要があります。
