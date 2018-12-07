# あなたの書いたJavaScriptはTypeScriptである

JavaScriptにコンパイルされるプログラミング言語に関しては、たくさんの競合がありました(そして今後も)。 TypeScriptは、*JavaScriptがTypeScriptである*点において、それらと一線を画しています。これを表す図：

![JavaScriptはTypeScriptです](https://raw.githubusercontent.com/basarat/typescript-book/master/images/venn.png)

しかし、これは、開発者がJavaScriptを学ぶ必要があることを意味しています(良いニュースは、JavaScriptだけ学べば良いということです)。TypeScriptは、単に、JavaScriptコードを良いドキュメントにする方法を標準化したものに過ぎません。

* 新しいプログラミング構文はバグ修正の助けにはなりません(CoffeeScriptを見てください)
* 新しいプログラミング言語は、理論に偏り、開発者を実行環境やコミュニティから遠ざけます(Dartを見てください)

TypeScriptは単にドキュメント付きのJavaScriptです。

## JavaScriptを改善する

TypeScriptは、JavaScriptのイカれた仕様から開発者を守ります(こんなのを覚えておく必要はありません)：

```ts
[] + []; // JavaScript will give you "" (which makes little sense), TypeScript will error

//
// other things that are nonsensical in JavaScript
// - don't give a runtime error (making debugging hard)
// - but TypeScript will give a compile time error (making debugging unnecessary)
//
{} + []; // JS : 0, TS Error
[] + {}; // JS : "[object Object]", TS Error
{} + {}; // JS : NaN or [object Object][object Object] depending upon browser, TS Error
"hello" - 1; // JS : NaN, TS Error

function add(a,b) {
  return
    a + b; // JS : undefined, TS Error 'unreachable code detected'
}
```

本質的にTypeScriptはJavaScriptのリンター(linter)です。*型情報*を持たない他のリンターよりも優れているだけです。

## 開発者は、まだJavaScriptを学ぶ必要がある

TypeScriptは、「実際にはJavaScriptを書くものである」という点から非常に実用的なプログラミング言語だと言われていますが、それゆえ足をすくわれないように、JavaScriptに関して知っておくべきことがあります。次にそれらについて説明しましょう。

> 注意：TypeScriptはJavaScriptのスーパーセット(上位互換)であり、JavaScriptにコンパイラやIDEで使う型情報が付いただけのものです
