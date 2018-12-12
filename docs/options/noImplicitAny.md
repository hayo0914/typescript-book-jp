# noImplicitAny

推測できないものや推測できないものがあり、予期しないエラーが発生する可能性があります。良い例は関数の引数です。アノテーションを付けないと、何が有効であるべきか、または無効であるべきかが明確ではありません。

```ts
function log(someArg) {
  sendDataToServer(someArg);
}

// What arg is valid and what isn't?
log(123);
log('hello world');
```

だから、もしあなたが何かの関数の引数にアノテーションをつけなければ、TypeScriptは`any`とみなして動きます。これにより、JavaScriptデベロッパーが期待しているような型チェックがオフになります。しかし、これは高い安全性を守ることを望む人々の足をすくうかもしれません。したがって、スイッチをオンにすると、型推論できない場合にフラグを立てるオプション、noImplicitAnyがあります。

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

あなたが本当にゼロの安全性を望むなら*明示的に`any`とマークすることができます：

```ts
function log(someArg: any) {
  sendDataToServer(someArg);
}
```
