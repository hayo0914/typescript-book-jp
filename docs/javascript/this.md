## this

関数の中での`this`へのアクセスは、関数がどのように呼び出されたかによって制御されます。これは一般に「呼び出しコンテキスト(calling context)」と呼ばれます。

例:

```ts
function foo() {
  console.log(this);
}

foo(); // logs out the global e.g. `window` in browsers
let bar = {
  foo
}
bar.foo(); // Logs out `bar` as `foo` was called on `bar`
```

そのため、`this`の使い方に気をつけてください。呼び出しコンテキストからクラス内の`this`を切り離したい場合は、アロー関数を使います。[アロー関数については後述します](../arrow-functions.md)。
