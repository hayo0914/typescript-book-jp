# let

JavaScriptにおいて`var`変数は**関数スコープ**\(function scope\)です。これは変数が**ブロックスコープ**\(blocked scope\)である他の多くの言語\(C\#/Javaなど\)とは異なります。もし、あなたがブロックスコープの考え方で以下のJavaScriptコードを見ると、`123`を表示すると思うかもしれません。しかし、実際には`456`が表示されます。

```typescript
var foo = 123;
if (true) {
    var foo = 456;
}
console.log(foo); // 456
```

これは`{`が新しい**変数スコープ**\(variable scope\)を作成しないためです。 変数`foo`はifブロックの内側にあっても外側にあっても同じです。これは、JavaScriptのプログラミングにおける一般的なエラーの原因です。そのため、TypeScript\(とES6\)は`let`キーワードを導入して真のブロックスコープ\(block scoped\)の変数を定義できるようにしています。つまり、`var`の代わりに`let`を使うと、スコープの外側で定義されているかもしれない変数とは異なる、真にユニークな変数を得ることができます。先ほどと同じ例を`let`で示します：

```typescript
let foo = 123;
if (true) {
    let foo = 456;
}
console.log(foo); // 123
```

`let`がエラーを防止してくれる他の場所は、ループ処理です。

```typescript
var index = 0;
var array = [1, 2, 3];
for (let index = 0; index < array.length; index++) {
    console.log(array[index]);
}
console.log(index); // 0
```

間違いなく、可能なときはいつでも`let`（または`const`）を使うべきです。そのほうが新しく学ぶ開発者や他の言語の経験者にとって直感的です。

## 関数はスコープを新たに作成する

これまで述べてきた、JavaScriptの関数が新しい変数スコープを作成することを例で示します。次のコードについて、考えてみてください。

```typescript
var foo = 123;
function test() {
    var foo = 456;
}
test();
console.log(foo); // 123
```

これは期待通りに動作します。これがなければ、JavaScriptでコードを書くのは至難の業でしょう。

## 生成されたJS\(Generated JS\)

TypeScriptによって生成されたJSは、同じ名前の`let`変数が既に周囲のスコープに存在する場合は、単純に変数名を変更します。`let`変数を単純なリネームします。例えば、次の例をみてください。`let`が`var`に置き換えられるだけです:

```typescript
if (true) {
    let foo = 123;
}

// 下記のようになります //

if (true) {
    var foo = 123;
}
```

しかし、変数名が既に周囲のスコープによって捕捉されている場合には、次のように新しい変数名が生成されます\(`_foo`に注目\)。

```typescript
var foo = '123';
if (true) {
    let foo = 123;
}

// 下記のようになります //

var foo = '123';
if (true) {
    var _foo = 123; // リネームされています
}
```

## Switch文

`case`文の本体\(body\)を`{}`で囲んで、異なる`case`文で変数名を安全に再利用することができます：

```typescript
switch (name) {
    case 'x': {
        let x = 5;
        // ...
        break;
    }
    case 'y': {
        let x = 10;
        // ...
        break;
    }
}
```

## クロージャ内の`let`

一般的にJavaScriptのDeveloperに対して面接で質問されることは、次のような単純なプログラムが、「何をログに表示するか？」という質問です：

```typescript
var funcs = [];
// たくさんの関数を作成する
for (var i = 0; i < 3; i++) {
    funcs.push(function() {
        console.log(i);
    })
}
// それらを呼び出す
for (var j = 0; j < 3; j++) {
    funcs[j]();
}
```

ある人は`0,1,2`であると予測したでしょう。意外なことに、3つの関数はすべて「3」を表示します。理由は、3つの関数すべて外側のスコープの変数`i`を使用しており、それらを実行するときに\(第2のループで\)`i`の値が`3`だからです\(これは最初のループの終了条件です\)。

修正方法のひとつは、ループごとに、その反復だけの変数スコープを新しく作ることです。既に学んだことですが、下記に示すように、新しい関数を作成し、ただちに実行することで新しい変数スコープを作成できます\(IIFEつまり即時関数実行式のパターンです `(function(){/ * body * /})();`\)。

```typescript
var funcs = [];
// たくさんの関数を作成する
for (var i = 0; i < 3; i++) {
    (function() {
        var local = i;
        funcs.push(function() {
            console.log(local);
        })
    })();
}
// それらを呼び出す
for (var j = 0; j < 3; j++) {
    funcs[j]();
}
```

ここで関数は_local_変数\(わかりやすく`local`と命名しました\)を閉じ込めて\(これが`closure`と呼ばれる所以です\)、ループ変数`i`の代わりに使用します。

> クロージャはパフォーマンスに影響を与えます\(周囲のスコープの状態を保存する必要があるためです\)。

ループ内のES6の`let`キーワードは、前に示した例とまったく同じように振る舞います:

```typescript
var funcs = [];
// create a bunch of functions
for (let i = 0; i < 3; i++) { // Note the use of let
    funcs.push(function() {
        console.log(i);
    })
}
// call them
for (var j = 0; j < 3; j++) {
    funcs[j]();
}
```

`var`の代わりに`let`を使うと、各ループ反復ごとに固有の変数`i`が作られます。

## まとめ

`let`は、コードのあらゆる場所で非常に役に立ちます。コードの可読性を大きく改善し、プログラミングの誤りを防止します。

