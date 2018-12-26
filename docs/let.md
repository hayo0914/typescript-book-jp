### let

JavaScriptにおいて`var`変数は関数スコープ(function scoped)です。これは変数がブロックスコープ(blocked scope)である他の多くの言語(C#/Javaなど)とは異なります。もしあなたがブロックスコープの考え方で以下のJavaScriptのコードを見ると、`123`を表示すると考えるでしょうが、そうではなく、`456`が表示されます。

```ts
var foo = 123;
if (true) {
    var foo = 456;
}
console.log(foo); // 456
```
これは`{`が新しい変数スコープ(variable scope)を作成しないためです。 変数`foo`はifブロックの内側にあっても外側にあっても同じです。これは、JavaScriptのプログラミングにおける一般的なエラー原因です。そのため、TypeScript(とES6)は`let`キーワードを導入して真のブロックスコープ(block scoped)の変数を定義できるようにしています。つまり、`var`の代わりに`let`を使うと、あなたはblockの外で定義したかもしれない変数から分離した、真にユニークな変数を得ることができます。先ほどと同じ例を`let`で示します：

```ts
let foo = 123;
if (true) {
    let foo = 456;
}
console.log(foo); // 123
```

`let`がエラーから守ってくれる他の場所は、繰り返しです。
```ts
var index = 0;
var array = [1, 2, 3];
for (let index = 0; index < array.length; index++) {
    console.log(array[index]);
}
console.log(index); // 0
```
間違いなく、可能なときはいつでも`let`を使うべきです。そのほうが新しい開発者や他の言語での開発者にとって直感的です。

#### 新しいスコープを作成する関数
これまで述べてきた、JavaScriptの関数が新しい変数スコープを作成することを例で示します。次のコードについて、考えてみてください。

```ts
var foo = 123;
function test() {
    var foo = 456;
}
test();
console.log(foo); // 123
```
これは期待通りに動作します。これがなければ、JavaScriptでコードを書くのは至難でしょう。

#### 生成されたJS(Generated JS)
TypeScriptによって生成されたJSは、同じ名前の`let`変数が既に周囲のスコープに存在する場合は、単純に変数名を変更します。`let`変数の単純な名前変更です。例えば、次の例は単純に、`let`を`var`に置き換えるだけです。

```ts
if (true) {
    let foo = 123;
}

// becomes //

if (true) {
    var foo = 123;
}
```
しかし、変数名が既に周囲のスコープによって捕捉されている場合、次のように新しい変数名が生成されます(`_foo`に注目)。

```ts
var foo = '123';
if (true) {
    let foo = 123;
}

// becomes //

var foo = '123';
if (true) {
    var _foo = 123; // Renamed
}
```

#### Switch
`case`文の本体(body)を`{}`で囲んで、以下に示すように、異なる`case`文で変数名を安全に再利用することができます：

```ts
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

#### クロージャ内部の`let`(let in closures)
一般的にJS Developerに対して面接で質問されることは、次のようなシンプルなプログラムが「何をログに表示するか？」です：

```ts
var funcs = [];
// create a bunch of functions
for (var i = 0; i < 3; i++) {
    funcs.push(function() {
        console.log(i);
    })
}
// call them
for (var j = 0; j < 3; j++) {
    funcs[j]();
}
```

ある人は`0,1,2`であると予想したでしょう。意外なことに、3つの関数は全て「3」を表示します。理由は、3つの関数すべて外側のスコープの変数`i`を使用しており、それらを実行するときに(第2のループで)`i`の値が`3`だからです(これは最初のループの終了条件です)。

１つの修正方法は、ループごとに、その反復(iteration)だけに付随した変数スコープを新造することです。既に習得したことですが、下記に例示するように、新しい関数を作成し、直ちに実行することで新しい変数スコープを作成することができます(IIFEパターン `(function(){/ * body * /})();`)。

```ts
var funcs = [];
// create a bunch of functions
for (var i = 0; i < 3; i++) {
    (function() {
        var local = i;
        funcs.push(function() {
            console.log(local);
        })
    })();
}
// call them
for (var j = 0; j < 3; j++) {
    funcs[j]();
}
```
ここで関数は*local*変数(わかりやすく`local`と命名しました)を閉じ込めて(それゆえ`closure`と呼ばれます)、ループ変数`i`の代わりに使用します。

> クロージャはパフォーマンスに影響を与えます(周囲のスコープの状態を保存する必要があるため)。

ループ内のES6の`let`キーワードは、同前な動作をします。

```ts
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

`var`の代わりに`let`を使うと、各ループ反復(iteration)に固有の変数`i`が生成されます。

#### 要約
`let`は、大部分のコードにおいて重宝します。コードの可読性を大幅に向上させ、プログラミングエラーの可能性を低減します。


[](https://github.com/olov/defs/blob/master/loop-closures.md)
