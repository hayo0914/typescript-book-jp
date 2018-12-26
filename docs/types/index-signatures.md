# インデックスシグネチャ(Index Signatures)

JavaScript(TypeScript)の`Object`は、他のJavaScript**オブジェクト**への参照を保持し、**文字列**でアクセスできます。

簡単な例：

```ts
let foo:any = {};
foo['Hello'] = 'World';
console.log(foo['Hello']); // World
```

キー"Hello"に文字列"World"を格納します。JavaScript**オブジェクト**を保存できると言ったので、クラスインスタンスを保存してみましょう:

```ts
class Foo {
  constructor(public message: string){};
  log(){
    console.log(this.message)
  }
}

let foo:any = {};
foo['Hello'] = new Foo('World');
foo['Hello'].log(); // World
```

また、**string**でアクセスできると言いましたね。もし他の何らかのオブジェクトをインデックスシグネチャに渡すと、JavaScriptのランタイムは`.toString`を事前に呼び出し、その文字列を得ます。これは以下の通りです：

```ts
let obj = {
  toString(){
    console.log('toString called')
    return 'Hello'
  }
}

let foo:any = {};
foo[obj] = 'World'; // toString called
console.log(foo[obj]); // toString called, World
console.log(foo['Hello']); // World
```

インデックスを示す場所で`obj`が使われるたびに`toString`が呼び出されることに注意してください。

配列は若干異なります。`number`型のインデックスを使うと、JavaScript VMは、最適化を試みます(それが実際に配列であるか、格納された要素の構造が全て一致しているかといったことに依存します)。なので`number`はそれ自身、`string`とは別の、正しいオブジェクトアクセサとみなされるべきです。以下は単純な配列の例です：

```ts
let foo = ['World'];
console.log(foo[0]); // World
```

それがJavaScriptです。ではTypeScriptでの優雅な取り扱い方を見ていきましょう。

## TypeScriptのインデックスシグネチャ

JavaScriptはインデックスシグネチャにオブジェクトを使った場合、暗黙的に`toString`を呼び出します。そのため、TypeScriptは、初心者が落とし穴にはまるのを防ぐために、エラーを出します(私はいつもstackoverflowで落とし穴にはまるJavaScriptユーザをたくさん見ています)：

```ts
let obj = {
  toString(){
    return 'Hello'
  }
}

let foo:any = {};

// ERROR: the index signature must be string, number ...
foo[obj] = 'World';

// FIX: TypeScript forces you to be explicit
foo[obj.toString()] = 'World';
```

ユーザに明示的に`toString`を使うことを強制する理由は、オブジェクトのデフォルトの`toString`実装がかなりひどいためです。v8では常に`[object Object]`を返します：

```ts
let obj = {message:'Hello'}
let foo:any = {};

// ERROR: the index signature must be string, number ...
foo[obj] = 'World';

// Here is where you actually stored it!
console.log(foo["[object Object]"]); // World
```

もちろん`number`はサポートされています。理由は以下の通りです。

1. すばらしい配列/タプルのサポートに必要です。
2. あなたが`obj`としてそれを使うとしても、デフォルトの`toString`実装はまともです(`[object Object]`ではありません)。

ポイント2を以下に示します。

```ts
console.log((1).toString()); // 1
console.log((2).toString()); // 2
```

だから、レッスン1：

> TypeScriptのインデックスシグネチャは`string`または`number`のいずれかでなければなりません。

参考まで: `symbols`もまたTypeScriptでサポートされています。しかし、まだそこには行かないでください。小さな一歩からです。

### インデックスシグネチャを宣言する

今まで私たちは、TypeScriptに私たちが望むことをさせるために`any`を使ってきました。私たちは、実際にはインデックスシグネチャを明示的に指定できます。例えば文字列を使ってオブジェクトに格納されているものが構造体`{message：string}`に従っていることを確認したいとします。これは`{[index：string]：{message：string}}`の宣言で行うことができます。これは以下のとおりです：

```ts
let foo:{ [index:string] : {message: string} } = {};

/**
 * Must store stuff that conforms to the structure
 */
/** Ok */
foo['a'] = { message: 'some message' };
/** Error: must contain a `message` or type string. You have a typo in `message` */
foo['a'] = { messages: 'some message' };

/**
 * Stuff that is read is also type checked
 */
/** Ok */
foo['a'].message;
/** Error: messages does not exist. You have a typo in `message` */
foo['a'].messages;
```

> ヒント： インデックスシグネチャの名前`{[index：string]：{message：string}}`の`index`はTypeScriptにとっては意味がなく、可読性のためだけのものです。例えばもしそれがユーザー名であれば、コードを見る次の開発者のために`{[username：string]：{message：string}}`と宣言することができます。

もちろん、`number`インデックスもサポートされています。例:`{[count：number]：SomeOtherTypeYouWantToStoreEgRebate}`

### すべてのメンバは`string`インデックスシグネチャに従わなければならない

`string`インデックスシグネチャを持つと、それと同時に、すべての明示的なメンバもそのインデックスシグネチャに準拠している必要があります。これを以下に示します:

```ts
/** Okay */
interface Foo {
  [key:string]: number
  x: number;
  y: number;
}
/** Error */
interface Bar {
  [key:string]: number
  x: number;
  y: string; // ERROR: Property `y` must be of type number
}
```

これは、すべての文字列アクセスで同じ結果が得られるように安全性を提供するためです:

```ts
interface Foo {
  [key:string]: number
  x: number;
}
let foo: Foo = {x:1,y:2};

// Directly
foo['x']; // number

// Indirectly
let x = 'x'
foo[x]; // number
```

### 文字列リテラルを制限する

インデックスシグネチャでは、マップ型(Mapped Types)などを使用して、インデックス文字列をリテラル文字列のユニオン(Union)のメンバであることを強制することができます。

```ts
type Index = 'a' | 'b' | 'c'
type FromIndex = { [k in Index]?: number }

const good: FromIndex = {b:1, c:2}

// Error:
// Type '{ b: number; c: number; d: number; }' is not assignable to type 'FromIndex'.
// Object literal may only specify known properties, and 'd' does not exist in type 'FromIndex'.
const bad: FromIndex = {b:1, c:2, d:3};
```

これは、次のページで説明するように、`keyof typeof`と一緒に使用されて語彙(vocabulary)の種類を捕捉することがよくあります。次のページで説明します。

語彙(vocabulary)の明記は一般的に後回しにされ得ます。

```ts
type FromSomeIndex<K extends string> = { [key in K]: number }
```

### `string`と`number`インデクサの両方を持つ

これは一般的な使用例ではありませんが、TypeScriptコンパイラはこれをサポートしています。

しかし、`string`インデクサは`number`インデクサよりも厳格であるという制約があります。これは意図的なものです。次のようなコードを可能にします：

```ts
interface ArrStr {
  [key: string]: string | number; // Must accommodate all members

  [index: number]: string; // Can be a subset of string indexer

  // Just an example member
  length: number;
}
```

### デザインパターン：ネストされたインデックスシグネチャ

> インデックスシグネチャを追加する際のAPIの考慮事項

JSコミュニティでは、通常、文字列インデクサを乱用するAPIをよく見かけるでしょう。例えばJSライブラリ　におけるCSSの共通パターンです:

```ts
interface NestedCSS {
  color?: string;
  [selector: string]: string | NestedCSS;
}

const example: NestedCSS = {
  color: 'red',
  '.subclass': {
    color: 'blue'
  }
}
```

このように、文字列インデクサと有効な値を混在させないようにしてください。例えばオブジェクトに入れるときのタイプミスはキャッチされません：

```ts
const failsSilently: NestedCSS = {
  colour: 'red', // No error as `colour` is a valid string selector
}
```

代わりに、ネストを独自のプロパティに分離します。例えば、`nest`(または`children`や `subnodes`など)のような名前で宣言します：

```ts
interface NestedCSS {
  color?: string;
  nest?: {
    [selector: string]: NestedCSS;
  }
}

const example: NestedCSS = {
  color: 'red',
  nest: {
    '.subclass': {
      color: 'blue'
    }
  }
}

const failsSilently: NestedCSS = {
  colour: 'red', // TS Error: unknown property `colour`
}
```

### インデックスシグネチャから特定のプロパティを除外する

場合によっては、プロパティを結合してインデックスシグニチャにしたいことがあります。これは推奨されておらず、上記のネストされたインデックスシグネチャのパターンを使用するべきです。

ただし、既存のJavaScriptをモデリングしている場合は、交差型(intersection type)で回避することができます。次に、交差型を使用せずに発生するエラーの例を示します。

```ts
type FieldState = {
  value: string
}

type FormState = {
  isValid: boolean  // Error: Does not conform to the index signature
  [fieldName: string]: FieldState
}
```

交差型を使用した場合の回避策は次のとおりです。

```ts
type FieldState = {
  value: string
}

type FormState =
  { isValid: boolean }
  & { [fieldName: string]: FieldState }
```

あなたはそれを既存のJavaScriptオブジェクトに対して宣言することができますが、そのようなオブジェクトをTypeScriptで生成できないことに注意してください。

```ts
type FieldState = {
  value: string
}

type FormState =
  { isValid: boolean }
  & { [fieldName: string]: FieldState }


// Use it for some JavaScript object you are gettting from somewhere 
declare const foo:FormState; 

const isValidBool = foo.isValid;
const somethingFieldState = foo['something'];

// Using it to create a TypeScript object will not work
const bar: FormState = { // Error `isValid` not assignable to `FieldState
  isValid: false
}
```
