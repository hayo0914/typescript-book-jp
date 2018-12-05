## Trueとみなされる値(Truthy)

JavaScriptは、Trueとみなされる値(truthy)の概念を持っています。例えば、特定の場所（例えば、`if` 条件文とbooleanの`&&` `||` オペレータ)において、trueのように評価されるものです。次に示すものは、JavaScriptにおいてtruthyです。例えば、`0`以外の数値です。

```ts
if (123) { // Will be treated like `true`
  console.log('Any number other than 0 is truthy');
}
```

truthyでないものは、`falsy`と呼ばれます。

これはあなたの参照のための便利な表です。

| 変数の型         | *falsy*である場合          | *truthy*である場合          |
|-----------------|--------------------------|--------------------------|
| `boolean`       | `false`                  | `true`                   |
| `string`        | `''` (empty string)      | その他の文字列             |
| `number`        | `0`  `NaN`               | その他の数値               |
| `null`          | 常にfalsy                 | あり得ない                 |
| `undefined`     | 常にfalsy                   | あり得ない                 |
| Any other Object including empty ones like `{}`,`[]` | あり得ない | 常にtruthy |


### 明示的であること

> The `!!` pattern

かなり一般的に、`boolean`として扱われる値を、それを本当の`boolean`(`true`|`false`)に変換することを明示的にすることは、良いことです。あなたは、`!!`を使って値を本当のbooleanに簡単に変換できます。例えば、`!!foo`です。これは単に`!`を２回使っただけです。最初の`!`は値をbooleanに変換しますが、その論理値を反転します。２つ目の`!`は、その値を本来の値にマッチするよう再度反転させます(例えば、 *truthy* -`!`> `false` -`!`> `true`)。

これは様々な場所で共通的に利用できるパターンです。例:

```js
// Direct variables
const hasName = !!name;

// As members of objects
const someObj = {
  hasName: !!name
}

// e.g. in ReactJS JSX
{!!someName && <div>{someName}</div>}
```
