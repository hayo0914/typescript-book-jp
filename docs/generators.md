## 発電機

> 注記：意味のある方法でTypeScriptでジェネレータを使用することはできません(ES5エミッタが進行中です)。しかし、それはすぐに変わるので、私たちはまだこの章を持っています。

`function *`は*ジェネレータ関数*の作成に使われる構文です。ジェネレータ関数を呼び出すと、ジェネレータオブジェクト*が返されます。ジェネレータオブジェクトは、[iterator] [iterator]インタフェース(すなわち、 `next`、`return`および `throw`関数)の直後にあります。

ジェネレータ機能には2つの重要な動機があります。

### レイジーイテレータ

ジェネレータ関数を使用して遅延イテレータを作成することができます。次の関数は、必要に応じて整数の**無限**リストを返します：

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

もちろんイテレータが終了した場合は、以下に示すように `{done：true}`の結果が得られます。

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

### 外部制御の実行
これは本当にエキサイティングな発電機の一部です。本質的には、関数がその実行を一時停止し、残りの関数実行の制御(運命)を呼び出し元に渡すことができます。

ジェネレータ関数は、呼び出したときには実行されません。これはジェネレータオブジェクトを作成するだけです。サンプルの実行とともに次の例を考えてみましょう。

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

* 関数はジェネレータオブジェクトに対して `next`が呼び出されると実行を開始します。
* 関数は `yield`文が出現するとすぐに*を一時停止します。
* 関数nextは、 `next`が呼び出されたときに*を再開します。

> 本質的にジェネレータ関数の実行は、ジェネレータオブジェクトによって制御可能です。

ジェネレータを使った私たちのコミュニケーションは、ジェネレータがイテレータの値を返すほとんど1つの方法でした。 JavaScriptのジェネレータの非常に強力な機能の1つは、双方向通信を可能にすることです!

* `iterator.next(valueToInject)`を使って、 `yield`式の結果の値を制御することができます。
* あなたは `iterator.throw(error)`を使って `yield`式のポイントで例外を投げることができます

次の例は `iterator.next(valueToInject)`を示しています：

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

ここに要約があります：
* `yield`は、ジェネレータ関数が通信を一時停止し、外部システムに制御を渡すことを許可します
* 外部システムは、ジェネレータ関数本体に値をプッシュすることができます
外部システムがジェネレータ関数本体に例外をスローする

これはどのように便利ですか？次のセクション[** async / await **] [async-await]に移動して調べてください。

[iterator]：./ iterators.md
[async-await]：./ async-await.md
