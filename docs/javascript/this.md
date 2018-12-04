## この

関数内の `this`キーワードへのアクセスは、実際に関数が実際に呼び出される方法によって実際に制御されます。これは一般に「呼び出しコンテキスト」と呼ばれます。

次に例を示します。

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

だから、あなたの使い方に気をつけてください。呼び出しコンテキストからクラス内の `this`を切断したい場合は、矢印関数を使います。[more later] [arrow]。

[arrow]：../ arrow-functions.md
