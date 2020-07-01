# this

関数の中での`this`へのアクセスは、関数がどのように呼び出されたかによって制御されます。これは一般に「呼び出しコンテキスト」と呼ばれます。

例:

```typescript
function foo() {
  console.log(this);
}

foo(); // グローバル値をログに出力します（例： ブラウザにおける `window`）
let bar = {
  foo
}
bar.foo(); // `bar`がログに出力されます。なぜなら、`bar`に対して`foo`が呼び出されるからです
```

なので、`this`の使い方に気をつけてください。呼び出しコンテキストからクラス内の`this`を切り離したい場合は、アロー関数を使います。[アロー関数については後述します](../future-javascript/arrow-functions.md)。

