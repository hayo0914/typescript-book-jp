# noImplicitAny

推測ができない、もしくは推測する事により予期せぬエラーを発生しかねないものがあります。良い例は関数の引数です。アノテーションを付けないと、何が有効で、何が有効でないのかが不明確です。

```ts
function log(someArg) {
  sendDataToServer(someArg);
}

// What arg is valid and what isn't?
log(123);
log('hello world');
```

だから、もしあなたが関数の引数にアノテーションを付けなければ、TypeScriptは`any`とみなして動きます。これにより、JavaScriptデベロッパーが期待しているような型チェックがオフになります。しかし、これは高い安全性を守ることを望む人々の足をすくうかもしれません。したがって、スイッチをオンにすると、型推論できない場合にフラグを立てるオプション、`noImplicitAny`があります。

```ts
function log(someArg) { // Error : someArg has an implicit `any` type
  sendDataToServer(someArg);
}
```

もちろん、アノテーションを付けて前進できます:

```ts
function log(someArg: number) {
  sendDataToServer(someArg);
}
```

あなたが本当にゼロの安全性を望むなら*明示的*に`any`とマークすることができます:

```ts
function log(someArg: any) {
  sendDataToServer(someArg);
}
```
