# JavaScript

JavaScriptにコンパイルされるプログラミング言語に関しては、他にも、たくさんの競合がありました\(そして今後もあるでしょう\)。 しかし、TypeScriptは、_JavaScriptがTypeScriptである、という_点において、他とは一線を画しています。これを表す図がこちらです：

![JavaScript&#x306F;TypeScript&#x3067;&#x3059;](https://raw.githubusercontent.com/basarat/typescript-book/master/images/venn.png)

しかし、これが意味していることは、あなたは、JavaScriptを学ぶ必要がある、ということです\(良いニュースは、JavaScript**だけ**を学べば良いということです\)。TypeScriptは、単に、JavaScriptのコードを良いドキュメントにする方法を標準化したものに過ぎません。

* 単なる新しいプログラミングの構文はバグを見つける助けにはなりません - しかし、よりクリーンなコードを書くことや、バグを減らす助けにはなるかもしれません\(例：CoffeeScript\)
* 新しいプログラミング言語の抽象化は、開発者を実行環境の詳細やコミュニティから遠ざけます - しかし、もしあなたが既に親しんでいる概念であれば、容易に学習できるかもしれません\(例：Dart は Java/C\# に近い言語です\)

TypeScriptは単にドキュメント付きのJavaScriptです。

## TypeScriptは、JavaScriptを改善する

TypeScriptは、JavaScriptの全く意味が通らない変な仕様から開発者を守ります\(こんなことを覚えておく必要はありません\)：

```typescript
[] + []; // JavaScript は "" を返す (意味不明な仕様)。 TypeScript はエラーを表示する

//
// その他の意味不明なJavaScriptの仕様
// - 実行時エラーが発生しない (そのため、デバッグが難しい）
// - しかし、TypeScriptはコンパイル時にエラーを表示する (デバッグ自体を不要にする)
//
{} + []; // JS : 0, TSはエラー
[] + {}; // JS : "[object Object]", TSはエラー
{} + {}; // JS : ブラウザによって、NaN または [object Object][object Object], TSはエラー
"こんにちは" - 1; // JS : NaN, TSはエラー

function add(a,b) {
  return
    a + b; // JS : undefined, TSはエラー '到達不可能なコードが検知されました'
}
```

本質的には、TypeScriptはJavaScriptのリンター\(コードの静的解析ツール\)です。_型情報_を持たない他のJavaScriptのリンターよりも優れているだけです。

## それでも開発者は、JavaScriptを学ぶ必要がある

TypeScriptは、「実際にはJavaScriptを書く」という点から非常に実用的なプログラミング言語であると言われています。だからこそJavaScriptに関して知っておかなければならないことがあります。次にそれらについて説明しましょう。

> 注意：TypeScriptはJavaScriptのスーパーセット\(上位互換\)であり、JavaScriptにコンパイラやIDEで使う型情報が付いただけのものです

