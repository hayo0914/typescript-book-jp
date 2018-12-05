### 発電機
`function *`とも呼ばれるジェネレータを使うと、実行を一時停止した後、一時停止/再開の遷移の間の状態を維持したまま再開することができる関数を作成することができます。ジェネレータから返される値は `iterator`と呼ばれ、この`pause-resume`遷移を制御するために使用できます。

ここでは、整数の*無限*リストを生成するジェネレータ関数の簡単な例を示します。

```ts
function* wholeNumbers() {
    var current = 0;
    while(true) {
        yield current++;
    }
}
```

`yield`コンテキストキーワードは、オプションの値(ここでは`current`)とともにジェネレータからの制御を戻す(事実上関数の実行を一時停止する)ために使用されます。 `iterator`の`.next() `メンバ関数を使ってこの値にアクセスできます。これは以下の通りです：

```ts
function* wholeNumbers() {
    var current = 0;
    while(true) {
        yield current++;
    }
}
var iterator = wholeNumbers();
console.log(iterator.next()); // 0
console.log(iterator.next()); // 1
console.log(iterator.next()); // 2
// so on till infinity....
```

これで `function *`、 `yield`、`.next() `を見てきました。

#### キャッチエラー
ジェネレータからスローされた(意図的に `スロー`または意図せずにエラーが発生したために)スローされたエラーは、通常の関数の実行と同様に `try / catch 'を使って捕捉できます。これは以下のとおりです：

```ts
function* wholeNumbers() {
    var current = 0;
    while(true) {
      if (current === 3)
        throw new Error('3 is the magic number');
      else
        yield current++;
    }
}
var iterator = wholeNumbers();
console.log(iterator.next()); // 0
console.log(iterator.next()); // 1
console.log(iterator.next()); // 2
try {
    console.log(iterator.next()); // Will throw an error
}
catch(ex) {
    console.log(ex.message); // 3 is the magic number
}
```

#### 外部で関数の実行を制御する
ジェネレータ関数から返されたイテレータは、ジェネレータ関数の状態*を制御するためにも使用できます。

// TODO：example
