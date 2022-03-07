# JavaScript

これまで存在した数多くの競合言語は \(きっとこれからもそうなのでしょうが\)、 _ある構文_ を _JavaScript_ へとコンパイルするものでした。TypeScriptは、 _JavaScriptがTypeScriptである_ という点において、他とは一線を画しています。これを表す図がこちらです：

![JavaScript&#x306F;TypeScript&#x3067;&#x3059;](https://raw.githubusercontent.com/basarat/typescript-book/master/images/venn.png)

しかし、これが意味していることは、 _JavaScriptを学ぶ必要がある_ ということです \(良いニュースは、JavaScript**だけ**を学べば良いということです\)。TypeScriptは、単に、JavaScriptのコードを良いドキュメントにする方法を標準化したものに過ぎません。

* 単に新しい構文が提供されたというだけでは、バグの発見に寄与することはありません。しかし、より意図が明確で、バグの少ないコードを書く助けには、なるかもしれません \(例：CoffeeScript\)。
* 新しく作られたプログラミング言語では、慣れ親しんだ開発環境やコミュニティから遠ざけられてしまいます。しかし、もしそれが既に慣れ親しんだものに近い雰囲気があれば、より馴染みやすくなるかもしれません\(例：Dartは、Java や C\# の開発者にとって馴染みやすいものです\)。

TypeScriptは単にドキュメント付きのJavaScriptです。

> JSNextは解釈の自由度が高く、JSの次のバージョンとして提案されたとしても、その全てが実際にブラウザでサポートされるとは限りません。TypeScriptは、提案が[ステージ3](https://tc39.es/process-document/)に達しさえすれば、それをサポートするようになります。

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

