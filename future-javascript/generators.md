# ジェネレータ

`function *`は_ジェネレータ関数_の作成に使う構文です。ジェネレータ関数を呼び出すと、_ジェネレータオブジェクト_が返されます。ジェネレータオブジェクトは、[イテレータ](iterators.md)インターフェースに準拠しています\(つまり`next`、`return`および`throw`関数を実装しています\)。

ジェネレータが必要となる背景には2つの重要な動機があります。

## 遅延評価

ジェネレータ関数を使用して遅延評価されるイテレータを作成することができます。次の関数は、必要なだけの整数の**無限**リストを返します：

```typescript
function* infiniteSequence() {
    var i = 0;
    while(true) {
        yield i++;
    }
}

var iterator = infiniteSequence();
while (true) {
    console.log(iterator.next()); // { value: xxxx, done: false } forever and ever
}
```

もちろんイテレータが終了した場合は、以下に示すように`{ done: true }`の結果を得られます。

```typescript
function* idMaker(){
  let index = 0;
  while(index < 3)
    yield index++;
}

let gen = idMaker();

console.log(gen.next()); // { value: 0, done: false }
console.log(gen.next()); // { value: 1, done: false }
console.log(gen.next()); // { value: 2, done: false }
console.log(gen.next()); // { done: true }
```

## ジェネレータ関数の外部制御

これはジェネレータの真にエキサイティングな部分です。本質的には、関数がその実行を一時停止し、残りの関数実行の制御（運命）を呼び出し元に渡すことができます。

ジェネレータ関数は、呼び出した時には実行されません。単にジェネレータオブジェクトを作るだけです。サンプルの実行とともに次の例を考えてみましょう:

```typescript
function* generator(){
    console.log('Execution started');
    yield 0;
    console.log('Execution resumed');
    yield 1;
    console.log('Execution resumed');
}

var iterator = generator();
console.log('Starting iteration'); // これはジェネレータ関数の本体の前に実行されます
console.log(iterator.next()); // { value: 0, done: false }
console.log(iterator.next()); // { value: 1, done: false }
console.log(iterator.next()); // { value: undefined, done: true }
```

これを実行すると、次の出力が得られます。

```text
$ node outside.js
Starting iteration
Execution started
{ value: 0, done: false }
Execution resumed
{ value: 1, done: false }
Execution resumed
{ value: undefined, done: true }
```

* 関数はジェネレータオブジェクトに対して`next`が呼び出された時に1回だけ実行されます
* 関数は`yield`文が出現するとすぐに一時停止します
* 関数は`next`が呼び出されたときに再開します

> つまり、基本的にジェネレータ関数の実行は、ジェネレータオブジェクトによって制御することができます。

ここまで、ジェネレータを使った通信は、ほとんどがジェネレータがイテレータの値を返す、一方向のものでした。JavaScriptのジェネレータの非常に強力な機能の1つは、双方向の通信を可能にすることです!

* `iterator.next(valueToInject)`を使って、`yield`式の返却値を制御することができます
* `iterator.throw(error)`を使って`yield`式の位置で例外を投げることができます

次の例は `iterator.next(valueToInject)`を示しています：

```typescript
function* generator() {
    var bar = yield 'foo';
    console.log(bar); // bar!
}

const iterator = generator();
// 最初に`yield`された値を取得するまで実行する
const foo = iterator.next();
console.log(foo.value); // foo
// `bar`を注入して処理を再開する
const nextThing = iterator.next('bar');
```

次の例は `iterator.throw(error)`を示しています：

```typescript
function* generator() {
    try {
        yield 'foo';
    }
    catch(err) {
        console.log(err.message); // bar!
    }
}

var iterator = generator();
// 最初に`yield`された値を取得するまで実行する
var foo = iterator.next();
console.log(foo.value); // foo
// 処理を再開させ、`bar`エラーを発生させる
var nextThing = iterator.throw(new Error('bar'));
```

まとめると、このようになります：

* `yield`は、ジェネレータ関数の通信を一時停止し、関数の外部に制御を渡すことを可能にします
* 外部から、ジェネレータ関数本体に値を送ることができます
* 外部から、ジェネレータ関数本体に対して例外を`throw`することができます

これが、どのように便利なのでしょうか？ 次のセクション[**async/await**](async-await.md)でそれを説明します。

[iterator](iterators.md) [async-await](async-await.md)

