# 呼び出し可能オブジェクト

次のように、型またはインターフェースの一部として呼び出し可能オブジェクトにアノテーションを付けることができます

```typescript
interface ReturnString {
  (): string
}
```

そのようなインターフェースのインスタンスは、例えば文字列を返す関数です。

```typescript
declare const foo: ReturnString;
const bar = foo(); // bar is inferred as a string
```

## 明白な例

もちろん、このような呼び出し可能なアノテーションは、必要に応じて引数/オプション引数/可変長引数を指定することもできます。例えばここに複雑な例があります：

```typescript
interface Complex {
  (foo: string, bar?: number, ...others: boolean[]): number;
}
```

インターフェースは、複数の呼び出し可能なアノテーションを提供して、関数のオーバーロードを指定することができます。例えば：

```typescript
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

もちろん、インターフェースの本体のように、呼び出し可能オブジェクトのインターフェースの本体を変数の型名として使用することができます。例えば：

```typescript
const overloaded: {
  (foo: string): string
  (foo: number): number
} = (foo: any) => foo;
```

## アロー構文

呼び出し可能オブジェクトのシグネチャを簡単に指定できるように、TypeScriptでは単純なアロー型アノテーションも使用できます。例えば、`number`をとり、`string`を返す関数は次のようにアノテーションすることができます：

```typescript
const simple: (foo: number) => string
    = (foo) => foo.toString();
```

> たった1つのアロー構文の制限： オーバーロードを指定することはできません。オーバーロードの場合、フルの`{(someArgs)：someReturn}`構文を使用する必要があります。

## ニューアブル\(Newable\)

ニューアブル\(Newable\)は、接頭辞`new`を持つ特殊なコーラブル型アノテーションです。これは単にnewを使って呼び出す必要があることを意味します。

```typescript
interface CallMeWithNewToGetString {
  new(): string
}
// Usage
declare const Foo: CallMeWithNewToGetString;
const bar = new Foo(); // bar is inferred to be of type string
```

