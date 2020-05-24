# noImplicitAny

型を推測できない、あるいは型を推測した結果が予期せぬエラーとなるかもしれない場合があります。良い例は関数の引数です。アノテーションを付けなければ、どの型が有効であるべきか、そうでないかが不明確になります。

```typescript
function log(someArg) {
  sendDataToServer(someArg);
}

// What arg is valid and what isn't?
log(123);
log('hello world');
```

だから、もしあなたが関数の引数にアノテーションを付けなければ、TypeScriptは`any`とみなして動きます。これにより、JavaScriptデベロッパーが期待しているような型チェックがオフになります。しかし、これは高い安全性を守ることを望む人々の足をすくうかもしれません。したがって、スイッチをオンにすると、型推論できない場合にフラグを立てるオプション、`noImplicitAny`があります。

```typescript
function log(someArg) { // Error : someArg has an implicit `any` type
  sendDataToServer(someArg);
}
```

もちろん、アノテーションを付けて前進できます:

```typescript
function log(someArg: number) {
  sendDataToServer(someArg);
}
```

あなたが本当にゼロの安全性を望むなら_明示的_に`any`とマークすることができます:

```typescript
function log(someArg: any) {
  sendDataToServer(someArg);
}
```

