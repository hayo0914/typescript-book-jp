# noImplicitAny

推測できないものや推測できないものがあり、予期しないエラーが発生する可能性があります。良い例は関数の引数です。注釈を付けないと、何が有効であるべきか、または無効であるべきかが明確ではない。

```ts
function log(someArg) {
  sendDataToServer(someArg);
}

// What arg is valid and what isn't?
log(123);
log('hello world');
```

だから、もしあなたがいくつかの関数の引数に注釈をつけなければ、TypeScriptは `any`とみなして動きます。これにより、JavaScriptデベロッパーが期待しているようなケースのチェックがオフになります。しかし、これは高い安全性を守ることを望む人々を捉えることができます。したがって、スイッチをオンにすると、タイプが推論できない場合にフラグを立てるオプション、noImplicitAnyがあります。

```ts
function log(someArg) { // Error : someArg has an implicit `any` type
  sendDataToServer(someArg);
}
```

もちろん、次に注釈を付けることができます：

```ts
function log(someArg: number) {
  sendDataToServer(someArg);
}
```

あなたが本当にゼロの安全性を望むなら*明示的に `any`とマークすることができます：

```ts
function log(someArg: any) {
  sendDataToServer(someArg);
}
```
