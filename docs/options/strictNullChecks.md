# `strictNullChecks`

デフォルトでは、 `null`と`undefined`はTypeScriptのすべての型に割り当てられます。

```ts
let foo: number = 123;
foo = null; // Okay
foo = undefined; // Okay
```

これは、多くの人々がどのようにJavaScriptを書くかをモデルにしています。しかし、すべてのものと同様に、TypeScriptでは、 `null`か`undefined`を*割り当てることができないか*明示する*ことができます。

厳密なヌルチェックモードでは、 `null`と`undefined`は異なります：

```ts
let foo = undefined;
foo = null; // NOT Okay
```

`Member`インターフェースを持っているとしましょう：

```ts
interface Member {
  name: string,
  age?: number
}
```

全ての `メンバー 'が彼らの年齢を提供するわけではないので、`age`はオプションのプロパティです。 `age`の値は`undefined`かもしれません。

`undefined`はすべての悪の根です。ランタイムエラーが発生することがよくあります。実行時に `Error`をスローするコードを書くのは簡単です：

```ts
getMember()
  .then(member: Member => {
    const stringifyAge = member.age.toString() // Cannot read property 'toString' of undefined
  })
```

しかし、厳密なヌル・チェック・モードでは、このエラーはコンパイル時に捕捉されます。

```ts
getMember()
  .then(member: Member => {
    const stringifyAge = member.age.toString() // Object is possibly 'undefined'
  })
```

## Nullアサーション演算子

新しい `!`ポストフィックス式演算子を使用して、型チェッカがその事実を結論できない文脈でそのオペランドが非ヌルでかつ非定義であることをアサートすることができる。例えば：

```ts
// Compiled with --strictNullChecks
function validateEntity(e?: Entity) {
    // Throw exception if e is null or invalid entity
}

function processEntity(e?: Entity) {
    validateEntity(e);
    let a = e.name;  // TS ERROR: e may be null.
    let b = e!.name;  // OKAY. We are asserting that e is non-null.
}
```

> これは単なるアサーションであり、型アサーションと同じ*値がnullでないことを確認する責任があることに注意してください。非nullアサーションは、本質的にコンパイラに「nullではないことを知っているので、ヌルではないかのように使用します」と伝えます。

### 完全な代入アサーション演算子

TypeScriptは、初期化されていないクラスのプロパティについても不平を言う。

```ts
class C {
  foo: number; // OKAY as assigned in constructor
  bar: string = "hello"; // OKAY as has property initializer
  baz: boolean; // TS ERROR: Property 'baz' has no initializer and is not assigned directly in the constructor.
  constructor() {
    this.foo = 42;
  }
}
```

プロパティ名に後置された確定割り当てアサーションを使用して、コンストラクタ以外の場所で初期化することをTypeScriptに通知することができます。

```ts
class C {
  foo!: number;
  // ^
  // Notice this exclamation point!
  // This is the "definite assignment assertion" modifier.
  
  constructor() {
    this.initialize();
  }
  initialize() {
    this.foo = 0;
  }
}
```

単純な変数宣言でこのアサーションを使用することもできます(例：

```ts
let a: number[]; // No assertion
let b!: number[]; // Assert

initialize();

a.push(4); // TS ERROR: variable used before assignment
b.push(4); // OKAY: because of the assertion

function initialize() {
  a = [0, 1, 2, 3];
  b = [0, 1, 2, 3];
}
```

> すべてのアサーションと同様に、コンパイラに信頼するように指示しています。コンパイラは、コードが実際にプロパティを常に割り当てていなくても、不平を言うことはありません。
