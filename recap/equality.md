# 等価演算子の同一性

## 等価演算子\(Equality\)

JavaScriptで注意するべき点の1つは`==`と `===`の違いです。 JavaScriptはエラーが起きにくい仕様であるため、`==`は、2つの変数の型変換を行います。 例えば、下記の場合、文字列は数値に変換されます。

```javascript
console.log(5 == "5"); // true   , TS Error
console.log(5 === "5"); // false , TS Error
```

しかし、JavaScriptの選択は必ずしも理想的ではありません。下の例の最初の行は`""`と `"0"`は両方とも文字列であり、明らかに等しくないため、falseです。しかし、第2のケースでは、`0`と空文字列\(`""`\)はfalsy\(`false`のように振る舞う\)であるため、`==`を使った比較ではtrueになります。両方とも`===`を使うとfalseになります。

```javascript
console.log("" == "0"); // false
console.log(0 == ""); // true

console.log("" === "0"); // false
console.log(0 === ""); // false
```

> TypeScriptの場合、`string == number`と`string === number`はどちらもコンパイルエラーであることに注意してください。通常は心配する必要はありません。

`==`と `===`と同様に、 `!=`と `!==`でも同じです。

そのため、\(プロとしてのアドバイス：\)我々は、後で説明するnullチェック以外は、常に`===`と `!==`を使います。

## 構造の等価性\(Structural Equality\)

`==`/`===`は、2つのオブジェクトの構造を比較したい場合は、使えません。例:

```javascript
console.log({a:123} == {a:123}); // False
console.log({a:123} === {a:123}); // False
```

このようなチェックを行うには、[deep-equal](https://www.npmjs.com/package/deep-equal) npmパッケージを使用します。

```javascript
import * as deepEqual from "deep-equal";

console.log(deepEqual({a:123},{a:123})); // True
```

しかし、一般的に、深い比較\(deep equal\)は必要ありません。開発者が本当に必要としていることは、`id`等でチェックすることで実現できます。

```typescript
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

