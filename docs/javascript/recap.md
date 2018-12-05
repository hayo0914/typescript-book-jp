# あなたのJavaScriptはTypeScriptです

JavaScriptコンパイラに対する、いくつかの構文には多くの競合がいました（そして今後もそうです）。 TypeScriptは、*あなたのJavaScriptがTypeScriptである*点でそれらとは異なります。ここに図があります：

！[JavaScriptはTypeScriptです]（https://raw.githubusercontent.com/basarat/typescript-book/master/images/venn.png）

しかし、これはJavaScriptを学ぶ必要があることを意味します（良いニュースはJavaScriptだけを学ぶ必要があるだけです）。 TypeScriptは、JavaScriptの優れたドキュメンテーションを提供する全ての方法を標準化しているだけです。

* 新しい構文はバグを修正するのに役立つわけではありません（CoffeeScriptを見てください）
* 新しい言語を作成すると、ランタイム、コミュニティを抽象化しすぎます（Dartを見てください）

TypeScriptは単なるドキュメント付きのJavaScriptです。

## JavaScriptを改善する

TypeScriptは、JavaScriptの決してまともに動かない部分からあなたを保護しようとします（このようなことは覚えておく必要はありません）：

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

本質的には、TypeScriptはJavaScriptを校正(linting)しています。 *型情報*を持たない他のlinterよりも良い仕事をしているだけです。

## あなたはまだJavaScriptを学ぶ必要があります

TypeScriptは、ガードしていない部分を攻撃されないように、いくつかのJavaScriptに関して学ぶ必要があること、あなたがJavaScriptを書くという事実から非常に実用的だと言われています。次にそれらについて説明しましょう。

> 注意：TypeScriptはJavaScriptのスーパーセットであり、JavaScriptにコンパイラ/IDEで使われるドキュメント（型情報）が付いただけのものです
