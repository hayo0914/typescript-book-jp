# TypeScriptスタイルガイドとコーディング規約

> 非公式のTypeScriptスタイルガイド

人々はこれについて私の意見を求めてきました。個人的に私は私のチームやプロジェクトにこれらのことをたくさん施行していませんが、そうした強い一貫性を持つ必要があると感じる人は、タイブレーカーとして言及することが役に立ちます。私ははるかに強く感じることがあり、[ヒントの章]（../ tips / main.md）で扱われています（例えば、タイプアサーションが悪い、プロパティーセッターが悪い）。

主要セクション：

* [変数]（#変数と関数）
* [クラス]（#クラス）
* [インタフェース]（#インタフェース）
* [タイプ]（#タイプ）
* [名前空間]（#名前空間）
* [Enum]（#enum）
* [`null`と`undefined`]（#null-vs-undefined）
* [書式設定]（#書式設定）
* [一重引用符と二重引用符]（#引用符）
* [Tabs vs. Spaces]（スペース数）
* [セミコロンを使用]（セミコロン）
* [配列を `Type []`として注釈する（#配列）
* [ファイル名]（#filename）
* [`type`対`interface`]（#type-vs-interface）

## 変数と関数
* 変数と関数名には `camelCase`を使います

> 理由：従来のJavaScript

** 悪い**
```ts
var FooVar;
function BarFunc() { }
```
** 良い**
```ts
var fooVar;
function barFunc() { }
```

## クラス
* クラス名には `PascalCase`を使います。

> 理由：これは実際には標準のJavaScriptではかなり一般的です。

** 悪い**
```ts
class foo { }
```
** 良い**
```ts
class Foo { }
```
* クラスメンバーとメソッドの `camelCase`を使う

> 理由：当然のことながら、変数と関数の命名規則に従います。

** 悪い**
```ts
class Foo {
    Bar: number;
    Baz() { }
}
```
** 良い**
```ts
class Foo {
    bar: number;
    baz() { }
}
```
## インタフェース

* 名前には `PascalCase`を使います。

> 理由：クラスに似ています

* メンバーには `camelCase`を使います。

> 理由：クラスに似ています

* **プレフィックスに `I`をつけないでください

> Reason：Unconventional。 `lib.d.ts`は`I`のない重要なインターフェース（例えば、Window、Documentなど）を定義します。

** 悪い**
```ts
interface IFoo {
}
```
** 良い**
```ts
interface Foo {
}
```

## タイプ

* 名前には `PascalCase`を使います。

> 理由：クラスに似ています

* メンバーには `camelCase`を使います。

> 理由：クラスに似ています


## 名前空間

* 名前に `PascalCase`を使用する

> 理由：TypeScriptチームに続くコンベンション。名前空間は事実上静的メンバーを持つクラスです。クラス名は `PascalCase`=>名前空間名は` PascalCase`です

** 悪い**
```ts
namespace foo {
}
```
** 良い**
```ts
namespace Foo {
}
```

## Enum

* enum名には `PascalCase`を使います

> 理由：クラスに似ています。タイプです。

** 悪い**
```ts
enum color {
}
```
** 良い**
```ts
enum Color {
}
```

* enumメンバーに `PascalCase`を使用する

> 理由：文字列作成者、例えばSyntaxKind.StringLiteralのようなTypeScriptチームに続くコンベンション。他の言語の翻訳（コード生成）をTypeScriptにも役立ちます。

** 悪い**
```ts
enum Color {
    red
}
```
** 良い**
```ts
enum Color {
    Red
}
```

## Null対Undefined

* 明示的に使用不可能にするためにどちらも使用しないことを推奨します。

> 理由：これらの値は、値間の一貫した構造を維持するためによく使用されます。 TypeScriptでは* types *を使用して構造体を表します

** 悪い**
```ts
let foo = {x:123,y:undefined};
```
** 良い**
```ts
let foo:{x:number,y?:number} = {x:123};
```

* 一般的に `undefined`を使用してください（代わりに`{valid：boolean、value？：Foo} `のようなオブジェクトを返すことを検討してください）

*** 悪い***
```ts
return null;
```
*** 良い***
```ts
return undefined;
```

* APIまたは従来のAPIの一部である場合は `null 'を使用します

> 理由：Node.jsでは従来通りです。 NodeBackスタイルコールバックの `error`は`null`です。

** 悪い**
```ts
cb(undefined)
```
** 良い**
```ts
cb(null)
```

* * truthy *を使用すると、**オブジェクト**が `null`または`undefined`であるかどうかをチェックします。

** 悪い**
```ts
if (error === null)
```
** 良い**
```ts
if (error)
```

* プリミティブに ``null` / `undefined`をチェックするには、`== undefined` / `！= undefined`（`=== `/`！== ` `` `、`0`、 `false`のような）他の偽の値ではありません。

** 悪い**
```ts
if (error !== null)
```
** 良い**
```ts
if (error != undefined)
```

## フォーマット
TypeScriptコンパイラには、非常に優れた書式言語サービスが付属しています。デフォルトで出力される出力は、チームの認知負荷を軽減するのに十分です。

コマンドラインでコードを自動的にフォーマットするには、[`tsfmt`]（https://github.com/vvakame/typescript-formatter）を使います。また、あなたのIDE（atom / vscode / vs / sublime）には、すでにフォーマットサポートが組み込まれています。

例：
```ts
// Space before type i.e. foo:<space>string
const foo: string = "hello";
```

## 引用

* エスケープしない限り、一重引用符（ ``）を使用することをお勧めします。

> 理由：他のJavaScriptチームがこれを行います（[airbnb]（https://github.com/airbnb/javascript）、[標準]（https://github.com/feross/standard）、[npm]（https： //github.com/npm/npm）、[ノード]（https://github.com/nodejs/node）、[google / angular]（https://github.com/angular/angular/）、[facebook /react](https://github.com/facebook/react））。入力が簡単です（ほとんどのキーボードでシフトが必要ありません）。 [Prettierチームは一重引用符もお勧めします]（https://github.com/prettier/prettier/issues/1105）

> 二重引用符にはメリットがありません：オブジェクトをJSONに簡単にコピーできます。ユーザーが他の言語を使用して、引用文字を変更せずに作業できるようにします。たとえばアポストロフィを使用できます。 「彼は行かない。しかし、私は、JSコミュニティが公正に決定された場所から逸脱することはありません。

* 二重引用符を使用できない場合は、バックティック（\ `）を使用してみてください。

> 理由：これらは一般に、複雑な文字列の意図を表しています。

## スペース

* `2 'スペースを使います。タブではありません。

> 理由：他のJavaScriptチームがこれを行います（[airbnb]（https://github.com/airbnb/javascript）、[idiomatic]（https://github.com/rwaldron/idiomatic.js）、[標準]（ https://github.com/feross/standard）、[npm]（https://github.com/npm/npm）、[node]（https://github.com/nodejs/node）、[google / （https://github.com/angular/angular/）、[facebook / react]（https://github.com/facebook/react）を参照してください）。 TypeScript / VSCodeチームは4つのスペースを使用しますが、間違いなくエコシステムの例外です。

## セミコロン

* セミコロンを使用してください。

> 理由：明示的なセミコロンは、言語書式設定ツールで一貫した結果を得るのに役立ちます。不足しているASI（自動セミコロン挿入）は、新しい開発者を旅行させることができます。 `foo（）\ n（function（）{}）`は1つのステートメント（2つではない）です。 TC39でもお勧めします。

## 配列

* 配列に `foos：Array <Foo>`の代わりに `foos：Foo []`として配列に注釈をつけます。

> 理由：読みやすい。 TypeScriptチームによって使用されます。心が `[]`を検出するように訓練されているので、何かが配列であることを知りやすくなります。

## ファイル名
`camelCase`を使ってファイルに名前を付けます。例えば。 `accordian.tsx`、`myControl.tsx`、 `utils.ts`、`map.ts`などです。

> 理由：多くのJSチームに在籍していました。

## 型vsインタフェース

* ユニオンや交差点が必要な場合には `type`を使います：

```
type Foo = number | { someProperty: number }
```
* `extend`や`implements`をしたいときは `interface`を使います。

```
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
