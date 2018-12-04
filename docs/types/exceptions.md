# 例外処理

JavaScriptには、例外のために使用できる `Error`クラスがあります。あなたは `throw`キーワードでエラーを投げます。あなたは `try`/` catch`ブロックの対でそれを捕まえることができます。

```js
try {
  throw new Error('Something bad happened');
}
catch(e) {
  console.log(e);
}
```

## エラーサブタイプ

ビルトインされた `Error`クラスのほかに、JavaScriptランタイムが投げることができる`Error`を継承するいくつかの組み込みエラークラスがあります：

### RangeError

数値変数またはパラメータが有効な範囲外にあるときに発生するエラーを表すインスタンスを作成します。

```js
// Call console with too many arguments
console.log.apply(console, new Array(1000000000)); // RangeError: Invalid array length
```

### ReferenceError

無効な参照を参照解除するときに発生するエラーを表すインスタンスを作成します。例えば

```js
'use strict';
console.log(notValidVar); // ReferenceError: notValidVar is not defined
```

### 構文エラー

有効でないJavaScriptを解析する際に発生する構文エラーを表すインスタンスを作成します。

```js
1***3; // SyntaxError: Unexpected token *
```

### TypeError

変数またはパラメータが有効な型でないときに発生するエラーを表すインスタンスを作成します。

```js
('1.2').toPrecision(1); // TypeError: '1.2'.toPrecision is not a function
```

### URIError

`encodeURI（）`または `decodeURI（）`に無効なパラメータが渡されたときに発生するエラーを表すインスタンスを生成します。

```js
decodeURI('%'); // URIError: URI malformed
```

## 常にエラーを使用する

初心者のJavaScriptデベロッパーはたまに生の文字列を投げるだけです

```js
try {
  throw 'Something bad happened';
}
catch(e) {
  console.log(e);
}
```

* しないでください*。 `Error`オブジェクトの基本的な利点は、`stack`プロパティを使ってビルドされた場所を自動的に追跡することです。

生の文字列は非常に苦しいデバッグ経験をもたらし、ログからのエラー分析を複雑にします。

## あなたはエラーを `スローする必要はありません

`Error`オブジェクトを渡すことは大丈夫です。これは、Node.jsのコールバックスタイルコードでは、最初の引数をエラーオブジェクトとしてコールバックを受け取ります。

```js
function myFunction (callback: (e?: Error)) {
  doSomethingAsync(function () {
    if (somethingWrong) {
      callback(new Error('This is my error'))
    } else {
      callback();
    }
  });
}
```

## 例外的なケース

「例外は例外的でなければならない」は、コンピュータサイエンスの一般的な言葉です。これがJavaScript（およびTypeScript）にも当てはまる理由はいくつかあります。

### どこに投げられるのか不明

次のコードを考えてみましょう。

```js
try {
  const foo = runTask1();
  const bar = runTask2();
}
catch(e) {
  console.log('Error:', e);
}
```

次の開発者は、どの関数がエラーを投げるかも知れません。コードをレビューしている人は、task1 / task2のコードとそれが呼び出す可能性のある他の関数を読み取ることなく知ることができません。

### 優雅なハンドリングを困難にする

スローする可能性のあるものの周りを明示的にキャッチして優雅にしようとすることができます：

```js
try {
  const foo = runTask1();
}
catch(e) {
  console.log('Error:', e);
}
try {
  const bar = runTask2();
}
catch(e) {
  console.log('Error:', e);
}
```

しかし、最初のタスクから2番目のタスクに物事を渡す必要がある場合、コードは乱雑になります（ 'run`を必要とする `foo`突然変異+`runTask1`の復帰から推論できないため注釈を明示的に必要とすることに注意してください） ：

```ts
let foo: number; // Notice use of `let` and explicit type annotation
try {
  foo = runTask1();
}
catch(e) {
  console.log('Error:', e);
}
try {
  const bar = runTask2(foo);
}
catch(e) {
  console.log('Error:', e);
}
```

### 型システムでうまく表現されていない

次の関数を考えてみましょう。

```ts
function validate(value: number) {
  if (value < 0 || value > 100) throw new Error('Invalid value');
}
```

このような場合に `Error`を使うのは、validate関数の型定義（`（value：number）=> void`）で表現されていないので、悪い考えです。代わりに、検証メソッドを作成するためのより良い方法は次のとおりです。

```ts
function validate(value: number): {error?: string} {
  if (value < 0 || value > 100) return {error:'Invalid value'};
}
```

そして今、型システムで表現されています。

> 非常に一般的な（シンプル/キャッチオールなど）の方法でエラーを処理しない限り、エラーをスローしないでください。
