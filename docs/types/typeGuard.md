## Type Guard (Type Guards)
Type Guardを使用すると、条件ブロック内のオブジェクトの型を制限することができます。

### typeof

TypeScriptはJavaScriptの`instanceof`と`typeof`演算子の使用を認識しています。条件付きブロックでこれらを使用すると、TypeScriptはその条件ブロック内で異なる変数の型を理解します。ここでは、TypeScriptが特定の関数が`string`に存在せず、おそらくユーザのタイプミスであったことを指摘する簡単な例を示します：

```ts
function doSomething(x: number | string) {
    if (typeof x === 'string') { // Within the block TypeScript knows that `x` must be a string
        console.log(x.subtr(1)); // Error, 'subtr' does not exist on `string`
        console.log(x.substr(1)); // OK
    }
    x.substr(1); // Error: There is no guarantee that `x` is a `string`
}
```

### instanceof

次はクラスと `instanceof`の例です：

```ts
class Foo {
    foo = 123;
    common = '123';
}

class Bar {
    bar = 123;
    common = '123';
}

function doStuff(arg: Foo | Bar) {
    if (arg instanceof Foo) {
        console.log(arg.foo); // OK
        console.log(arg.bar); // Error!
    }
    if (arg instanceof Bar) {
        console.log(arg.foo); // Error!
        console.log(arg.bar); // OK
    }

    console.log(arg.common); // OK
    console.log(arg.foo); // Error!
    console.log(arg.bar); // Error!
}

doStuff(new Foo());
doStuff(new Bar());
```

TypeScriptは `else`を理解しています。そうすれば`if`の中は、特定の型であり、`else`の中はその型でないことが分かります。次に例を示します。

```ts
class Foo {
    foo = 123;
}

class Bar {
    bar = 123;
}

function doStuff(arg: Foo | Bar) {
    if (arg instanceof Foo) {
        console.log(arg.foo); // OK
        console.log(arg.bar); // Error!
    }
    else {  // MUST BE Bar!
        console.log(arg.foo); // Error!
        console.log(arg.bar); // OK
    }
}

doStuff(new Foo());
doStuff(new Bar());
```

### in

`in`演算子は、オブジェクト上のプロパティの存在を安全にチェックし、Type Guardとして使用することができます。例えば。

```ts
interface A {
  x: number;
}
interface B {
  y: string;
}

function doStuff(q: A | B) {
  if ('x' in q) {
    // q: A
  }
  else {
    // q: B
  }
}
```

### リテラル型のType Guard

異なるリテラル値を区別するには、`===` / `==` / `!==` / `!=` が利用できます。

```ts
type TriState = 'yes' | 'no' | 'unknown';

function logOutState(state:TriState) {
  if (state == 'yes') {
    console.log('User selected yes');
  } else if (state == 'no') {
    console.log('User selected no');
  } else {
    console.log('User has not made a selection yet');
  }
}
```

ユニオン型の中にリテラル型がある場合にも同じ方法が使えます。次のように共通するプロパティの値をチェックすることで、異なるユニオン型を区別できます。

```ts
type Foo = {
  kind: 'foo', // Literal type
  foo: number
}
type Bar = {
  kind: 'bar', // Literal type 
  bar: number
}

function doStuff(arg: Foo | Bar) {
    if (arg.kind === 'foo') {
        console.log(arg.foo); // OK
        console.log(arg.bar); // Error!
    }
    else {  // MUST BE Bar!
        console.log(arg.foo); // Error!
        console.log(arg.bar); // OK
    }
}
```

### `strictNullChecks`を使用したnullとundefinedのチェック

TypeScriptは十分賢いので、次のように`== null` / `!= null`チェックをすることで`null`と`undefined`の両方を排除できます。

```ts
function foo(a?: number | null) {
  if (a == null) return;

  // a is number now.
}
```

### ユーザー定義のType Guard
JavaScriptには非常に豊富な実行時の解析サポートが組み込まれていません。単純なJavaScriptオブジェクトだけを使用している場合(構造型を使用する場合)、 `instanceof`または`typeof`にアクセスすることさえできません。これらの場合、Type Guard関数をユーザが定義することができます。これは、`someArgumentName is SomeType`を返す関数です。次に例を示します。

```ts
/**
 * Just some interfaces
 */
interface Foo {
    foo: number;
    common: string;
}

interface Bar {
    bar: number;
    common: string;
}

/**
 * User Defined Type Guard!
 */
function isFoo(arg: any): arg is Foo {
    return arg.foo !== undefined;
}

/**
 * Sample usage of the User Defined Type Guard
 */
function doStuff(arg: Foo | Bar) {
    if (isFoo(arg)) {
        console.log(arg.foo); // OK
        console.log(arg.bar); // Error!
    }
    else {
        console.log(arg.foo); // Error!
        console.log(arg.bar); // OK
    }
}

doStuff({ foo: 123, common: '123' });
doStuff({ bar: 123, common: '123' });
```

### Type Guardsとコールバック

TypeScript doesn't assume type guards remain active in callbacks as making this assumption is dangerous. e.g.

```ts
// Example Setup
declare var foo:{bar?: {baz: string}};
function immediate(callback: ()=>void) {
  callback();
}


// Type Guard
if (foo.bar) {
  console.log(foo.bar.baz); // Okay
  functionDoingSomeStuff(() => {
    console.log(foo.bar.baz); // TS error: Object is possibly 'undefined'"
  });
}
```

The fix is as easy as storing the inferred safe value in a local variable, automatically ensuring it doesn't get changed externally, and TypeScript can easily understand that:

```js
// Type Guard
if (foo.bar) {
  console.log(foo.bar.baz); // Okay
  const bar = foo.bar;
  functionDoingSomeStuff(() => {
    console.log(bar.baz); // Okay
  });
}
```
