## 公称タイピング
TypeScript型のシステムは構造的です(これは主な動機の一つです)。(../ why-typescript.md)しかし、同じ構造を持っていても、2つの変数が異なる*タイプ名*を持つため、2つの変数を区別する必要があるシステムでは、実際の使用例があります。非常に一般的な使用例は、* identity *構造(一般にC#/ Javaなどの言語で* name *に関連付けられたセマンティクスを持つ文字列です)です。

コミュニティにはいくつかのパターンがあります。私はそれらを個人的な好みの降順でカバーする：

## リテラル型の使用

このパターンは、ジェネリック型とリテラル型を使用します。

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

* メリット
   - どのタイプアサーションも必要ありません
* 不利益
   - 構造体 `{type、value}`は望ましくない可能性があり、サーバの直列化のサポートが必要です

## Enumを使う
[TypeScriptのEnums](../ enums.md)は、特定のレベルの名目型を提供します。 2つの列挙型は、名前が異なる場合、等しくありません。この事実を利用して、構造的に互換性のある型に対して公称型を提供することができます。

回避策は次のとおりです。
* *ブランド* enumを作成する。
* ブランドenumの*交差*( `＆`)としての型の作成+実際の構造。

これは、型の構造が単なる文字列であるところで以下に説明されています：

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

`numbers`は`enum`と型互換性があるため、これまでの手法は使用できません。代わりに、インターフェイスを使用して構造の互換性を破ることができます。このメソッドはまだTypeScriptコンパイラチームによって使用されているので、言及する価値があります。 `_`接頭辞と`Brand`接尾辞を使用することを強くお勧めします(そして、[TypeScriptチームに続く人](https://github.com/Microsoft/TypeScript/blob/7b48a182c05ea4dea81bab73ecbbe9e013a79e99/src/compiler/types)。 .ts#L693-L698))。

この回避策には、以下が含まれます。
構造上の互換性を損なうために、型に未使用のプロパティを追加する。
* 新しいアサーションやキャストダウンが必要な場合は、型アサーションを使用します。

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
