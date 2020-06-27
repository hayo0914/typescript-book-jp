# 宣言空間

TypeScriptには、_変数_宣言空間と_型_宣言空間という2つの宣言空間があります。これらの概念については以下で解説します。

## 型宣言空間\(Type Declaration Space\)

型宣言空間には型アノテーションとして使用できるものが含まれています。例えば以下は型宣言です：

```typescript
class Foo {};
interface Bar {};
type Bas = {};
```

これは、 `Foo`、`Bar`、 `Bas`などを型名として使用できることを意味します。例:

```typescript
var foo: Foo;
var bar: Bar;
var bas: Bas;
```

あなたが `interface Bar`を持っていても、_変数宣言空間_に宣言されないので変数として使うことはできません。これを以下に示します。

```typescript
interface Bar {};
var bar = Bar; // ERROR: "cannot find name 'Bar'"
```

`cannot find name`と言うのは、_変数_宣言空間に`Bar`という名前が宣言されていないからです。それは次のトピック「変数宣言空間」につながります。

## 変数宣言空間\(Variable Declaration Space\)

変数宣言空間\(Variable Declaration Space\)には、変数として使用できるものもあります。`class Foo`は、型宣言空間に`Foo`型を宣言することを見てきました。驚かないでください。それは、_変数_宣言空間に対して、変数_Foo_を宣言します：

```typescript
class Foo {};
var someVar = Foo;
var someOtherVar = 123;
```

クラスを変数として渡したいことがあるので、これは素晴らしいことです。覚えておくこと：

* 型宣言空間にしか宣言されない `interface` のようなものを変数として使うことはできません

同じように、`var` を使って宣言したものは_変数_宣言空間だけに宣言されるので、型アノテーションとして使うことはできません：

```typescript
var foo = 123;
var bar: foo; // ERROR: "cannot find name 'foo'"
```

`cannot find name`というエラーが発生する理由は、_型_宣言空間で`foo`という名前が定義されていないからです。

