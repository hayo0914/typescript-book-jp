TypeScriptの#型推論

TypeScriptは、いくつかの簡単なルールに基づいて変数の型を推論(およびチェック)できます。これらのルール
シンプルなので、安全で安全でないコードを認識するために脳を鍛えることができます(これは私と私のチームメイトにとって非常に迅速に起こりました)。

> 流れるタイプは、私の脳内でタイプ情報の流れを想像するだけです。

## 変数の定義

変数の型は、定義によって推論されます。

```ts
let foo = 123; // foo is a `number`
let bar = "Hello"; // bar is a `string`
foo = bar; // Error: cannot assign `string` to a `number`
```

これは右から左に流れるタイプの例です。

## 関数の戻り値の型

戻り値の型は、return文によって推測されます。次の関数は `number`を返すと推測されます。

```ts
function add(a: number, b: number) {
    return a + b;
}
```

これは底部に流出するタイプの例です。

## 課題

関数のパラメータ/戻り値の型は、代入によっても推論することができる。 `foo`は`Adder`で、 `number`は`a`と `b`の型になります。

```ts
type Adder = (a: number, b: number) => number;
let foo: Adder = (a, b) => a + b;
```

この事実は、あなたが望むようにエラーを発生させる以下のコードによって実証することができます：

```ts
type Adder = (a: number, b: number) => number;
let foo: Adder = (a, b) => {
    a = "hello"; // Error: cannot assign `string` to a `number`
    return a + b;
}
```

これは、左から右に流れるタイプの例です。

コールバック引数の関数を作成する場合、同じ*代入*スタイル型の推論が機能します。結局のところ、 `argument  - > parameter`は単に変数代入の別の形です。

```ts
type Adder = (a: number, b: number) => number;
function iTakeAnAdder(adder: Adder) {
    return adder(1, 2);
}
iTakeAnAdder((a, b) => {
    // a = "hello"; // Would Error: cannot assign `string` to a `number`
    return a + b;
})
```

## 構造化

これらの単純なルールは、**構造化**(オブジェクトリテラル作成)の存在下でも機能します。たとえば、次のような場合、 `foo`の型は`{a：number、b：number} `と推測されます。

```ts
let foo = {
    a: 123,
    b: 456
};
// foo.a = "hello"; // Would Error: cannot assign `string` to a `number`
```

同様に配列について：

```ts
const bar = [1,2,3];
// bar[0] = "hello"; // Would error: cannot assign `string` to a `number`
```

そしてもちろんどんなネスティングでも：

```ts
let foo = {
    bar: [1, 3, 4]
};
// foo.bar[0] = 'hello'; // Would error: cannot assign `string` to a `number`
```

## 破壊

そしてもちろん、彼らはまた、両方のオブジェクトを破壊する作業をします：

```ts
let foo = {
    a: 123,
    b: 456
};
let {a} = foo;
// a = "hello"; // Would Error: cannot assign `string` to a `number`
```

配列：

```ts
const bar = [1, 2];
let [a, b] = bar;
// a = "hello"; // Would Error: cannot assign `string` to a `number`
```

関数のパラメータが推定できれば、その構造化されたプロパティも推定できます。例えばここでは引数を `a`/` b`のメンバーに分解します。

```ts
type Adder = (numbers: { a: number, b: number }) => number;
function iTakeAnAdder(adder: Adder) {
    return adder({ a: 1, b: 2 });
}
iTakeAnAdder(({a, b}) => { // Types of `a` and `b` are inferred
    // a = "hello"; // Would Error: cannot assign `string` to a `number`
    return a + b;
})
```

## ガードの種類

[Type Guards](./ typeGuard.md)がどのように(特に組合の場合に)型を変更したり絞り込んだりするのを見てきました。型ガードは、ブロック内の変数の型推論の別の形式です。

## 警告

### パラメータの周りに注意してください

代入から推論できない場合、型は関数パラメータに流れません。たとえば次のような場合、コンパイラは `foo`の型を知らないので、`a`や `b`の型を推論することはできません。

```ts
const foo = (a,b) => { /* do something */ };
```

しかし、 `foo`がタイプされた場合、関数パラメータの型を推論することができます(`a`、 `b`は両方とも以下の例では`number`型であると推測されます)。

```ts
type TwoNumberFunction = (a: number, b: number) => void;
const foo: TwoNumberFunction = (a, b) => { /* do something */ };
```

### 返品については注意してください

TypeScriptは一般的に関数の戻り値の型を推測することができますが、期待どおりではない可能性があります。例えば、ここでは関数 `foo`は`any`の戻り値の型を持っています。

```ts
function foo(a: number, b: number) {
    return a + addOne(b);
}
// Some external function in a library someone wrote in JavaScript
function addOne(a) {
    return a + 1;
}
```

これは、戻り値の型が `addOne`(`a`は `any`なので`addOne`の戻り値は `any`なので`foo`の戻り値は `any`)の型定義が悪いためです。

> 関数の返り値を明示するのが最も簡単だと分かります。結局のところ、これらの注釈は定理であり、関数本体は証明である。

想像できる他のケースもありますが、良いニュースは、そのようなバグを捕まえるのに役立つコンパイラフラグがあることです。

## `noImplicitAny`

フラグ `noImplicitAny`は、変数の型を推測できない場合(したがって、暗黙の*`any`型としてしか持つことができない場合)、エラーを発生させるようにコンパイラに指示します。そうすることができます

* どちらかと言うと*どちらかというと、 `：any '型の注釈を明示的に*加えることで`any`型にしたい
* いくつかの*正しい*注釈を追加することによってコンパイラを助けます。
