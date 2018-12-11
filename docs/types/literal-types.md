## リテラル
リテラルはJavaScriptのプリミティブである値そのものです。

### 文字列リテラル

型として文字列リテラルを使用できます。例えば：

```ts
let foo: 'Hello';
```

ここでは`foo`という名前の変数を作成しました。それに代入されるリテラル値は`Hello`のみを許可します。これは以下のとおりです：

```ts
let foo: 'Hello';
foo = 'Bar'; // Error: "Bar" is not assignable to type "Hello"
```

それらは単独ではあまり使い所がありませんが、ユニオン型で結合して、強力な(そして便利な)抽象化を作成することができます。

```ts
type CardinalDirection =
    "North"
    | "East"
    | "South"
    | "West";

function move(distance: number, direction: CardinalDirection) {
    // ...
}

move(1,"North"); // Okay
move(1,"Nurth"); // Error!
```

### その他のリテラル型
TypeScriptは`boolean`と`number`リテラル型もサポートしています。

```ts
type OneToFive = 1 | 2 | 3 | 4 | 5;
type Bools = true | false;
```

### 推論
かなり一般的に`Type string is not assignable to type "foo"`というエラーを受け取ります。次の例はこれを示しています。

```js
function iTakeFoo(foo: 'foo') { }
const test = {
  someProp: 'foo'
};
iTakeFoo(test.someProp); // Error: Argument of type string is not assignable to parameter of type 'foo'
```

これは、`test`が`{someProp：string} `型であると推定されるためです。この問題を解決するには、シンプルな型アサーションを使用して、TypeScriptに以下のようにリテラルを推測させます。

```js
function iTakeFoo(foo: 'foo') { }
const test = {
  someProp: 'foo' as 'foo'
};
iTakeFoo(test.someProp); // Okay!
```

### ユースケース
文字列型の有効な使用例は次のとおりです。

#### 文字列ベースの列挙型

[TypeScript enumsは数字ベースです](../enums.md)。上記の`CardinalDirection`の例のようにユニオン型の文字列リテラルを使用して文字列ベースの列挙型を模倣することができます。次の関数を使って`Key：Value`構造体を生成することさえできます：

```ts
/** Utility function to create a K:V from a list of strings */
function strEnum<T extends string>(o: Array<T>): {[K in T]: K} {
  return o.reduce((res, key) => {
    res[key] = key;
    return res;
  }, Object.create(null));
}
```

そして、`keyof typeof`を使ってリテラル型の合成を生成します。完全な例を次に示します。

```ts
/** Utility function to create a K:V from a list of strings */
function strEnum<T extends string>(o: Array<T>): {[K in T]: K} {
  return o.reduce((res, key) => {
    res[key] = key;
    return res;
  }, Object.create(null));
}

/**
  * Sample create a string enum
  */

/** Create a K:V */
const Direction = strEnum([
  'North',
  'South',
  'East',
  'West'
])
/** Create a Type */
type Direction = keyof typeof Direction;

/** 
  * Sample using a string enum
  */
let sample: Direction;

sample = Direction.North; // Okay
sample = 'North'; // Okay
sample = 'AnythingElse'; // ERROR!
```

#### 既存のJavaScript APIのモデリング

例えば [CodeMirrorエディタには`readOnly`オプションがあります](https://codemirror.net/doc/manual.html#option_readOnly)。これは、`boolean`またはリテラル文字列`nocursor`(有効値: true、false、"nocursor")です。それは次のように宣言することができます：

```ts
readOnly: boolean | 'nocursor';
```

#### ユニオン型の区別

これは[本の後方](./discriminated-unions.md)で説明します。
