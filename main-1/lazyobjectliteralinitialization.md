# Lazy Object Literal Initialization

かなり一般的に、JavaScriptのコードベースでは、以下のようにしてオブジェクトリテラルを初期化します。

```typescript
let foo = {};
foo.bar = 123;
foo.bas = "Hello World";
```

コードをTypeScriptに移すと即座に次のようなエラーが表示されます。

```typescript
let foo = {};
foo.bar = 123; // Error: Property 'bar' does not exist on type '{}'
foo.bas = "Hello World"; // Error: Property 'bas' does not exist on type '{}'
```

これは、`let foo = {}`の状態から、TypeScriptは`foo`の型\(初期化代入の左辺\)を右辺`{}`の型に推論するためです\(プロパティの無いオブジェクト\)。そのため、あなたがTypeScriptが知らないプロパティに代入しようとするとエラーになります。

## 理想的な修正

TypeScriptでオブジェクトを初期化する適切な方法は、代入でそれを行うことです。

```typescript
let foo = {
    bar: 123,
    bas: "Hello World",
};
```

これは、コードのレビューと保守性の意味でも適しています。

> 以下で説明する簡単な修正と、妥協的な遅延初期化パターンは、プロパティを初期化すること忘れることに苛まれます。

## 簡単な修正\(Quick Fix\)

TypeScriptに移行するJavaScriptコードベースが大きい場合は、理想的な修正が実行可能な解決策ではない可能性があります。その場合、_型アサーション_を慎重に使用してコンパイラをサイレントにすることができます：

```typescript
let foo = {} as any;
foo.bar = 123;
foo.bas = "Hello World";
```

## 妥協\(Middle Ground\)

もちろん、`any`アサーションを使用することは、TypeScriptの安全性を損なうため、非常に悪いことがあります。妥協的なfixは、インターフェースを作り、以下を確実にすることです。

* 良いドキュメント
* 安全な代入

これを以下に示します。

```typescript
interface Foo {
    bar: number
    bas: string
}

let foo = {} as Foo;
foo.bar = 123;
foo.bas = "Hello World";
```

インターフェースを使用するとバグから救われるという事実を示す簡単な例です：

```typescript
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

