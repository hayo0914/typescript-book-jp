# インデックス署名

JavaScript(したがってTypeScript)の `Object`は、他のJavaScript **オブジェクト**への参照を保持する**文字列**でアクセスできます。

ここに簡単な例があります：

```ts
let foo:any = {};
foo['Hello'] = 'World';
console.log(foo['Hello']); // World
```

キー "Hello"の下に文字列 "World"を格納します。私たちはJavaScript **オブジェクト**を保存できると言ったので、コンセプトを示すためにクラスインスタンスを保存することができます。

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

また、** string **でアクセスできると言ったことを覚えておいてください。他のオブジェクトをインデックスシグネチャに渡すと、JavaScriptランタイムは実際に結果を得る前に `.toString`を呼び出します。これは以下のとおりです：

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

`toString`は、インデックス位置で`obj`が使われるたびに呼び出されます。

配列は若干異なります。 `number`インデックスを付けるために、JavaScript VMは最適化しようとします(実際には配列であり、一致したアイテムの構造体などに応じて異なります)。だから、 `number`はそれ自身で正しいオブジェクトアクセッサーとみなされるべきです(`string`とは異なります)。以下は単純な配列の例です：

```ts
let foo = ['World'];
console.log(foo[0]); // World
```

それがJavaScriptです。ここで、このコンセプトのTypeScriptの優雅な取り扱いについて見ていきましょう。

## TypeScriptインデックスシグネチャ

最初に、JavaScript *は暗黙のうちにどんなオブジェクトインデックスシグネチャでも `toString`を呼び出すので、初心者が足で自分を撃ってしまうのを防ぐためにエラーが出ます(私はJavaScriptをスタックオーバーフロー)：

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

ユーザに明示的に強制する理由は、オブジェクトのデフォルトの `toString`実装がかなりひどいためです。 v8では常に `[object Object]`を返します：

```ts
let obj = {message:'Hello'}
let foo:any = {};

// ERROR: the index signature must be string, number ...
foo[obj] = 'World';

// Here is where you actually stored it!
console.log(foo["[object Object]"]); // World
```

もちろん `number`はサポートされています

1. 優れたアレイ/タプルのサポートに必要です。
あなたが `obj`のためにそれを使うとしても、デフォルトの`toString`実装は素晴らしいです( `[object Object]`ではなく)。

ポイント2を以下に示します。

```ts
console.log((1).toString()); // 1
console.log((2).toString()); // 2
```

だからレッスン1：

> TypeScriptのインデックスシグネチャは `string`または`number`のいずれかでなければなりません

クイックノート： `symbols 'も有効で、TypeScriptでサポートされています。しかし、まだそこには行かないでください。赤ちゃんのステップ。

### インデックス署名を宣言する

だから私たちは、TypeScriptに私たちが望むことをさせるために `any`を使っています。実際に* index *の署名を明示的に指定できます。例えば。文字列を使ってオブジェクトに格納されているものが構造体 `{message：string}`に従っていることを確認したいとします。これは `{[index：string]：{message：string}}`宣言で行うことができます。これは以下のとおりです：

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

> TIP：インデックス署名の名前。 `{[index：string]：{message：string}}`の `index`はTypeScriptにとって意味がなく、読みやすくするためだけです。例えばもしあなたがユーザー名であれば、コードを見ている次の開発者を助けるために `{[username：string]：{message：string}}`を実行することができます。

もちろん、「数」インデックスもサポートされている。 `{[count：number]：SomeOtherTypeYouWantToStoreEgRebate}`

### すべてのメンバーは `string`インデックスの署名に従わなければなりません

`string`インデックスシグネチャを持つとすぐに、すべての明示的メンバもそのインデックスシグネチャに準拠している必要があります。これを以下に示します。

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

これは、すべての文字列アクセスで同じ結果が得られるように安全性を提供するためです。

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

### 文字列リテラルの限定されたセットを使用する

インデックスシグネチャでは、マップドタイプ*などを使用して、インデックス文字列をリテラル文字列のメンバーにする必要があります。

```ts
type Index = 'a' | 'b' | 'c'
type FromIndex = { [k in Index]?: number }

const good: FromIndex = {b:1, c:2}

// Error:
// Type '{ b: number; c: number; d: number; }' is not assignable to type 'FromIndex'.
// Object literal may only specify known properties, and 'd' does not exist in type 'FromIndex'.
const bad: FromIndex = {b:1, c:2, d:3};
```

これは、次のページで説明するように、 `keyof typeof`と一緒に使用されてボキャブラリータイプをキャプチャすることがよくあります。

ボキャブラリの仕様は一般的に延期できます。

```ts
type FromSomeIndex<K extends string> = { [key in K]: number }
```

### `string`と`number`インデクサの両方を持つ

これは一般的な使用例ではありませんが、それにもかかわらずTypeScriptコンパイラはこれをサポートしています。

しかし、 `string`インデクサは`number`インデクサよりも厳格であるという制約があります。これは意図的なものです。次のようなタイプ入力を可能にする：

```ts
interface ArrStr {
  [key: string]: string | number; // Must accommodate all members

  [index: number]: string; // Can be a subset of string indexer

  // Just an example member
  length: number;
}
```

### デザインパターン：ネストされたインデックスの署名

> インデックス署名を追加する際のAPIの考慮事項

JSコミュニティでは、通常、文字列インデクサーを乱用するAPIが表示されます。例えばJSライブラリのCSS間の共通パターン：

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

このように、文字列インデクサーと*有効な*値を混在させないようにしてください。例えば。詰め物のタイプミスは未知のままです：

```ts
const failsSilently: NestedCSS = {
  colour: 'red', // No error as `colour` is a valid string selector
}
```

代わりに、ネスティングを独自のプロパティに分離します。 `nest`(または`children`や `subnodes`など)のような名前で宣言します：

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

場合によっては、プロパティをインデックスシグニチャに結合する必要があります。これは勧告されておらず、上記のネストされたインデックスシグネチャパターンを使用する必要があります。

ただし、既存のJavaScript *をモデリングしている場合は、交差点タイプで回避することができます。次に、交差点を使用せずに発生するエラーの例を示します。

```ts
type FieldState = {
  value: string
}

type FormState = {
  isValid: boolean  // Error: Does not conform to the index signature
  [fieldName: string]: FieldState
}
```

交差点タイプを使用した場合の回避策は次のとおりです。

```ts
type FieldState = {
  value: string
}

type FormState =
  { isValid: boolean }
  & { [fieldName: string]: FieldState }
```

既存のJavaScriptをモデル化するように宣言することはできますが、TypeScriptを使用してそのようなオブジェクトを作成することはできません。

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
