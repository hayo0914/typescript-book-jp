## 平等

JavaScriptで注意すべき点の1つは、 `==`と `===`の違いです。 JavaScriptが試みるように
プログラミングエラーに対して弾力性がある `==` 2つの変数間で型強制を試みる。 aを変換する
文字列を数値に変換して、数値と比較することができます。

```js
console.log(5 == "5"); // true   , TS Error
console.log(5 === "5"); // false , TS Error
```

しかし、JavaScriptの選択肢は必ずしも理想的ではありません。たとえば、次の例では、最初の文はfalseです
`` ``と ``0 '`は両方とも文字列であり、明らかに等しくないためです。しかし、第2のケースでは、「0」と
空文字列（ `" "`）は偽である（すなわち、 `false`のように振る舞う）ので、`== `に関して等しい。両方のステートメント
`===`を使うとfalseになります。

```js
console.log("" == "0"); // false
console.log(0 == ""); // true

console.log("" === "0"); // false
console.log(0 === ""); // false
```

> `string == number`と`string === number `はどちらもTypeScriptのコンパイル時エラーであることに注意してください。通常、これについて心配する必要はありません。

`==`と `===`と同様に、 `！=`と `！==`

だからProTip：私たちは後で説明するヌルチェックを除いて常に `===`と `！==`を使います。

## 構造平等
`==`/ `===`の2つのオブジェクトを比較したい場合は、***ではありません。例えば

```js
console.log({a:123} == {a:123}); // False
console.log({a:123} === {a:123}); // False
```
このようなチェックを行うには、[deep-equal]（https://www.npmjs.com/package/deep-equal）npmパッケージを使用します。

```js
import * as deepEqual from "deep-equal";

console.log(deepEqual({a:123},{a:123})); // True
```

しかし、かなり一般的に深いチェックは必要ありません。本当に必要なのは、いくつかの `id`でチェックすることだけです。

```ts
type IdDisplay = {
  id: string,
  display: string
}
const list: IdDisplay[] = [
  {
    id: 'foo',
    display: 'Foo Select'
  },
  {
    id: 'bar',
    display: 'Bar Select'
  },
]

const fooIndex = list.map(i => i.id).indexOf('foo');
console.log(fooIndex); // 0
```
