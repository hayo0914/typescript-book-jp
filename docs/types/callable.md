## 呼び出し可能
次のように、タイプまたはインタフェースの一部としてコール可能オブジェクトに注釈を付けることができます

```ts
interface ReturnString {
  (): string
}
```
そのようなインターフェースのインスタンスは、例えば文字列を返す関数である。

```ts
declare const foo: ReturnString;
const bar = foo(); // bar is inferred as a string
```

### 明らかな例
もちろん、このような*呼び出し可能な注釈は、必要に応じて引数/オプション引数/残り引数を指定することもできます。例えばここに複雑な例があります：

```ts
interface Complex {
  (foo: string, bar?: number, ...others: boolean[]): number;
}
```

インタフェースは、複数の呼び出し可能な注釈を提供して、関数のオーバーロードを指定することができます。例えば：

```ts
interface Overloaded {
    (foo: string): string
    (foo: number): number
}

// example implementation
function stringOrNumber(foo: number): number;
function stringOrNumber(foo: string): string;
function stringOrNumber(foo: any): any {
    if (typeof foo === 'number') {
        return foo * foo;
    } else if (typeof foo === 'string') {
        return `hello ${foo}`;
    }
}

const overloaded: Overloaded = stringOrNumber;

// example usage
const str = overloaded(''); // type of `str` is inferred as `string`
const num = overloaded(123); // type of `num` is inferred as `number`
```

もちろん、* any *インターフェースの本体のように、呼び出し可能なインターフェースの本体を変数の型名として使用することができます。例えば：

```ts
const overloaded: {
  (foo: string): string
  (foo: number): number
} = (foo: any) => foo;
```

### 矢印の構文
呼び出し可能なシグネチャを簡単に指定できるように、TypeScriptでは単純な矢印タイプの注釈も使用できます。例えば、 `number`をとり、`string`を返す関数は次のように注釈することができます：

```ts
const simple: (foo: number) => string
    = (foo) => foo.toString();
```

> 矢印の構文の制限のみ：過負荷を指定することはできません。オーバーロードの場合、フルボディの `{(someArgs)：someReturn}`構文を使用する必要があります。

### Newable

Newableは、接頭辞 `new`を持つ特別な型の* callable *型の注釈です。これは単に* newを使って*を呼び出す必要があることを意味します。

```ts
interface CallMeWithNewToGetString {
  new(): string
}
// Usage
declare const Foo: CallMeWithNewToGetString;
const bar = new Foo(); // bar is inferred to be of type string
```
