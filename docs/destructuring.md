### デストラクション

TypeScriptは以下の形式の分解をサポートしています（構造的に構造化されていない、つまり構造が分割されています）。

1. オブジェクトの破壊
1. アレイの破壊

構造化を構造化*の逆と考えるのは簡単です。 JavaScriptの*構造化*メソッドはオブジェクトリテラルです：

```ts
var foo = {
    bar: {
        bas: 123
    }
};
```
JavaScriptに構築されたすばらしい*構造化サポートがなければ、その場で新しいオブジェクトを作成することは、実際には非常に面倒です。破壊は、構造からデータを取り出すのと同じレベルの利便性をもたらします。

#### オブジェクトの破壊
デストラクタリングは便利です。なぜなら、1行で行うことができ、それ以外の場合は複数の行を必要とするからです。次の場合を考えてみましょう。

```ts
var rect = { x: 0, y: 10, width: 15, height: 20 };

// Destructuring assignment
var {x, y, width, height} = rect;
console.log(x, y, width, height); // 0,10,15,20

rect.x = 10;
({x, y, width, height} = rect); // assign to existing variables using outer parentheses
console.log(x, y, width, height); // 10,10,15,20
```
ここでは、非構造化がなければ `rect 'から`x、y、width、height`を一つずつ選択する必要があります。

抽出した変数を新しい変数名に割り当てるには、次のようにします。

```ts
// structure
const obj = {"some property": "some value"};

// destructure
const {"some property": someProperty} = obj;
console.log(someProperty === "some value"); // true
```

さらに、構造化を使用して構造体から* deep *データを取得することもできます。これは次の例に示されています。

```ts
var foo = { bar: { bas: 123 } };
var {bar: {bas}} = foo; // Effectively `var bas = foo.bar.bas;`
```

#### オブジェクトを破壊する
あるオブジェクトから任意の数の要素を取り上げ、残りの要素のオブジェクト*を残りのオブジェクトを使って取得することができます。

```ts
var {w, x, ...remaining} = {w: 1, x: 2, y: 3, z: 4};
console.log(w, x, remaining); // 1, 2, {y:3,z:4}
```
一般的な使用例では、特定のプロパティも無視します。例えば：
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

#### 配列の破壊
一般的なプログラミングの質問：「3つ目の変数を使用せずに2つの変数を交換する方法」。 TypeScriptソリューション：

```ts
var x = 1, y = 2;
[x, y] = [y, x];
console.log(x, y); // 2,1
```
配列の破壊は事実上コンパイラが `[0]、[1]、...`などをしていることに注意してください。これらの値が存在するという保証はありません。

#### 配列を使って破壊する
配列から任意の数の要素を取得し、残りの要素の配列*を、残りの配列の構造解除を使用して取得することができます。

```ts
var [x, y, ...remaining] = [1, 2, 3, 4];
console.log(x, y, remaining); // 1, 2, [3,4]
```

#### 配列destructuring with ignores
あなたは、その場所を空のままにして、つまり割り当ての左側に `、、`を残すだけで、インデックスを無視することができます。例えば：
```ts
var [x, , ...remaining] = [1, 2, 3, 4];
console.log(x, remaining); // 1, [3,4]
```

#### JS Generation
ES6以外のターゲットのJavaScript生成には、一時的な変数の作成が含まれています。

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
Destructuringは、行数を減らして意図を明確にすることで、コードをより読みやすく保守しやすくすることができます。配列の構造化を解除すると、配列をタプルのように使うことができます。
