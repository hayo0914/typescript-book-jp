## Trueとみなされる値(Truthy)

JavaScriptは、特定の場所(例えば、`if` 条件文とbooleanの`&&` `||` オペレータ)で、Trueと評価される値(`truthy`)の概念を持っています。次に示すものは、JavaScriptにおいてtruthyです。例えば`0`以外の数値はtruthyです。

```ts
if (123) { // Will be treated like `true`
  console.log('Any number other than 0 is truthy');
}
```

truthyでないものは、`falsy`と呼ばれます。

これは開発者のための便利なリファレンスです。

| 変数の型         | *falsyな値*              | *truthyな値*             |
|-----------------|--------------------------|--------------------------|
| `boolean`       | `false`                  | `true`                   |
| `string`        | `''` (空文字列)      | その他の文字列             |
| `number`        | `0`  `NaN`               | その他の数値               |
| `null`          | 常にfalsy                 | なし                     |
| `undefined`     | 常にfalsy                 | なし                     |
| その他のオブジェクト(`{}`や`[]`といった空のものも含む) | なし | 常にtruthy |


### 明示的にする

> The `!!` pattern

一般的に、`boolean`として扱われる値を、それを本当の`boolean`(`true`|`false`)に明示的に変換することは、良いことです。あなたは、`!!`を使って値を本当のbooleanに簡単に変換できます。例えば、`!!foo`です。これは単に`!`を２回使っただけです。最初の`!`は値をbooleanに変換しますが、その論理値を反転します。２つ目の`!`は、その値を本来の値にマッチするよう再度反転させます(例えば、 *truthy* -`!`> `false` -`!`> `true`)。

これはあらゆる場面で共通的に使えるパターンです。

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
