## リテラル
リテラルはJavaScriptのプリミティブである* exact *値です。

### 文字列リテラル

型として文字列リテラルを使用できます。例えば：

```ts
let foo: 'Hello';
```

ここでは `foo`という名前の変数を作成しました。*はそれに代入されるリテラル値` `Hello``のみを許可します。これは以下のとおりです：

```ts
let foo: 'Hello';
foo = 'Bar'; // Error: "Bar" is not assignable to type "Hello"
```

それらは単独ではあまり有用ではないが、タイプユニオンで結合して、強力な(そして有用な)抽象化を作成することができる。

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
TypeScriptは `boolean`と`number`リテラル型もサポートしています。

```ts
type OneToFive = 1 | 2 | 3 | 4 | 5;
type Bools = true | false;
```

### 推論
かなり一般的に `タイプ文字列はタイプ" foo "`に代入不可能なエラーを受け取ります。次の例はこれを示しています。

```js
function iTakeFoo(foo: 'foo') { }
const test = {
  someProp: 'foo'
};
iTakeFoo(test.someProp); // Error: Argument of type string is not assignable to parameter of type 'foo'
```

これは、 `test`が`{someProp：string} `型であると推定されるためです。この問題を解決するには、シンプルな型アサーションを使用して、TypeScriptに以下のようにリテラルを推測させます。

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

[TypeScript enumsは数字ベースです](../ enums.md)。上記の `CardinalDirection`の例のように、共用体型の文字列リテラルを使用して文字列ベースの列挙型をモックすることができます。次の関数を使って `Key：Value`構造体を生成することさえできます：

```ts
/** Utility function to create a K:V from a list of strings */
function strEnum<T extends string>(o: Array<T>): {[K in T]: K} {
  return o.reduce((res, key) => {
    res[key] = key;
    return res;
  }, Object.create(null));
}
```

そして、 `keyof typeof`を使ってリテラル型共用体を生成します。完全な例を次に示します。

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

例えば。 [CodeMirrorエディタには、 `readOnly`オプション(https://codemirror.net/doc/manual.html#option_readOnly)があります。これは、`boolean`またはリテラル文字列 ``nocursor '`(有効有効値` true 、false、 "nocursor")。それは次のように宣言することができます：

```ts
readOnly: boolean | 'nocursor';
```

#### 差別化された組合

[これは本の後の方](./ discriminated-unions.md)で説明します。


[](https://github.com/Microsoft/TypeScript/pull/5185)
