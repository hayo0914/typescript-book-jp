# 解釈エラー(Interpreting Errors)
TypeScriptは、*Developer Help*指向のプログラミング言語であることを非常に重視しているので、何かがうまく動いてない時のエラーメッセージは、高レベルなサポートになるよう努力しています。これは、コンパイラは助けにならないと考えるユーザーにとっては、わずかな情報過多につながる可能性があります。 

1つの例をIDEで見て、エラーメッセージを読むプロセスを1つ1つ見ていきましょう。

```ts
type SomethingComplex = {
  foo: number,
  bar: string
}
function takeSomethingComplex(arg: SomethingComplex) {
}
function getBar(): string {
  return 'some bar';
}

//////////////////////////////////
// Example error production
//////////////////////////////////
const fail = {
  foo: 123,
  bar: getBar
};

takeSomethingComplex(fail); // TS ERROR HAPPENS HERE 
```

この例は関数呼び出しに失敗している一般的なプログラミングエラーです(`bar: getBar`は`bar: getBar()`であるべきです)。この不手際については、幸運なことに、TypeScriptによって型の要件が一致しないことが即座にキャッチされます。

## エラーのカテゴリ(Error Categories)
TypeScriptのエラーメッセージには2種類あります(SuccinctとDetailed)。

### 簡潔(Succinct)
succinctエラーメッセージは、エラー番号とメッセージについての、通常のコンパイラの説明を提供することを意図したものです。例えば、succinctメッセージは次のようなものです。

```
TS2345: Argument of type '{ foo: number; bar: () => string; }' is not assignable to parameter of type 'SomethingComplex'.
```
これはかなり自明です。しかし、なぜこのエラーが起きたのかを深く掘り下げたものではありません。それは、*detailed*エラーメッセージが意図するものです。

### 詳細(Detailed)
この例のdetailedバージョンは以下のようなものです:

```
[ts]
Argument of type '{ foo: number; bar: () => string; }' is not assignable to parameter of type 'SomethingComplex'.
  Types of property 'bar' are incompatible.
    Type '() => string' is not assignable to type 'string'.
```
detailedメッセージの目的は、ユーザーに、なぜ何かのエラー（この例では型の非互換性）が起きたかをユーザーにガイドすることです。最初の行はsuccinctと同じですが、その後ろにチェーンが繋がっています。あなたは、これらのチェーンを、行と行の間の「WHY?」に対する答えの繋がりとして読むべきです。

```
ERROR: Argument of type '{ foo: number; bar: () => string; }' is not assignable to parameter of type 'SomethingComplex'.

WHY? 
CAUSE ERROR: Types of property 'bar' are incompatible.

WHY? 
CAUSE ERROR: Type '() => string' is not assignable to type 'string'.
```

なので根本原因は、
* `bar`プロパティに
* `string`型が期待されているにも関わらず、関数`() => string`があるため

これはデベロッパーにとって`bar`プロパティのバグの修正の助けになるものです(彼らは関数の`()`を呼び出すのを忘れました)。

## IDEのツールチップでの見え方(How it shows up in an IDE Tooltip)

IDEは通常、`detailed`メッセージ、`succinct`バージョンの順にツールチップを表示します。下記は例です:

![IDE error message example](https://raw.githubusercontent.com/basarat/typescript-book/master/images/errors/interpreting-errors/ide.png)

* あなたは通常は、ただ`detailed`バージョンを見て、`WHY?`のチェーンを頭の中に作ります
* あなたは似たようなエラーを検索するために`succinct`バージョンを使います(`TSXXXX`エラーコードか、エラーメッセージの一部を使います)
