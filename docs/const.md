### const

`const`はES6/TypeScriptで提供されている非常に嬉しい追加です。変数を不変(immutable)にできます。これは、可読性だけでなく実行時の観点からも優れています。 constを使うには`var`を`const`で置き換えてください：

```ts
const foo = 123;
```

> この構文は、`let constant foo`すなわち変数+動作指定子のようなものを入力させる他の言語よりも、ずっと優れています(私見です)。

`const`は可読性とメンテナンス性の両方において良い習慣であり、魔法のリテラル(magic literals)を使うことを避けられます。

```ts
// Low readability
if (x > 10) {
}

// Better!
const maxRows = 10;
if (x > maxRows) {
}
```

#### const宣言は初期化する必要がある
以下はコンパイラエラーです：

```ts
const foo; // ERROR: const declarations must be initialized
```

#### 代入の左辺は定数ではない
定数は作成後は不変です。したがって、それらを新しい値に代入しようとするとコンパイラエラーになります：

```ts
const foo = 123;
foo = 456; // ERROR: Left-hand side of an assignment expression cannot be a constant
```

#### ブロックスコープ
`const`は[`let`](./let.md)で見たようにブロックスコープです：

```ts
const foo = 123;
if (true) {
    const foo = 456; // Allowed as its a new variable limited to this `if` block
}
```

#### 深い不変性
`const`は、変数の参照(reference)を保護する限りにおいて、オブジェクトリテラルでも機能します：

```ts
const foo = { bar: 123 };
foo = { bar: 456 }; // ERROR : Left hand side of an assignment expression cannot be a constant
```

ただし、以下に示すように、オブジェクト内部のプロパティを変更することは可能です。

```ts
const foo = { bar: 123 };
foo.bar = 456; // Allowed!
console.log(foo); // { bar: 456 }
```

このため、プリミティブや不変(immutable)のデータ構造で`const`を使うことをお勧めします。
