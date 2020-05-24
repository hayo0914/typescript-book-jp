# Function parameters

あまりにも多くのパラメータや同じ型のパラメータを取る関数がある場合は、代わりにオブジェクトを取るように関数を変更することを検討してください。

以下の関数を考えてみましょう：

```typescript
function foo(flagA: boolean, flagB: boolean) {
  // your awesome function body 
}
```

このような関数定義では、それを間違って呼び出すのはかなり簡単です。`foo(flagB、flagA)`を呼び出すと、コンパイラの助けを借りることができません。

代わりに、オブジェクトを取得する関数に変換します。

```typescript
function foo(config: {flagA: boolean, flagB: boolean}) {
  const {flagA, flagB} = config;
  // your awesome function body 
}
```

関数呼び出しは`foo({flagA、flagB})`のようになりますので、間違いの発見やコードレビューを簡単にすることができます。

> 注意：あなたの機能が十分にシンプルで、効果があまり期待できないと感じる場合は、このアドバイスを無視してください🌹

