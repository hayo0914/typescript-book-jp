# あなたのJavaScriptはTypeScriptです

いくつかのシンタックス*〜* JavaScript *コンパイラには多くのライバルがいました（そして今後もそうです）。 TypeScriptは、あなたのJavaScriptがTypeScript *である点でそれらとは異なります。ここに図があります：

！[JavaScriptはTypeScriptです]（https://raw.githubusercontent.com/basarat/typescript-book/master/images/venn.png）

しかし、* JavaScript *を学ぶ必要があることを意味します（良いニュースはJavaScript *を学ぶ必要があるだけです）。 TypeScriptは、JavaScriptの優れたドキュメンテーション*をすべて標準化しています。

* あなたに新しい構文を与えるだけでは、バグを修正するのに役立つわけではありません（CoffeeScriptを見て）。
* 新しい言語を作成すると、あなたのランタイム、コミュニティから離れすぎていることが抽象化されます（ダーツを見て）。

TypeScriptは単なるドキュメントのJavaScriptです。

## JavaScriptを改善する

TypeScriptは、これまで働いたことのないJavaScriptの部分からあなたを保護しようとします（このようなことは覚えておく必要はありません）：

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

本質的には、TypeScriptはJavaScriptをlintingしています。 *タイプ情報*を持たない他のリンターよりも良い仕事をしているだけです。

## あなたはまだJavaScriptを学ぶ必要があります

これは、TypeScriptがJavaScript *を書いているという事実に非常に実用的だと言っているので、JavaScriptについては、まだ注意を払わないようにする必要があることがいくつかあります。次にそれらについて説明しましょう。

> 注意：TypeScriptはJavaScriptのスーパーセットです。コンパイラ/ IDEで実際に使用可能なドキュメントだけです。
