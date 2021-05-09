# 型推論

TypeScriptは、いくつかの簡単なルールに基づいて変数の型を推論\(およびチェック\)します。これらのルールはシンプルなので、安全/安全でないコードを認識するために、脳に記憶することができます\(これは私と私のチームメイトでは非常にすぐでした\)。

> 型の流れは、私が頭の中で想像する型情報の流れとちょうど一致しています

## 変数の定義\(Variable Definition\)

変数の型は、定義によって推論されます。

```typescript
let foo = 123; // foo is a `number`
let bar = "Hello"; // bar is a `string`
foo = bar; // Error: cannot assign `string` to a `number`
```

これは右から左に流れる型の例です。

## 関数の戻り値の型\(Function Return Types\)

戻り値の型は、return文によって推測されます。次の関数は`number`を返すと推測されます。

```typescript
function add(a: number, b: number) {
    return a + b;
}
```

これは底から流れ出ていく型の例です。

## 代入\(Assignment\)

関数のパラメータ/戻り値の型は、代入によっても推論することができます。`foo`は`Adder`で、`number`は`a`と `b`の型になります。

```typescript
type Adder = (a: number, b: number) => number;
let foo: Adder = (a, b) => a + b;
```

この事実は、以下のコードで示すことができます。あなたが期待する通りのエラーが発生します：

```typescript
type Adder = (a: number, b: number) => number;
let foo: Adder = (a, b) => {
    a = "hello"; // Error: cannot assign `string` to a `number`
    return a + b;
}
```

これは、左から右に流れる型の例です。

コールバック引数の関数を作成する場合、同じ代入スタイルの型推論が機能します。結局のところ、`argument -> parameter`は単に変数代入の一種です。

```typescript
type Adder = (a: number, b: number) => number;
function iTakeAnAdder(adder: Adder) {
    return adder(1, 2);
}
iTakeAnAdder((a, b) => {
    // a = "hello"; // Would Error: cannot assign `string` to a `number`
    return a + b;
})
```

## 構造化\(Structuring\)

これらの単純なルールは、**構造化**\(オブジェクトリテラルの作成\)の下でも機能します。たとえば、次のような場合、`foo`の型は`{a:number, b:number}`と推論されます。

```typescript
let foo = {
    a: 123,
    b: 456
};
// foo.a = "hello"; // Would Error: cannot assign `string` to a `number`
```

同様に配列について：

```typescript
const bar = [1,2,3];
// bar[0] = "hello"; // Would error: cannot assign `string` to a `number`
```

そしてもちろんどんなネストでも：

```typescript
let foo = {
    bar: [1, 3, 4]
};
// foo.bar[0] = 'hello'; // Would error: cannot assign `string` to a `number`
```

## 分解\(Destructuring\)

そしてもちろん、構造の分解でも機能します:

```typescript
let foo = {
    a: 123,
    b: 456
};
let {a} = foo;
// a = "hello"; // Would Error: cannot assign `string` to a `number`
```

配列：

```typescript
const bar = [1, 2];
let [a, b] = bar;
// a = "hello"; // Would Error: cannot assign `string` to a `number`
```

関数のパラメータの型が推測できれば、その構造化されたプロパティも同様に推測されます。例えばここでは引数を`a`/`b`のメンバに分解します。

```typescript
type Adder = (numbers: { a: number, b: number }) => number;
function iTakeAnAdder(adder: Adder) {
    return adder({ a: 1, b: 2 });
}
iTakeAnAdder(({a, b}) => { // Types of `a` and `b` are inferred
    // a = "hello"; // Would Error: cannot assign `string` to a `number`
    return a + b;
})
```

## Type Guard \(Type Guards\)

[Type Guard](typeguard.md)が\(特にユニオン型の場合に\)どのように型を変更したり絞り込んだりするのかを見てきました。TypeGuardは、ブロック内の変数の型推論の別の形式です。

## 警告\(Warnings\)

### パラメータに注意してください

代入から推論できない場合、型は関数パラメータに流れません。たとえば次のような場合、コンパイラは`foo`の型を知らないので、`a`や`b`の型を推論することはできません。

```typescript
const foo = (a,b) => { /* do something */ };
```

しかし、 `foo`に型を指定された場合、関数パラメータの型を推論することができます\(以下の例では`a`、`b`は両方とも`number`型であると推測されます\)。

```typescript
type TwoNumberFunction = (a: number, b: number) => void;
const foo: TwoNumberFunction = (a, b) => { /* do something */ };
```

### returnに注意してください

TypeScriptは一般的に関数の戻り値の型を推測することができますが、期待通りではない可能性があります。例えば、ここでは関数`foo`は`any`の戻り値の型を持っています。

```typescript
function foo(a: number, b: number) {
    return a + addOne(b);
}
// Some external function in a library someone wrote in JavaScript
function addOne(a) {
    return a + 1;
}
```

これは、`addOne`の型定義が悪いため、fooの戻り値の型が影響を受けたものです\(`a`は`any`なので`addOne`の戻り値は`any`で、`foo`の戻り値は`any`\)。

> 関数の返り値を明示するのが最も簡単だと分かります。結局のところ、これらのアノテーションは定理であり、関数本体が証明です。

想像できる他のケースもありますが、良いニュースは、そのようなバグを捕まえるのに役立つコンパイラフラグがあることです。

## `noImplicitAny`

フラグ `noImplicitAny`は、変数の型を推測できない場合\(したがって、暗黙の`any`型としてしか持つことができない場合\)、エラーを発生させるようにコンパイラに指示します。それによって、次のことが可能です。

* そうしたい場合は、明示的に`：any`型の注釈を加えることで`any`型にしたい
* 正しいアノテーションを追加することによってコンパイラを助ける

