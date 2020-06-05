# const

`const`はES6/TypeScriptで提供された非常に歓迎すべき追加です。変数を**イミュータブル**\(immutable\)にできます。これは、可読性だけでなく実行時の視点からも優れています。 constを使うには、単に`var`を`const`で置き換えるだけです:

```typescript
const foo = 123;
```

> この構文は、`let constant foo`すなわち変数+動作指定子のようなものを入力させる他の言語よりも、ずっと優れています\(個人的な意見です\)。

`const`は可読性とメンテナンス性のどちらにとっても良い習慣です。そして、マジックリテラル\(magic literals\)を使うことを避けることができます。

```typescript
// Low readability
if (x > 10) {
}

// Better!
const maxRows = 10;
if (x > maxRows) {
}
```

## const宣言は初期化する必要があります

以下はコンパイルエラーになります：

```typescript
const foo; // ERROR: const declarations must be initialized
```

## 代入の左辺に定数は置けない

作成された定数はイミュータブルです。したがって、新しい値を代入しようとするとコンパイルエラーになります：

```typescript
const foo = 123;
foo = 456; // ERROR: Left-hand side of an assignment expression cannot be a constant
```

## ブロックスコープ

`const`は[`let`](let.md)と同様に**ブロックスコープ**です：

```typescript
const foo = 123;
if (true) {
    const foo = 456; // Allowed as its a new variable limited to this `if` block
}
```

## 深い不変性 \(deep immutability\)

`const`は、変数の参照\(reference\)を保護する限りにおいて、オブジェクトリテラルでも機能します：

```typescript
const foo = { bar: 123 };
foo = { bar: 456 }; // ERROR : Left hand side of an assignment expression cannot be a constant
```

ただし、以下に示すように、オブジェクト内部のプロパティを変更することは可能です。

```typescript
const foo = { bar: 123 };
foo.bar = 456; // Allowed!
console.log(foo); // { bar: 456 }
```

## できるだけ const にしよう

後で変数の初期化を行ったり、再代入する予定が無いのであれば `const` を使いましょう\(再代入する場合は `let` を使います\)。

