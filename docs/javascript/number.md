## 数値(Number)
プログラミングで数値を扱うときは、その言語における数値の扱いに注意する必要があります。ここでは、JavaScriptで数字に関して注意するべき、いくつかの重要な点を説明します。

### コア型(Core Type)
JavaScriptにはたった1つの数値型しかありません。倍精度の64ビットの数値(`Number`)です。以下でその限界と望ましい解決策について説明します。

### 10進数(Decimal)
他の言語におけるdouble / floatに精通している人であれば、バイナリの浮動小数は10進数の少数と正しく対応していないことを知っているでしょう。 JavaScriptの数値を使った簡単な(そして有名な)例を以下に示します：

```js
console.log(.1 + .2); // 0.30000000000000004
```

> 正しい少数演算のためには、以下に述べる`big.js`を使います。

### 整数(Integer)
Javascriptの数値型の制限は、`Number.MAX_SAFE_INTEGER`と`Number.MIN_SAFE_INTEGER`です。

```js
console.log({max: Number.MAX_SAFE_INTEGER, min: Number.MIN_SAFE_INTEGER});
// {max: 9007199254740991, min: -9007199254740991}
```

数値の扱いにおける**安全**とは、丸め誤差が起きた数値ではないことが確実であることです。

安全でない値は、安全な限界値から`+1 か -1`離れた値であり、どんな値の加算/減算でも、結果を丸めるでしょう。

```js
console.log(Number.MAX_SAFE_INTEGER + 1 === Number.MAX_SAFE_INTEGER + 2); // true!
console.log(Number.MIN_SAFE_INTEGER - 1 === Number.MIN_SAFE_INTEGER - 2); // true!

console.log(Number.MAX_SAFE_INTEGER);      // 9007199254740991
console.log(Number.MAX_SAFE_INTEGER + 1);  // 9007199254740992 - Correct
console.log(Number.MAX_SAFE_INTEGER + 2);  // 9007199254740992 - Rounded!
console.log(Number.MAX_SAFE_INTEGER + 3);  // 9007199254740994 - Rounded - correct by luck
console.log(Number.MAX_SAFE_INTEGER + 4);  // 9007199254740996 - Rounded!
```

安全性をチェックするには、ES6の`Number.isSafeInteger`を使用します：

```js
// Safe value
console.log(Number.isSafeInteger(Number.MAX_SAFE_INTEGER)); // true

// Unsafe value
console.log(Number.isSafeInteger(Number.MAX_SAFE_INTEGER + 1)); // false

// Because it might have been rounded to it due to overflow
console.log(Number.isSafeInteger(Number.MAX_SAFE_INTEGER + 10)); // false
```

> JavaScriptは、最終的に[BigInt](https://developers.google.com/web/updates/2018/05/bigint) がサポートされます。現時点では、任意精度整数の計算を行いたい場合は、下記の`big.js`を使います。

### big.js
財務計算(例：GST計算、セントでのお金、追加など)のために数学を使用する場合は、[big.js](https://github.com/MikeMcl/big.js/)のようなライブラリを使用します。
* 完全無欠な10進演算
* 安全な範囲外の整数値

インストールは簡単です：
```bash
npm install big.js @types/big.js
```

簡単な使用例：

```js
import { Big } from 'big.js';

export const foo = new Big('111.11111111111111111111');
export const bar = foo.plus(new Big('0.00000000000000000001'));

// To get a number:
const x: number = Number(bar.toString()); // 少数点以下の精度を失う
```

> このライブラリは、チャートやキャンバスの描画など、UI /パフォーマンスが重視される目的には使用しないでください。

### NaN
数値計算が有効な数値で表現できない場合、JavaScriptは特別なNaN値を返します。古典的な例は虚数です。

```js
console.log(Math.sqrt(-1)); // NaN
```

注：等価演算子は**NaN値では機能しません**。代わりに`Number.isNaN`を使用してください：

```js
// Don't do this
console.log(NaN === NaN); // false!!

// Do this
console.log(Number.isNaN(NaN)); // true
```

### 無限(Infinity)
Numberで表現可能な値の境界は、`Number.MAX_VALUE`と`-Number.MAX_VALUE`の値として利用できます。

```js
console.log(Number.MAX_VALUE);  // 1.7976931348623157e+308
console.log(-Number.MAX_VALUE); // -1.7976931348623157e+308
```

精度が変更されない範囲外の値は、これらの限界値に制限されます。

```js
console.log(Number.MAX_VALUE + 1 == Number.MAX_VALUE);   // true!
console.log(-Number.MAX_VALUE - 1 == -Number.MAX_VALUE); // true!
```

精度が変更される範囲外の値は、特殊な値`Infinity`/`-Infinity`に解決されます。

```js
console.log(Number.MAX_VALUE + 10**1000);  // Infinity
console.log(-Number.MAX_VALUE - 10**1000); // -Infinity
```

もちろん、これらの無限大値は、それを必要とする算術演算でも現れます。

```js
console.log( 1 / 0); // Infinity
console.log(-1 / 0); // -Infinity
```

以下のように、これらの`Infinity`値を手動で使うか、`Number`クラスの静的メンバーを使うことができます：

```js
console.log(Number.POSITIVE_INFINITY === Infinity);  // true
console.log(Number.NEGATIVE_INFINITY === -Infinity); // true
```

幸運なことに、比較演算子(`<`/ `>`)は無限値に対して確実に動作します：

```js
console.log( Infinity >  1); // true
console.log(-Infinity < -1); // true
```

### 無限小(Infinitesimal)

Numberで表現可能なゼロでない最小値は、静的な`Number.MIN_VALUE`として使用できます。

```js
console.log(Number.MIN_VALUE);  // 5e-324
```

`MIN_VALUE`より小さい値(アンダーフロー値)は0に変換されます。

```js
console.log(Number.MIN_VALUE / 10);  // 0
```

> より直感的に: `Number.MAX_VALUE`より大きい値がINFINITYに丸められるように、`Number.MIN_VALUE`より小さい値は`0`に丸められます。
