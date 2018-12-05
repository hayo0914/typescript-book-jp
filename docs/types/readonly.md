## readonly
TypeScriptのタイプシステムでは、インターフェイス上の個々のプロパティを `readonly`としてマークすることができます。これにより、機能的な方法で作業することができます(予期せぬ突然変異は悪い)。

```ts
function foo(config: {
    readonly bar: number,
    readonly bas: number
}) {
    // ..
}

let config = { bar: 123, bas: 123 };
foo(config);
// You can be sure that `config` isn't changed 🌹
```

もちろん `interface`と`type`の定義に `readonly`を使うこともできます：

```ts
type Foo = {
    readonly bar: number;
    readonly bas: number;
}

// Initialization is okay
let foo: Foo = { bar: 123, bas: 456 };

// Mutation is not
foo.bar = 456; // Error: Left-hand side of assignment expression cannot be a constant or a read-only property
```

クラスプロパティを `readonly`として宣言することもできます。次のように、宣言のポイントまたはコンストラクタで初期化することができます。

```ts
class Foo {
    readonly bar = 1; // OK
    readonly baz: string;
    constructor() {
        this.baz = "hello"; // OK
    }
}
```

## Readonly
`Readonly`型は`T`型をとり、そのすべてのプロパティをマップ型を使って `readonly`とマークします。実際にそれを使用するデモがあります：

```ts
type Foo = {
  bar: number;
  bas: number;
}

type FooReadonly = Readonly<Foo>; 

let foo:Foo = {bar: 123, bas: 456};
let fooReadonly:FooReadonly = {bar: 123, bas: 456};

foo.bar = 456; // Okay
fooReadonly.bar = 456; // ERROR: bar is readonly
```

### さまざまな使用例

#### ReactJS
不変性を愛するライブラリの1つがReactJSです。たとえば、あなたの `Props`と`State`には不変であるとマークすることができます：

```ts
interface Props {
    readonly foo: number;
}
interface State {
    readonly bar: number;
}
export class Something extends React.Component<Props,State> {
  someMethod() {
    // You can rest assured no one is going to do
    this.props.foo = 123; // ERROR: (props are immutable)
    this.state.baz = 456; // ERROR: (one should use this.setState)  
  }
}
```

しかし、Reactの型定義として、これらを `readonly`としてマークする必要はありません(渡されたジェネリック型を上で述べた`Readonly`型で内部的にラップすることによって)。

```ts
export class Something extends React.Component<{ foo: number }, { baz: number }> {
  // You can rest assured no one is going to do
  someMethod() {
    this.props.foo = 123; // ERROR: (props are immutable)
    this.state.baz = 456; // ERROR: (one should use this.setState)  
  }
}
```

#### シームレスで不変

インデックス署名を読み取り専用としてマークすることもできます：

```ts
/**
 * Declaration
 */
interface Foo {
    readonly[x: number]: number;
}

/**
 * Usage
 */
let foo: Foo = { 0: 123, 2: 345 };
console.log(foo[0]);   // Okay (reading)
foo[0] = 456;          // Error (mutating): Readonly
```

ネイティブJavaScript配列を*不変*形式で使用したい場合は、これは素晴らしいことです。実際、TypeScriptには `ReadonlyArray <T>`インタフェースが付属しています。

```ts
let foo: ReadonlyArray<number> = [1, 2, 3];
console.log(foo[0]);   // Okay
foo.push(4);           // Error: `push` does not exist on ReadonlyArray as it mutates the array
foo = foo.concat([4]); // Okay: create a copy
```

#### 自動推論
場合によっては、コンパイラは、特定の項目を読み込み専用に自動的に推論することができます。クラス内でgetterしか持たずsetterも持たないプロパティを持つ場合は、たとえば読み取り専用とみなされます。

```ts
class Person {
    firstName: string = "John";
    lastName: string = "Doe";
    get fullName() {
        return this.firstName + this.lastName;
    }
}

const person = new Person();
console.log(person.fullName); // John Doe
person.fullName = "Dear Reader"; // Error! fullName is readonly
```

### との相違点
`const`
1. 可変参照用です
1. 変数を他のものに再割り当てすることはできません。

`readonly`は
1. プロパティの場合
1. エイリアシングのためにプロパティを変更することができます。

説明するサンプル1：

```ts
const foo = 123; // variable reference
var bar: {
    readonly bar: number; // for property
}
```

2：

```ts
let foo: {
    readonly bar: number;
} = {
        bar: 123
    };

function iMutateFoo(foo: { bar: number }) {
    foo.bar = 456;
}

iMutateFoo(foo); // The foo argument is aliased by the foo parameter
console.log(foo.bar); // 456!
```

基本的に `readonly`は、プロパティ*を私が変更することはできないことを保証しますが、その保証を持たない(型互換性のために許されている)人にそれを渡すと、変更できます。もちろん、 `iMutateFoo`が`foo.bar`に変更を加えていないと言った場合、コンパイラは以下のように正しくフラグを立てます：

```ts
interface Foo {
    readonly bar: number;
}
let foo: Foo = {
    bar: 123
};

function iTakeFoo(foo: Foo) {
    foo.bar = 456; // Error! bar is readonly
}

iTakeFoo(foo); // The foo argument is aliased by the foo parameter
```

[](https://github.com/Microsoft/TypeScript/pull/6532)
