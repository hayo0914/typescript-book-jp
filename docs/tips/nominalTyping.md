## Normal Typing
TypeScriptの型システムは構造的です。そして、[これはTypeScriptを使う理由の一つ](../why-typescript.md)です。しかし、同じ構造を持っていても、2つの変数が異なる*型名*を持つ2つの変数を区別する必要があるシステムのユースケースがあります。非常に一般的な使用例は、identity構造(一般的にC#/Javaなどの言語において*名前*と関連するセマンティクスを持つただの文字列)です。

コミュニティでは、いくつかのパターンが登場しています。私の個人的な好みで降順に説明します:

## リテラル型の使用

このパターンは、ジェネリックとリテラル型を使用します。

```ts
/** Generic Id type */
type Id<T extends string> = {
  type: T,
  value: string,
}

/** Specific Id types */
type FooId = Id<'foo'>;
type BarId = Id<'bar'>;

/** Optional: contructors functions */
const createFoo = (value: string): FooId => ({ type: 'foo', value });
const createBar = (value: string): BarId => ({ type: 'bar', value });

let foo = createFoo('sample')
let bar = createBar('sample');

foo = bar; // Error
foo = foo; // Okay
```

* アドバンテージ
   - どの型アサーションも必要ありません
* デメリット
   - `{type,value}`のような構造は望ましくない可能性があり、サーバ側のシリアライズのサポートが必要です

## Enumsを使う
[TypeScriptのEnums](../enums.md)は、一定のレベルのnominal型付けを提供します。2つの列挙型は、名前が異なる場合、等しくありません。この事実を利用して、構造的に互換性のある型に対してnominal型付けを提供することができます。

この回避策には、以下が含まれます。
* 種類を表すenumを作成する
* enumと実際の構造の(intersection `＆`)としての型を作成する

下記のデモで示します。その構造の型はただの文字列です:

```ts
// FOO
enum FooIdBrand {}
type FooId = FooIdBrand & string;

// BAR
enum BarIdBrand {}
type BarId = BarIdBrand & string;

/**
 * Usage Demo
 */
var fooId: FooId;
var barId: BarId;

// Safety!
fooId = barId; // error
barId = fooId; // error

// Newing up
fooId = 'foo' as FooId;
barId = 'bar' as BarId;

// Both types are compatible with the base
var str: string;
str = fooId;
str = barId;
```

## インタフェースの使用

`numbers`は`enum`と型互換性があるため、これまでの手法は使用できません。代わりに、インターフェイスを使用して構造の互換性を破ることができます。この方法はTypeScriptコンパイラチームによっても使用されているので、言及する価値があります。`_`プレフィックスと`Brand`サフィックスを使用する規約を強くお薦めします(そして、[TypeScriptチームに採用されている規約です](https://github.com/Microsoft/TypeScript/blob/7b48a182c05ea4dea81bab73ecbbe9e013a79e99/src/compiler/types.ts#L693-L698))。

この回避策には、以下が含まれます。
* 構造上の互換性を破るために、型に未使用のプロパティを追加する。
* 新しくオブジェクトを作成したり、ダウンキャストが必要な場合は、型アサーションを使用します。

これは以下のとおりです：

```ts
// FOO
interface FooId extends String {
    _fooIdBrand: string; // To prevent type errors
}

// BAR
interface BarId extends String {
    _barIdBrand: string; // To prevent type errors
}

/**
 * Usage Demo
 */
var fooId: FooId;
var barId: BarId;

// Safety!
fooId = barId; // error
barId = fooId; // error
fooId = <FooId>barId; // error
barId = <BarId>fooId; // error

// Newing up
fooId = 'foo' as any;
barId = 'bar' as any;

// If you need the base string
var str: string;
str = fooId as any;
str = barId as any;
```
