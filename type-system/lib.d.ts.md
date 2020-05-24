# lib.d.ts

## `lib.d.ts`

特別な宣言ファイル`lib.d.ts`はTypeScriptをインストールしたときに付属しています。このファイルには、JavaScriptランタイムとDOMに存在するさまざまな一般的なJavaScriptの構成物の環境宣言が含まれています。

* このファイルは、TypeScriptプロジェクトのコンパイルコンテキストに自動的に含まれます
* このファイルの目的は型チェックのあるJavaScript開発を簡単に始めることです

コンパイルオプションに`--noLib`を指定してこのファイルをコンパイルコンテキストから除外することができます\(`tsconfig.json`に`noLib : true`を指定\)。

### 使用例

いつものように、実際に使用されている例を見てみましょう：

```typescript
var foo = 123;
var bar = foo.toString();
```

このコードは問題なく型チェックされます。なぜなら、すべてのJavaScriptオブジェクトに対して`toString`関数が`lib.d.ts`で定義されているからです。

`noLib`オプションで同じサンプルコードを使用すると、型チェックエラーが発生します：

```typescript
var foo = 123;
var bar = foo.toString(); // ERROR: Property 'toString' does not exist on type 'number'.
```

もうあなたは`lib.d.ts`の重要性を理解したので、次にその内容を見てみましょう。

### `lib.d.ts`の内容

`lib.d.ts`の内容は、主に変数宣言の集まりです。例えば`window`、`document`、`math`や、同様のインターフェース宣言`Window`、`Document`、`Math`です。

このドキュメントと型アノテーションを読む一番簡単な方法は、あなたが動くと知っているもののコードを打ち込むことです。例えばIDEで`Math.floor`と打ち込み、F12を押下すると、定義に移動します\(VSCodeはこれを良くサポートしています\)。

サンプルの変数宣言を見てみましょう。`window`は次のように定義されます：

```typescript
declare var window: Window;
```

これは単純な`declare var`の後に変数名\(ここでは`window`\)とタイプアノテーションのインターフェース\(`Window`インターフェース\)が続きます。これらの変数は、一般的にいくつかのグローバルインターフェースを指し示します。例として、ここに`Window`インターフェースの小さな\(実際には非常に大規模な\)サンプルを提示します：

```typescript
interface Window extends EventTarget, WindowTimers, WindowSessionStorage, WindowLocalStorage, WindowConsole, GlobalEventHandlers, IDBEnvironment, WindowBase64 {
    animationStartTime: number;
    applicationCache: ApplicationCache;
    clientInformation: Navigator;
    closed: boolean;
    crypto: Crypto;
    // so on and so forth...
}
```

これらのインターフェースには、たくさんの型情報があることがわかります。TypeScriptが存在しない場合、あなたの頭にこれを保持する必要があります。コンパイルの知識を、インテリセンス\(Intellisense\)のようなものを使って容易にアクセスできるようにすることができます。

これらのグローバルにインターフェースを使用するには良い理由があります。`lib.d.ts`を変更することなく、これらのグローバルのインターフェースにプロパティを追加することができます。次に、このコンセプトについて説明します。

### ネイティブ型\(Native Types\)を変更する

TypeScriptの`interface`はオープンエンドなので、`lib.d.ts`で宣言されたインターフェースにメンバを追加するだけで、TypeScriptはその追加を認識します。これらのインターフェースを`lib.d.ts`に関連付けるには、これらの変更を [グローバルモジュール](../project/modules/) で行う必要があることに注意してください。このために、 [`globals.d.ts`](../project/modules/globals.md) という特別なファイルを作成することをお勧めします。

ここでは、 `window`、`Math`、`Date`に要素を追加する例をいくつか示します：

#### `window`の例

単に`Window`インターフェースにものを追加します：

```typescript
interface Window {
    helloWorld(): void;
}
```

これにより、あなたはそれを安全な方法で使うことができます：

```typescript
// Add it at runtime
window.helloWorld = () => console.log('hello world');
// Call it
window.helloWorld();
// Misuse it and you get an error:
window.helloWorld('gracius'); // Error: Supplied parameters do not match the signature of the call target
```

#### `Math`の例

グローバル変数`Math`は`lib.d.ts`で定義されています\(再度、あなたの開発ツールを使って定義に移動してください\)：

```typescript
/** An intrinsic object that provides basic mathematics functionality and constants. */
declare var Math: Math;
```

すなわち、変数`Math`は`Math`インターフェースのインスタンスです。`Math`インターフェースは次のように定義されています：

```typescript
interface Math {
    E: number;
    LN10: number;
    // others ...
}
```

つまり、グローバル変数の`Math`に物を追加したいのであれば、それをグローバルインターフェースの`Math`に追加するだけです。[`seedrandom`プロジェクト](https://www.npmjs.com/package/seedrandom) を参考に、グローバル`Math`オブジェクトに`seedrandom`関数を追加してください。これは非常に簡単に宣言できます：

```typescript
interface Math {
    seedrandom(seed?: string);
}
```

そして、あなたはそれを使うことができます：

```typescript
Math.seedrandom();
// or
Math.seedrandom("Any string you want!");
```

#### `Date`の例

`lib.d.ts`の`Date`変数の定義を見ると、次のようになっています：

```typescript
declare var Date: DateConstructor;
```

`DateConstructor`というインターフェースは、`Date`グローバル変数を使って使うことができるメンバが含まれている点で、`Math`と`Window`で見たものに似ています。 例えば`Date.now()`です。これらのメンバに加えて、`Date`インスタンス\(例えば`new Date()`\)を作成するためのコンストラクタのシグネチャが含まれています。 `DateConstructor`インターフェースの断片を以下に示します：

```typescript
interface DateConstructor {
    new (): Date;
    // ... other construct signatures

    now(): number;
    // ... other member functions
}
```

プロジェクト [`datejs`](https://github.com/abritinthebay/datejs) を考えてみましょう。 DateJSは、メンバを`Date`グローバル変数と`Date`インスタンスの両方に追加します。したがって、このライブラリのTypeScriptの定義は、以下のようになります\(ところで、[コミュニティはすでにそれをあなたのために書いています](https://github.com/DefinitelyTyped/DefinitelyTyped/blob/master/types/datejs/index.d)\)：

```typescript
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

これにより、型安全な方法で次のようなことができます：

```typescript
var today = Date.today();
var todayAfter1second = today.addMilliseconds(1000);
```

#### `string`の例

文字列の `lib.d.ts`を調べると、`Date`\(`String`グローバル変数、`StringConstructor`インターフェース、`String`インターフェース\)のようなものが見つかるでしょう。しかし、注意すべき点の1つは、以下のコードサンプルで示すように、`String`インターフェースは、文字列リテラルに対しても影響を与えます:

```typescript
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

同様の変数とインターフェースは、`Number`、`Boolean`、`RegExp`などの静的メンバとインスタンスメンバの両方を持つ他のものにも存在し、これらのインターフェースはこれらの型のリテラルのインスタンスにも影響します。

### `string`後方一致の例

メンテナンス上の理由から、`global.d.ts`を作成することを推奨しました。しかし、あなたが望むのであればファイルモジュールの中からグローバルな名前空間に入れることができます。これは`declare global {/ * global namespace here * /}`を使って行います。例えば。前の例は次のようにすることもできます：

```typescript
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

前に述べたように、 `--noLib`のコンパイラフラグを使用すると、TypeScriptは自動的に`lib.d.ts`を除外します。これが有用である理由はさまざまです。一般的なもののいくつかを以下に示します。

* 標準ブラウザベースのランタイム環境とは大きく異なるカスタムJavaScript環境で実行する場合
* コード内で使用可能なグローバルを厳密に制御したい場合。例えばlib.d.tsは`item`を大域変数として定義していますが、あなたはそれをコードに混入させたくないでしょう

デフォルトの `lib.d.ts`を除外すると、コンパイルコンテキストに同様の名前のファイルを含めることができ、TypeScriptは型チェックのためにそれを取り込みます。

> 注意： `--noLib`には注意してください。一度noLibを使ったら、あなたのプロジェクトを他の人と共有しようとしたとき、noLibを\(またはあなたのLibを\)使うことを強制することになります。さらに悪いことに、もし彼らのコードをプロジェクトに持っていこうとすると、あなたのlibに基づくコードに変換する必要があるかもしれません。

### コンパイラターゲットの`lib.d.ts`に対する効果

コンパイラのターゲットを `es6`に設定すると`lib.d.ts`は`Promise`のようなより現代的なもの\(es6\)のための環境宣言を追加します。コンパイラターゲットがコードの環境を変えるという魔法の効果は、一部の人にとっては望ましいことです。他の人にとっては、コードと環境を合わせないといけないので、問題があります。

しかしそれでも、あなたの環境をきめ細かく制御したい場合は、次に述べる`--lib`オプションを使うべきです。

### libオプション

場合によっては、コンパイルターゲット\(生成されたJavaScriptのバージョン\)と環境ライブラリサポートの関係を切り離したい場合があります。2016年6月において一般的な例は、`Promise`です。たいていは`--target es5`のようにすることを望むと思います。しかし、それでも、`Promise`のような最新の機能を使いたい場合、これをサポートするために、`lib`コンパイラオプションを使って`lib`を明示的に制御することができます。

> 注意： `--lib`を使うと、`--target`のlibの魔法を切り離して、より細かい制御ができます。

このオプションをコマンドラインまたは`tsconfig.json`に指定することができます\(それを推奨します\)。

**コマンドライン**：

```text
tsc --target es5 --lib dom,es6
```

**tsconfig.json** ：

```javascript
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
  * scripthost
* ESNext By-Featureオプション\(バルク機能よりも小さい\)
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

> 注意： `--lib`オプションは非常に細かく調整された制御を提供します。したがって、たいていは、バルク機能と環境カテゴリから対象を選択すれば良いでしょう。 --libが指定されていない場合、デフォルトのライブラリが選択されます：
>
> * --target es5の場合 =&gt; es5、dom、scripthost
> * --target es6の場合 =&gt; es6、dom、dom.iterable、scripthost

私の個人的な推奨：

```javascript
"compilerOptions": {
    "target": "es5",
    "lib": ["es6", "dom"]
}
```

ES5にシンボル\(Symbol\)を含む例：

ターゲットがes5の場合、Symbol APIは含まれません。実際のところ`[ts]Cannot find name 'Symbol'`ようなエラーが表示されます。 "target": "es5"と "lib"を組み合わせて、TypeScriptにSymbol APIを提供することができます：

```javascript
"compilerOptions": {
    "target": "es5",
    "lib": ["es5", "dom", "scripthost", "es2015.symbol"]
}
```

## 古いJavaScriptエンジン用のポリフィル

> [この件に関するEgghead PRO Video](https://egghead.io/lessons/typescript-using-es6-and-esnext-with-typescript)

`Map`/`Set`や、`Promise`\(このリストは当然変更されるでしょう\)のような、いくつかのランタイム機能は、モダンな`lib`オプションで使用できるものがかなりあります。これらを使うには `core-js`を使うだけです。単に、インストールしてください：

```text
npm install core-js --save-dev
```

また、アプリケーションのエントリポイントにインポートを追加します。

```javascript
import "core-js";
```

それは、これらのランタイム機能をあなたのためにポリフィルしてくれるでしょう🌹

