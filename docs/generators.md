## ジェネレータ(Generators)

`function *`は*ジェネレータ関数*の作成に使う構文です。ジェネレータ関数を呼び出すと、*ジェネレータオブジェクト*(Generator Object)が返されます。ジェネレータオブジェクトは、[イテレータ](./iterators.md)インタフェースと同じです(つまり`next`、`return`および`throw`関数)。

ジェネレータ機能が必要となる背景には２つの重要な鍵があります。

### 遅延イテレータ(Lazy Iterators)

ジェネレータ関数を使用して遅延イテレータを作成することができます。次の関数は、必要なだけの整数の**無限**リストを返します：

```ts
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

もちろんイテレータが終了した場合は、以下に示すように`{done：true}`の結果を得られます。

```ts
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

### 外部制御による実行(Externally Controlled Execution)
これはジェネレータの本当にエキサイティングな部分です。本質的には、関数がその実行を一時停止し、残りの関数実行の制御をコール元に渡すことができます。

ジェネレータ関数は、コールした時には実行されません。これはジェネレータオブジェクトを作成するだけです。サンプルの実行とともに次の例を考えてみましょう:

```ts
function* generator(){
    console.log('Execution started');
    yield 0;
    console.log('Execution resumed');
    yield 1;
    console.log('Execution resumed');
}

var iterator = generator();
console.log('Starting iteration'); // This will execute before anything in the generator function body executes
console.log(iterator.next()); // { value: 0, done: false }
console.log(iterator.next()); // { value: 1, done: false }
console.log(iterator.next()); // { value: undefined, done: true }
```

これを実行すると、次の出力が得られます。

```
$ node outside.js
Starting iteration
Execution started
{ value: 0, done: false }
Execution resumed
{ value: 1, done: false }
Execution resumed
{ value: undefined, done: true }
```

* 関数はジェネレータオブジェクトに対して`next`が呼び出された時に１回だけ実行されます
* 関数は`yield`文が出現するとすぐに一時停止します
* 関数は`next`が呼び出されたときに再開します

> なので、本質的にジェネレータ関数の実行は、ジェネレータオブジェクトによって制御することができます。

ジェネレータを使った我々のコミュニケーションは、ジェネレータが返す値がほとんど唯一の方法でした。JavaScriptのジェネレータの非常に強力な機能の1つは、双方向のコミュニケーションを可能にすることです!

* `iterator.next(埋め込み値)`を使って、`yield`式の結果の値を制御することができます
* `iterator.throw(error)`を使って`yield`式の位置で例外を投げることができます

次の例は `iterator.next(埋め込み値)`を示しています：

```ts
function* generator() {
    var bar = yield 'foo';
    console.log(bar); // bar!
}

const iterator = generator();
// Start execution till we get first yield value
const foo = iterator.next();
console.log(foo.value); // foo
// Resume execution injecting bar
const nextThing = iterator.next('bar');
```

次の例は `iterator.throw(error)`を示しています：

```ts
function* generator() {
    try {
        yield 'foo';
    }
    catch(err) {
        console.log(err.message); // bar!
    }
}

var iterator = generator();
// Start execution till we get first yield value
var foo = iterator.next();
console.log(foo.value); // foo
// Resume execution throwing an exception 'bar'
var nextThing = iterator.throw(new Error('bar'));
```

ここに要約を記載します：
* `yield`は、ジェネレータ関数のコミュニケーションを一時停止し、外部システムに制御を渡すことを可能にします
* 外部システムは、ジェネレータ関数本体に値を送ることができます
* 外部システムは、ジェネレータ関数本体に例外をスローすることができます

これが、どのように便利なのでしょうか？次のセクション[**async/await**][async-await]に移動して調べてください。

[iterator](./iterators.md)
[async-await](./ async-await.md)
