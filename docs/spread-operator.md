### スプレッド演算子

スプレッド演算子の主な目的は、配列またはオブジェクトの要素を拡散させることです。これは例を用いて最もよく説明されています。

#### 適用
よく使われるケースは、配列を関数の引数に渡すことです。以前は `Function.prototype.apply`を使う必要がありました：

```ts
function foo(x, y, z) { }
var args = [0, 1, 2];
foo.apply(null, args);
```

これを行うには、以下に示すように、引数の前に `...`を付けるだけです。

```ts
function foo(x, y, z) { }
var args = [0, 1, 2];
foo(...args);
```

ここでは、 `args`配列を位置的な`arguments`に広げています。

#### デストラクション
* destructuring *でこれを使用した例はすでにあります。

```ts
var [x, y, ...remaining] = [1, 2, 3, 4];
console.log(x, y, remaining); // 1,2,[3,4]
```
ここでの動機付けは、構造を破壊するときに配列の残りの要素を簡単に取り込めるようにすることです。

#### 配列の割り当て
スプレッド演算子を使用すると、配列の*拡張バージョン*を別の配列に簡単に配置できます。これは以下の例で実証されています：

```ts
var list = [1, 2];
list = [...list, 3, 4];
console.log(list); // [1,2,3,4]
```

展開された配列を任意の位置に配置して、期待する効果を得ることができます。

```ts
var list = [1, 2];
list = [0, ...list, 4];
console.log(list); // [0,1,2,4]
```

#### オブジェクトスプレッド
オブジェクトを別のオブジェクトに広げることもできます。一般的な使用例は、オリジナルに変更を加えることなくオブジェクトにプロパティを追加するだけです。

```ts
const point2D = {x: 1, y: 2};
/** Create a new object by using all the point2D props along with z */
const point3D = {...point2D, z: 3};
```

オブジェクトの場合、スプレッド事項を置く順序。これは `Object.assign`のように動作し、あなたが期待していることを行います：最初に来るのは後で来るものによって '上書き'されます：

```ts
const point2D = {x: 1, y: 2};
const anotherPoint3D = {x: 5, z: 4, ...point2D};
console.log(anotherPoint3D); // {x: 1, y: 2, z: 4}
const yetAnotherPoint3D = {...point2D, x: 5, z: 4}
console.log(yetAnotherPoint3D); // {x: 5, y: 2, z: 4}
```

別の一般的な使用例は、単純な浅い拡張です。

```ts
const foo = {a: 1, b: 2, c: 0};
const bar = {c: 1, d: 2};
/** Merge foo and bar */
const fooBar = {...foo, ...bar};
// fooBar is now {a: 1, b: 2, c: 1, d: 2}
```

#### 要約
`apply`はJavaScriptでよく使うものなので、`this`引数にその醜い `null`を持たない方が良い構文にするのは良いことです。また、他の配列から配列を外す（destructuring）または（代入）するための専用の構文を使用すると、部分配列に対して配列処理を実行するときに便利な構文が提供されます。


[]（https://github.com/Microsoft/TypeScript/pull/1931）
