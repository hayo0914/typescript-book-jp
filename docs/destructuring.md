### 分解(Destructuring)

TypeScriptは以下の形式の分解(Destructuring)をサポートしています(文字通り、de-structuringから来ています。つまり、構造を分解します)。

1. オブジェクトの分解
1. 配列の分解

分解は、構造化(structuring)の反対と考えるのが簡単です。JavaScriptの構造化手段はオブジェクトリテラルです：

```ts
var foo = {
    bar: {
        bas: 123
    }
};
```
JavaScriptに構築されたすばらしい構造化サポートがなければ、その場で新しいオブジェクトを作成することは、実際には非常に面倒です。分解は構造からデータを取り出すことに同じレベルの利便性をもたらします。

#### オブジェクトの分解
分解は1行で行うことができるので非常に便利です。それ以外の方法では複数行のコードが必要です。次の場合を考えてみましょう。

```ts
var rect = { x: 0, y: 10, width: 15, height: 20 };

// Destructuring assignment
var {x, y, width, height} = rect;
console.log(x, y, width, height); // 0,10,15,20

rect.x = 10;
({x, y, width, height} = rect); // assign to existing variables using outer parentheses
console.log(x, y, width, height); // 10,10,15,20
```
ここでは、分解が無ければ、`rect`から`x、y、width、height`を一つずつ取得する必要があります。

展開した変数を、新しい変数名に割り当てるには、次のようにします。

```ts
// structure
const obj = {"some property": "some value"};

// destructure
const {"some property": someProperty} = obj;
console.log(someProperty === "some value"); // true
```

さらに、分解を使用して構造体から深いデータを取得することもできます。次の例で示します。

```ts
var foo = { bar: { bas: 123 } };
var {bar: {bas}} = foo; // Effectively `var bas = foo.bar.bas;`
```

#### オブジェクト分解でスプレッド演算子(rest)を使う
あるオブジェクトから任意の数の要素を取得し、残った要素をスプレッド演算子を使って取得することができます。

```ts
var {w, x, ...remaining} = {w: 1, x: 2, y: 3, z: 4};
console.log(w, x, remaining); // 1, 2, {y:3,z:4}
```
一般的なユースケースは、特定のプロパティを無視することです。例：
```ts
// Example function
function goto(point2D: {x: number, y: number}) {
  // Imagine some code that might break
  // if you pass in an object
  // with more items than desired
}
// Some point you get from somewhere
const point3D = {x: 1, y: 2, z: 3};
/** A nifty use of rest to remove extra properties */
const { z, ...point2D } = point3D;
goto(point2D);
```

#### 配列の分解
一般的なプログラミングの質問：「3つ目の変数を使用せずに2つの変数を交換する方法は？」。TypeScriptでの解決策：

```ts
var x = 1, y = 2;
[x, y] = [y, x];
console.log(x, y); // 2,1
```
配列の分解は事実上コンパイラが`[0], [1], ...`をしていることに注意してください。これらの値が存在する保証はありません。

#### 配列分解でスプレッド演算子(rest)を使う
配列から任意の数の要素を取得し、残りの要素を、スプレッド演算子を使って配列として取得することができます。

```ts
var [x, y, ...remaining] = [1, 2, 3, 4];
console.log(x, y, remaining); // 1, 2, [3,4]
```

#### 配列分解で一部の要素を無視する
あなたは、その場所を空のままにして、つまり代入の左側に`, ,`を残すだけで、インデックスを無視することができます。例：
```ts
var [x, , ...remaining] = [1, 2, 3, 4];
console.log(x, remaining); // 1, [3,4]
```

#### 生成されるJS
ES6以外をターゲットにして生成されるJavaScriptには、一時変数の作成が含まれています。

```ts
var x = 1, y = 2;
[x, y] = [y, x];
console.log(x, y); // 2,1

// becomes //

var x = 1, y = 2;
_a = [y,x], x = _a[0], y = _a[1];
console.log(x, y);
var _a;
```

#### 要約
分解(Destructuring)は、行数を減らして意図を明確にすることで、コード可読性と保守性を高めます。配列分解を使うことにより、配列をタプル(組)のように使うことができます。
