# あなたの書いたJavaScriptはTypeScriptである

JavaScriptにコンパイルされるプログラミング言語に関しては、たくさんの競合がありました(そして今後も)。 TypeScriptは、*JavaScriptがTypeScriptである*点において、それらと一線を画しています。これを表す図がこちらです：

![JavaScriptはTypeScriptです](https://raw.githubusercontent.com/basarat/typescript-book/master/images/venn.png)

しかしながら、これは、あなたがJavaScriptを学ぶ必要があることを意味しています(良いニュースは、JavaScript**だけ**学べば良いということです)。TypeScriptは、単に、JavaScriptコードを良いドキュメントにする方法を標準化したものに過ぎません。

* 単なる新しいプログラミング構文はバグを見つける助けにはなりません - でも、よりクリーンなコードや、少ないバグの助けにはなるかもしれません(例：CoffeeScript)
* 新しいプログラミング言語の抽象化は、開発者をランタイムやコミュニティから遠ざけます - でも、もしあなたが既に親しんでいる概念であれば、学習が容易になるかもしれません(例：Dart は Java/C# に近い)

TypeScriptは単にドキュメント付きのJavaScriptです。

## JavaScriptを改善する

TypeScriptは、JavaScriptの全く意味を成さない仕様から開発者を守ります(こんなことを覚えておく必要はありません)：

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

TypeScriptは、「実際はJavaScriptを書く」という点から非常に実用的なプログラミング言語だと言われています。しかし、だからこそJavaScriptに関して知っておくべきことがあります。次にそれらについて説明しましょう。

> 注意：TypeScriptはJavaScriptのスーパーセット(上位互換)であり、JavaScriptにコンパイラやIDEで使う型情報が付いただけのものです
