# 分割代入

TypeScriptは以下の分割\(Destructuring\)をサポートしています\(文字通り、de-structuringから来ています。つまり、構造を分解します\)。

1. オブジェクトの分割
2. 配列の分割

分割は、構造化\(structuring\)の反対と考えてください。それが簡単な理解です。JavaScriptで構造を作る方法はオブジェクトリテラルです。下記に例を示します：

```typescript
var foo = {
    bar: {
        bas: 123
    }
};
```

JavaScriptに組み込まれている素晴らしい構造化のサポートがなければ、必要に応じて新しいオブジェクトを作成することは、非常に面倒なことだったでしょう。分割\(Destructuring\)の機能はデータを取り出すために、同じような利便性をもたらしてくれるものです。

## オブジェクトの分割

分割は1行で行うことができるので非常に便利です。それ以外の方法では複数行のコードが必要です。次の場合を考えてみましょう。

```typescript
var rect = { x: 0, y: 10, width: 15, height: 20 };

// 分割代入
var {x, y, width, height} = rect;
console.log(x, y, width, height); // 0,10,15,20

rect.x = 10;
({x, y, width, height} = rect); // 外側のカッコで囲み、既存の変数に代入
console.log(x, y, width, height); // 10,10,15,20
```

ここでは、分解が無ければ、`rect`から`x、y、width、height`を1つずつ取得する必要があります。

展開した変数を、新しい変数名に割り当てるには、次のようにします。

```typescript
// 構造の作成
const obj = {"some property": "some value"};

// 分割
const {"some property": someProperty} = obj;
console.log(someProperty === "some value"); // true
```

さらに、分割を使用して構造体の深いデータを取得することもできます。次の例で示します。

```typescript
var foo = { bar: { bas: 123 } };
var {bar: {bas}} = foo; // 次と同じです: `var bas = foo.bar.bas;`
```

## オブジェクトの分割でスプレッド演算子（Restパラメータ）を使う

あるオブジェクトから任意の数の要素を取得し、残った要素をスプレッド演算子を使って取得することができます。

```typescript
var {w, x, ...remaining} = {w: 1, x: 2, y: 3, z: 4};
console.log(w, x, remaining); // 1, 2, {y:3,z:4}
```

一般的なユースケースは、特定のプロパティを無視することです。例：

```typescript
// サンプル関数
function goto(point2D: {x: number, y: number}) {
  // 余計なものが含まれたオブジェクトが渡されたら
  // 正しく動作しないようなコードを想像してください
}
// どこかから取得したPointのオブジェクト
const point3D = {x: 1, y: 2, z: 3};
/** 余計なプロパティを取り除くための、面白いスプレッド演算子の使い方 */
const { z, ...point2D } = point3D;
goto(point2D);
```

## 配列の分割

一般的なプログラミングの質問では、このようなものがあります：「3つ目の変数を使用せずに2つの変数を交換する方法は？」。TypeScriptでの解決策はこうです：

```typescript
var x = 1, y = 2;
[x, y] = [y, x];
console.log(x, y); // 2,1
```

配列の分割は、事実上コンパイラが`[0], [1], ...`などとしていることに注意してください。なので、これらの値が存在することは保証されていません。

## 配列の分割でスプレッド演算子\(Restパラメータ\)を使う

配列から任意の数の要素を取得し、残りの要素を、スプレッド演算子を使って配列として取得することができます。

```typescript
var [x, y, ...remaining] = [1, 2, 3, 4];
console.log(x, y, remaining); // 1, 2, [3,4]
```

## 配列の分割で一部の要素を無視する

あなたは、その場所を空のままにして、つまり代入の左側に`, ,`を残すだけで、特定の要素を無視することができます。例：

```typescript
var [x, , ...remaining] = [1, 2, 3, 4];
console.log(x, remaining); // 1, [3,4]
```

## 生成されるJavaScript

ES5以前をターゲットにしてコンパイルして生成されるJavaScriptでは、一時変数が使われます。

```typescript
var x = 1, y = 2;
[x, y] = [y, x];
console.log(x, y); // 2,1

// 下記のようになります //

var x = 1, y = 2;
_a = [y,x], x = _a[0], y = _a[1];
console.log(x, y);
var _a;
```

## まとめ

分割\(Destructuring\)は、行数を減らし、開発者の意図を明確にすることで、コードの可読性と保守性を高めてくれます。配列の分割を使うことにより、配列をタプル\(Tuple\)のように使うことができます。

