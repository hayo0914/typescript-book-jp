### let

`var`JavaScriptの変数は* function scoped *です。これは変数がブロックスコープ*である他の多くの言語（C#/ Javaなど）とは異なります。 *ブロックスコープのマインドセットをJavaScriptに持ってきた場合、 `123`を印刷すると、`456`が表示されます。

```ts
var foo = 123;
if (true) {
    var foo = 456;
}
console.log(foo); // 456
```
これは `{`が新しい*可変スコープ*を作成しないためです。変数 `foo`はifブロックの内側と同じですが、ifブロックの外側にあります。これは、JavaScriptプログラミングの一般的なエラーの原因です。これは、TypeScript（とES6）が `let`キーワードを導入して真のブロックスコープ*で変数を定義できるようにする理由です。つまり、 `var`の代わりに`let`を使うと、あなたはスコープの外で定義したかもしれないものから切り離された本当のユニークな要素を得るでしょう。同じ例が `let`で示されています：

```ts
let foo = 123;
if (true) {
    let foo = 456;
}
console.log(foo); // 123
```

`let`がエラーからあなたを救う別の場所はループです。
```ts
var index = 0;
var array = [1, 2, 3];
for (let index = 0; index < array.length; index++) {
    console.log(array[index]);
}
console.log(index); // 0
```
すべての誠意を持って、新しい、既存の多言語開発者には驚きが少なくなるので、可能な限り「let」を使用するほうがよいとわかります。

#### 新しいスコープを作成する関数
これまで述べてきたことから、関数がJavaScriptで新しい変数スコープを作成することを実証したいと思います。次の点を考慮してください。

```ts
var foo = 123;
function test() {
    var foo = 456;
}
test();
console.log(foo); // 123
```
これは期待通りに動作します。これがなければ、JavaScriptでコードを書くのは非常に難しいでしょう。

#### 生成されたJS
TypeScriptによって生成されたJSは、類似の名前が既に周囲のスコープに存在する場合、 `let`変数の単純な名前変更です。例えば。 `var`を`let`に置き換えるだけで、次のように生成されます：

```ts
if (true) {
    let foo = 123;
}

// becomes //

if (true) {
    var foo = 123;
}
```
しかし、変数名がすでに周囲のスコープによって取得されている場合、新しい変数名が次のように生成されます（ `_foo`に注目してください）。

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

#### スイッチ
あなたの `case '体を`{} `で囲んで、以下に示すように異なる`case`文で変数名を確実に再利用することができます：

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

#### 閉鎖する
JavaScript開発者のための一般的なプログラミング面接の質問は、この単純なファイルのログです。

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
1人はそれが `0,1,2 'であると予想していたでしょう。意外なことに、それは3つの機能全てに対して「3」になるだろう。理由は、3つの関数すべてが外側のスコープからの変数 `i`を使用しており、それらを実行するときに（第2のループで）`i`の値が `3`（これは最初のループの終了条件です）。

修正は、そのループ反復に特有の各ループ内に新しい変数を作成することである。前に習得したように、新しい関数を作成し、直ちに実行することで新しい変数スコープを作成することができます（つまり、 `（function（）{/ * body * /}）（）;`クラスからのIIFEパターン：

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
ここで関数は* local *変数（便宜的に `local`と呼ぶ）を閉じる（それゆえ`クロージャー 'と呼ばれます）、ループ変数 `i`の代わりにそれを使用します。

> クロージャはパフォーマンスに影響を与えます（周囲の状態を保存する必要があります）。

ループ内のES6の `let`キーワードは、前の例と同じ動作をします：

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

`var`の代わりに`let`を使うと、各ループ反復に固有の変数 `i`が生成されます。

#### 要約
`let`は、大部分のコードに対して非常に便利です。コードの可読性を大幅に向上させ、プログラミングエラーの可能性を減らすことができます。



[]（https://github.com/olov/defs/blob/master/loop-closures.md）
