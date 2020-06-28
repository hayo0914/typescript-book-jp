# エラーの理解

TypeScriptは、開発者が気持ち良く開発できるようにすることを非常に重視しているプログラミング言語です。なので、何かがうまく動いてない時のエラーメッセージは、なるべく分かりやすくなるように努力しています。

１つの例をVSCodeで見て、エラーメッセージを読むプロセスをステップバイステップで見ていきましょう。

```typescript
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
// エラーの発生例
//////////////////////////////////
const fail = {
  foo: 123,
  bar: getBar
};

takeSomethingComplex(fail); // ここでTypeScriptのコンパイルエラーが表示されます
```

この例は関数の呼び出しに失敗している一般的なプログラミングの誤りです\(`bar: getBar`は`bar: getBar()`であるべきです\)。このような誤りは、ありがたいことにTypeScriptによって即座にキャッチされます。なぜなら、型が一致していないからです。

## エラーの種類

TypeScriptのエラーメッセージは２種類あります（簡潔なエラーメッセージと、詳細なエラーメッセージ）。

### 簡潔なエラーメッセージ

簡潔なエラーメッセージの目的は、エラー番号とエラーメッセージに関する一般的なコンパイラの説明を提供することです。例えば、次のようなものです。

```text
TS2345: Argument of type '{ foo: number; bar: () => string; }' is not assignable to parameter of type 'SomethingComplex'.
```

このエラーメッセージは、読めば意味は理解できるものです。しかし、なぜこのエラーが起きたのか、ということを深く掘り下げたものではありません。そのためには、詳細なエラーメッセージを見る必要があります。

### 詳細なエラーメッセージ

この例における詳細なエラーメッセージは以下のようなものです:

```text
[ts]
Argument of type '{ foo: number; bar: () => string; }' is not assignable to parameter of type 'SomethingComplex'.
  Types of property 'bar' are incompatible.
    Type '() => string' is not assignable to type 'string'.
```

詳細なエラーメッセージの目的は、開発者に対して、なぜこのエラー（この例では型の不一致）が起きたかをわかるようにすることです。最初の行は簡潔なエラーメッセージと同じですが、その下の行にチェーンが繋がっています。これらのチェーンは、行と行の間の「なぜ？」に対する答えを提供するものです。

```text
ERROR: Argument of type '{ foo: number; bar: () => string; }' is not assignable to parameter of type 'SomethingComplex'.

なぜ? 
CAUSE ERROR: Types of property 'bar' are incompatible.

なぜ? 
CAUSE ERROR: Type '() => string' is not assignable to type 'string'.
```

なので根本原因は、

* `bar`プロパティに
* `string`型が期待されているにも関わらず、関数`() => string`が代入されているため

です。

これを見れば、開発者は簡単に`bar`プロパティのバグを修正することができます\(開発者は関数の`()`を呼び出すのを忘れていた、ということです\)。

## IDEのツールチップでの表示

IDEは通常、詳細なエラーメッセージ、簡潔なエラーメッセージの順にツールチップを表示します。下記はその例です:

![IDE error message example](https://raw.githubusercontent.com/basarat/typescript-book/master/images/errors/interpreting-errors/ide.png)

* 通常は、ただ詳細なエラーメッセージを見て、エラー原因`WHY?`のチェーンを頭の中に作ります
* そして、似たようなエラーをWebで検索するために簡潔なエラーメッセージを利用します\(`TSXXXX`エラーコードか、エラーメッセージの一部を使います\)

