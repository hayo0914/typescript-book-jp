# スタイルガイド（コーディング規約）

> 非公式のTypeScriptスタイルガイド

スタイルガイドについて意見を求められることはよくあります。個人的には、私は自分のチームやプロジェクトにコーディングスタイルをあまり強制してはいませんが、コードに一貫性が必要だと思う人がいるような状況において、基準として以下で述べるようなスタイルガイドがあることが役に立つのは確かです。個人的にはスタイルよりもはるかに強い意見を持っている観点があり、それについては[ヒントの章](main-1/)で説明しています（例えば、型アサーションはよくない、プロパティーsetterはよくない、など）🌹

主要セクション：

* [変数](styleguide.md#変数と関数)
* [クラス](styleguide.md#クラス)
* [インターフェース](styleguide.md#インターフェース)
* [タイプ](styleguide.md#タイプ)
* [名前空間](styleguide.md#名前空間)
* [Enum](styleguide.md#enum)
* [`null` vs `undefined`](styleguide.md#null-vs-undefined)
* [書式設定](styleguide.md#書式設定)
* [一重引用符と二重引用符](styleguide.md#引用符)
* [タブ vs ](styleguide.md#スペース数)
* [セミコロン](styleguide.md#セミコロン)
* [配列](styleguide.md#配列)
* [ファイル名](styleguide.md#filename)
* [`type` vs `interface`](styleguide.md#type-vs-interface)

## 変数と関数 {#変数と関数}

* 変数と関数名には `camelCase`を使います

> 理由：従来のJavaScript

**悪い**

```typescript
var FooVar;
function BarFunc() { }
```

**良い**

```typescript
var fooVar;
function barFunc() { }
```

## クラス {#クラス}

* クラス名には `PascalCase`を使います。

> 理由：これは実際には標準のJavaScriptではかなり一般的です。

**悪い**

```typescript
class foo { }
```

**良い**

```typescript
class Foo { }
```

* クラスメンバとメソッドの `camelCase`を使う

> 理由：当然のことながら、変数と関数の命名規則に従います。

**悪い**

```typescript
class Foo {
    Bar: number;
    Baz() { }
}
```

**良い**

```typescript
class Foo {
    bar: number;
    baz() { }
}
```

## インターフェース {#インターフェース}

* 名前には`PascalCase`を使います。

> 理由：クラスに似ています

* メンバには`camelCase`を使います。

> 理由：クラスに似ています

* プレフィックスに`I`をつけないでください

> Reason： 慣例的ではないため。`lib.d.ts`は`I`のない重要なインターフェース\(例えば、Window、Documentなど\)を定義します。

**悪い**

```typescript
interface IFoo {
}
```

**良い**

```typescript
interface Foo {
}
```

## タイプ {#タイプ}

* 名前には`PascalCase`を使います。

> 理由：クラスに似ています

* メンバには`camelCase`を使います。

> 理由：クラスに似ています

## 名前空間 {#名前空間}

* 名前に`PascalCase`を使用する

> 理由：TypeScriptチームに続くコンベンション。名前空間は事実上静的メンバを持つクラスです。クラス名は`PascalCase`=&gt;名前空間名は`PascalCase`です

**悪い**

```typescript
namespace foo {
}
```

**良い**

```typescript
namespace Foo {
}
```

## Enum {#enum}

* enum名には`PascalCase`を使います

> 理由：クラスに似ています。タイプです。

**悪い**

```typescript
enum color {
}
```

**良い**

```typescript
enum Color {
}
```

* enumメンバに `PascalCase`を使用する

> 理由：言語作成者、TypeScriptチームに従った慣例です。例えば`SyntaxKind.StringLiteral`です。他の言語からTypeScriptへの翻訳\(コード生成\)にも役立ちます。

**悪い**

```typescript
enum Color {
    red
}
```

**良い**

```typescript
enum Color {
    Red
}
```

## `null` vs `undefined` {#null-vs-undefined}

* 明示的に使用不可能にするために、どちらも使用しないことを推奨します。

> 理由：これらの値は、値間の一貫した構造を維持するためによく使用されます。TypeScriptでは型を使用して構造を表します

**悪い**

```typescript
let foo = { x: 123, y: undefined };
```

**良い**

```typescript
let foo: { x: number, y?: number } = { x: 123 };
```

* 一般的に `undefined`を使用してください\(代わりに`{valid:boolean,value?:Foo}`のようなオブジェクトを返すことを検討してください\)

_**悪い**_

```typescript
return null;
```

_**良い**_

```typescript
return undefined;
```

* APIまたは従来のAPIの一部である場合は`null`を使用します

> 理由：Node.jsの慣例通りです。NodeBackスタイルコールバックの`error`は`null`です。

**悪い**

```typescript
cb(undefined)
```

**良い**

```typescript
cb(null)
```

* _truthy_を使用すると、**オブジェクト**が `null`または`undefined`であるかどうかをチェックできます。

**悪い**

```typescript
if (error === null)
```

**良い**

```typescript
if (error)
```

* プリミティブに`null`/`undefined`をチェックするには、`== undefined`/`!= undefined`を使います。これは`null`/`undefined`の両方に働きます。しかし、他の_falsy_値には使わないでください\(例:`''`,`0`,`false`\)。

**悪い**

```typescript
if (error !== null)
```

**良い**

```typescript
if (error != undefined)
```

## フォーマット {#書式設定}

TypeScriptコンパイラには、非常に優れた言語フォーマットのサービスが付属しています。デフォルトで出力される出力は、チームの認知負荷を軽減するのに十分です。

コマンドラインでコードを自動的にフォーマットするには、 [`tsfmt`](https://github.com/vvakame/typescript-formatter) を使います。また、あなたのIDE\(atom/ vscode/vs/sublime\)には、すでにフォーマットのサポートが組み込まれています。

例：

```typescript
// 型の前にスペースを入れます。つまり、 foo:<スペース>string のようにします。
const foo: string = "hello";
```

## 引用符 {#引用符}

* エスケープしない限り、シングルクォート\(`'`\)を使用することをお勧めします。

> 理由：他のJavaScriptチームがこれを行っています\([airbnb](https://github.com/airbnb/javascript)、[標準](https://github.com/feross/standard)、[npm](https://github.com/npm/npm)、[NodeJS](https://github.com/nodejs/node)、[google/angular](https://github.com/angular/angular/)、[facebook/react](https://github.com/facebook/react)\)。入力が簡単です\(ほとんどのキーボードでシフトが必要ありません\)。[Prettierチームもシングルクォートを勧めています](https://github.com/prettier/prettier/issues/1105)
>
> ダブルクォートはメリットがないわけではありません: オブジェクトをJSONに簡単にコピーできます。ユーザーが他の言語を使用して、引用文字を変更せずに作業できるようにします。たとえばアポストロフィを使用できます。例えば、`He's not going.`。しかし、私は、JSコミュニティが公正に決定したものから逸脱することはありません。

* ダブルクォートを使用できない場合は、バックティック\(\`\)を使用してみてください。

> 理由：これらは一般に、十分複雑な文字列の意図を表しています。

## スペース {#スペース数}

* `2`つのスペースを使います。タブではありません。

> 理由：他のJavaScriptチームがこれを行っています\([airbnb](https://github.com/airbnb/javascript)、[idiomatic](https://github.com/rwaldron/idiomatic.js)、[標準](https://github.com/feross/standard)、[npm](https://github.com/npm/npm)、[node](https://github.com/nodejs/node)、[google/angular](https://github.com/angular/angular/)、[facebook/react](https://github.com/facebook/react)を参照してください\)。 TypeScript/VSCodeチームは4つのスペースを使用しますが、間違いなくエコシステムの例外です。

## セミコロン {#セミコロン}

* セミコロンを使用してください。

> 理由：明示的なセミコロンは、言語書式設定ツールで一貫した結果を得るのに役立ちます。Missing ASI\(Automatic semicolon insertion: 自動セミコロン挿入\)は、例えば`foo() \n (function(){})`を単一の文\(2つではなく\)と間違えます。TC39でも同様に勧められています。

## 配列 {#配列}

* 配列に`foos: Array<Foo>`の代わりに`foos: Foo[]`として配列にアノテーションをつけます。

> 理由：読みやすい。TypeScriptチームによって使用されています。脳が`[]`を検出するように訓練されているので、何かが配列であることを知りやすくなります。

## ファイル名 {#filename}

`camelCase`を使ってファイルに名前を付けます。例えば`accordion.tsx`、`myControl.tsx`、`utils.ts`、`map.ts`などです。

> 理由：多くのJSチームで慣習的です。

## `type` vs `interface` {#type-vs-interface}

* ユニオン型や交差型が必要な場合には`type`を使います：

```typescript
type Foo = number | { someProperty: number }
```

* `extend`や`implements`をしたいときは`interface`を使います。

```typescript
interface Foo {
  foo: string;
}
interface FooBar extends Foo {
  bar: string;
}
class X implements FooBar {
  foo: string;
  bar: string;
}
```

* そうでなければ、その日あなたを幸せにするものを使用してください。

