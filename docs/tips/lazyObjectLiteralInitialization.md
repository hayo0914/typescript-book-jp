## 遅延オブジェクトのリテラルの初期化

JavaScriptコードベースでは、以下のようにしてオブジェクトリテラルを初期化します。

```ts
let foo = {};
foo.bar = 123;
foo.bas = "Hello World";
```

コードをTypeScriptに移動すると、次のようなエラーが表示されます。

```ts
let foo = {};
foo.bar = 123; // Error: Property 'bar' does not exist on type '{}'
foo.bas = "Hello World"; // Error: Property 'bas' does not exist on type '{}'
```

これは、 `let foo = {}`の状態から、TypeScript *は `foo`の型(初期化代入の左辺)を右辺`{} `の型に推論するためですプロパティなし)。それで、あなたが知らないプロパティに割り当てようとするとエラーになります。

### 理想的な修正

TypeScriptでオブジェクトを初期化する*適切な方法は、割り当てでそれを行うことです。

```ts
let foo = {
    bar: 123,
    bas: "Hello World",
};
```

これは、コードのレビューとコードのメンテナンスの目的にも最適です。

> 以下で説明するクイックフィックスとミドルグラウンド*レイジー*初期化パターンは、*誤ってプロパティを初期化することを忘れています*。

### クイックフィックス

TypeScriptに移行するJavaScriptコードベースが大きい場合は、理想的な修正が実行可能な解決策ではない可能性があります。その場合、*型アサーション*を慎重に使用してコンパイラをサイレントにすることができます：

```ts
let foo = {} as any;
foo.bar = 123;
foo.bas = "Hello World";
```

### ミドルグラウンド

もちろん、 `any`アサーションを使用することは、TypeScriptの安全性を損なうため、非常に悪いことがあります。中盤の修正は `インターフェースを作成して確実に

* 良いドキュメント
* 安全な割り当て

これを以下に示します。

```ts
interface Foo {
    bar: number
    bas: string
}

let foo = {} as Foo;
foo.bar = 123;
foo.bas = "Hello World";
```

インターフェイスを使用するとあなたを救うことができるという事実を示す簡単な例です：

```ts
interface Foo {
    bar: number
    bas: string
}

let foo = {} as Foo;
foo.bar = 123;
foo.bas = "Hello World";

// later in the codebase:
foo.bar = 'Hello Stranger'; // Error: You probably misspelled `bas` as `bar`, cannot assign string to number
}
```
