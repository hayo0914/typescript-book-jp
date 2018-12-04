### const

`const`はES6 / TypeScriptが提供する非常に歓迎された追加です。変数を使用して不変にすることができます。これは、ドキュメンテーションだけでなく実行時の視点からも優れています。 constを使うには `var`を`const`で置き換えてください：

```ts
const foo = 123;
```

> 構文は他の言語よりもはるかに優れています（IMHO）。これはユーザーに `let constant foo`のようなものを入力させます。つまり、変数+動作指定子です。

`const`は読みやすさとメンテナンス性の両方の良い習慣であり、*魔法のリテラル*を使うのを避けます。

```ts
// Low readability
if (x > 10) {
}

// Better!
const maxRows = 10;
if (x > maxRows) {
}
```

#### const宣言を初期化する必要があります
以下はコンパイラエラーです：

```ts
const foo; // ERROR: const declarations must be initialized
```

#### 代入の左辺は定数ではありません
定数は作成後に不変です。したがって、それらを新しい値に代入しようとするとコンパイラエラーになります：

```ts
const foo = 123;
foo = 456; // ERROR: Left-hand side of an assignment expression cannot be a constant
```

#### ブロックスコープ
`const`は` `let``（./ let.md）で見たようにブロックスコープです：

```ts
const foo = 123;
if (true) {
    const foo = 456; // Allowed as its a new variable limited to this `if` block
}
```

#### 深い不変性
`const`は、変数* reference *を保護する限り、オブジェクトリテラルでも機能します：

```ts
const foo = { bar: 123 };
foo = { bar: 456 }; // ERROR : Left hand side of an assignment expression cannot be a constant
```

ただし、以下に示すように、オブジェクトのサブプロパティを変更することはできます。

```ts
const foo = { bar: 123 };
foo.bar = 456; // Allowed!
console.log(foo); // { bar: 456 }
```

このため、プリミティブや不変のデータ構造で `const`を使うことをお勧めします。
