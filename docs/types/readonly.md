## readonly
TypeScriptの型システムでは、インターフェイス上の個々のプロパティを`readonly`としてマークすることができます。これにより、関数的に作業することができます(予期しない変更は良くありません)。

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

もちろん `interface`と`type`の定義に`readonly`を使うこともできます：

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

クラスプロパティを`readonly`として宣言することもできます。次のように、宣言箇所またはコンストラクタで初期化することができます。

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
`Readonly`型は`T`型をとり、そのすべてのプロパティを`readonly`とマークします。以下にデモを示します：

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
不変性(Immutabillity)を愛するライブラリの1つがReactJSです。たとえば、あなたの`Props`と`State`には不変(immutable)であるとマークすることができます：

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

しかし、Reactの型定義として、これらを`readonly`としてマークする必要はありません。Reactは既に内部でそれを行っています。

```ts
export class Something extends React.Component<{ foo: number }, { baz: number }> {
  // You can rest assured no one is going to do
  someMethod() {
    this.props.foo = 123; // ERROR: (props are immutable)
    this.state.baz = 456; // ERROR: (one should use this.setState)  
  }
}
```

#### シームレスな不変性(Seamless Immutable)

インデックスのシグネチャをreadonlyとしてマークすることもできます：

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

ネイティブのJavaScript配列を不変的(immutable)な方法で使用したいと思うことは、素晴らしいことです。実際、ちょうどそのためにTypeScriptには`ReadonlyArray<T>`インタフェースが付属しています。

```ts
let foo: ReadonlyArray<number> = [1, 2, 3];
console.log(foo[0]);   // Okay
foo.push(4);           // Error: `push` does not exist on ReadonlyArray as it mutates the array
foo = foo.concat([4]); // Okay: create a copy
```

#### 自動推論
場合によっては、コンパイラは、特定の項目を読み込み専用に自動的に推論することができます。例えば、クラス内でgetterしか持たずsetterを持たないプロパティは、読み取り専用とみなされます。

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

### `const`との相違点
`const`
1. 変数参照に利用するものである
1. 他の値を再度割り当てることはできない

`readonly`
1. プロパティに利用するものである
1. エイリアシングによってプロパティが変更されることがありえる

説明のためのサンプル1：

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

基本的に `readonly`は、プロパティを私が変更することはできないことを保証しますが、(型互換性のための理由で)その保証を持たない人にそれを渡すと、変更できてしまいます。もちろん、`iMutateFoo`が「`foo.bar`に変更を加えない」と言っている場合、コンパイラは以下のように正しくエラーフラグを立てます：

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
