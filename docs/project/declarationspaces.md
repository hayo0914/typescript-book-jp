## 宣言空間(Declaration Spaces)

TypeScriptには、*変数*宣言空間と*型*宣言空間という2つの宣言空間があります。これらの概念については以下で解説します。

### 型宣言空間(Type Declaration Space)
型宣言空間には型アノテーションとして使用できるものが含まれています。例えば以下は型宣言です：

```ts
class Foo {};
interface Bar {};
type Bas = {};
```
これは、 `Foo`、`Bar`、 `Bas`などを型名として使用できることを意味します。例:

```ts
var foo: Foo;
var bar: Bar;
var bas: Bas;
```

あなたが `interface Bar`を持っていても、*変数宣言空間*に宣言されないので変数として使うことはできません。これを以下に示します。

```ts
interface Bar {};
var bar = Bar; // ERROR: "cannot find name 'Bar'"
```

`cannot find name`と言うのは、*変数*宣言空間に`Bar`という名前が宣言されていないからです。それは次のトピック「変数宣言空間」につながります。

### 変数宣言空間(Variable Declaration Space)
変数宣言空間(Variable Declaration Space)には、変数として使用できるものが含まれています。`class Foo`は、`Foo`型が型宣言空間に宣言されることがわかりました。何だと思いますか？それは、*変数*宣言空間に対しても、以下のように変数*Foo*を宣言します：

```ts
class Foo {};
var someVar = Foo;
var someOtherVar = 123;
```
クラスを変数として渡したいことがあるので、これは素晴らしいことです。覚えておくこと：

* 型宣言空間にしか宣言されない`interface`のようなものを変数として使うことはできません

同様に、`var`を使って宣言したものは*変数*宣言空間だけに宣言されるものであり、型アノテーションとして使うことはできません：

```ts
var foo = 123;
var bar: foo; // ERROR: "cannot find name 'foo'"
```
`cannot find name`と言うエラーは、*型*宣言空間で`foo`という名前が定義されていないからです。
