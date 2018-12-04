# 移動タイプ

TypeScriptのタイプシステムは非常に強力で、そこでは他の言語では不可能な方法で移動とスライシングが可能です。

これは、TypeScriptが、JavaScriptなどの高度に動的な言語でシームレスに作業できるように設計されているためです。ここでは、TypeScriptでタイプを移動するためのいくつかのトリックについて説明します。

これらの主な動機：あなたは1つのことを変更し、他のものはすべて自動的に更新され、うまく設計された制約システムのように、

## Type + Valueの両方をコピーする

クラスを移動したい場合は、次の操作を行うことができます。

```ts
class Foo { }
var Bar = Foo;
var bar: Bar; // ERROR: cannot find name 'Bar'
```

これはエラーです。なぜなら、 `var`は`Foo`を*変数*宣言空間にコピーしただけなので、型の注釈として `Bar`を使うことができないからです。正しい方法は、 `import`キーワードを使うことです。 * namespaces *や* modules *を使用している場合にのみ、 `import`キーワードをこのように使用することができます（詳細は後で説明します）。

```ts
namespace importing {
    export class Foo { }
}

import Bar = importing.Foo;
var bar: Bar; // Okay
```

この `import 'トリックは、*型と変数*の両方で機能します。

## 変数の型を取り込む

`typeof`演算子を使用して、型の注釈で実際に変数を使用することができます。これにより、ある変数が別の変数と同じ型であることをコンパイラに伝えることができます。これを実証する例を以下に示します。

```ts
var foo = 123;
var bar: typeof foo; // `bar` has the same type as `foo` (here `number`)
bar = 456; // Okay
bar = '789'; // ERROR: Type `string` is not `assignable` to type `number`
```

## クラスメンバーのタイプを取得する

変数の型を取り込むのと同様に、単に型取得の目的で変数を宣言するだけです。

```ts
class Foo {
  foo: number; // some member whose type we want to capture
}

// Purely to capture type
declare let _foo: Foo;

// Same as before
let bar: typeof _foo.foo;
```

## マジック文字列の種類を取得する

多くのJavaScriptライブラリとフレームワークは、生のJavaScript文字列を処理します。 `const`変数を使用してその型を取り込むことができます。

```ts
// Capture both the *type* and *value* of magic string:
const foo = "Hello World";

// Use the captured type:
let bar: typeof foo;

// bar can only ever be assigned to `Hello World`
bar = "Hello World"; // Okay!
bar = "anything else "; // Error!
```

この例では、 `bar`はリテラルタイプ` `Hello World '`を持っています。これについては、[リテラルタイプのセクション]（https://basarat.gitbooks.io/typescript/content/docs/types/literal-types.html "リテラルタイプ"）を参照してください。

## キー名のキャプチャ

`keyof`演算子を使うと、ある型のキー名を取得できます。例えば。変数のキー名を `typeof`を使って最初に取得することでそれを取得することができます：

```ts
const colors = {
  red: 'red',
  blue: 'blue'
}
type Colors = keyof typeof colors;

let color: Colors; // same as let color: "red" | "blue"
color = 'red'; // okay
color = 'blue'; // okay
color = 'anythingElse'; // Error
```

上記の例のように、文字列列挙型+定数のようなものを簡単に作成することができます。
