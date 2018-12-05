## 等価性(Equality)

JavaScriptで注意すべき点の1つは、 `==`と `===`の違いです。 JavaScriptはエラーに対して耐性を持たせているため、 `==` 2つの変数間で型変換を試みます。 例えば、下記のように文字列は、数値に変換されてから比較されます。

```js
console.log(5 == "5"); // true   , TS Error
console.log(5 === "5"); // false , TS Error
```

しかし、JavaScriptの選択肢は必ずしも理想的ではありません。たとえば、下の例の最初の文はfalseですが、`""`と `"0"`は両方とも文字列であり、明らかに等しくないためです。しかし、第2のケースでは、「0」と空文字列（ `" "`）は「偽」である（`false`のように振る舞う）ので、`== `に関して等価です。両方の文は、`===`を使うとfalseになります。

```js
console.log("" == "0"); // false
console.log(0 == ""); // true

console.log("" === "0"); // false
console.log(0 === ""); // false
```

> `string == number`と`string === number `はどちらもTypeScriptのコンパイル時エラーであることに注意してください。通常、これについて心配する必要はありません。

`==`と `===`と同様に、 `！=`と `！==`でも同じです。

だから、（プロとしてのアドバイス：）私たちは後で説明するnullチェックを除いて常に`===`と `！==`を使います。

## 構造の比較
`==`/ `===`は、2つのオブジェクトの構造を比較したい場合は、不十分です。例えば

```js
console.log({a:123} == {a:123}); // False
console.log({a:123} === {a:123}); // False
```
このようなチェックを行うには、[deep-equal](https://www.npmjs.com/package/deep-equal) npmパッケージを使用します。

```js
import * as deepEqual from "deep-equal";

console.log(deepEqual({a:123},{a:123})); // True
```

しかし、かなり一般的に、深い比較は必要ありません。本当に必要なのは、いくつかの`id`でチェックすることだけです。

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
