# const

`const`はES6/TypeScriptで提供された非常に素晴らしい機能です。変数を**イミュータブル**\(immutable\)、つまり**不変**にすることができます。これは、可読性の面だけでなく実行時の面でも優れています。 constを使うには、単に`var`の代わりに`const`を使うだけです:

```typescript
const foo = 123;
```

> この構文は、`let constant foo`すなわち変数+動作指定子のようなものを入力させる他の言語よりも、ずっと優れています\(個人的な意見です\)。

`const`を使うことは、可読性とメンテナンス性のどちらの面でも良いことです。そして、マジックリテラル（謎の定数、マジックナンバーとも呼びます）を使うことを避けることができます。

```typescript
// 可読性が低いコードです
if (x > 10) {
}

// このほうがベターです
const maxRows = 10;
if (x > maxRows) {
}
```

## const宣言は初期化する必要があります

以下はコンパイルエラーになります：

```typescript
const foo; // ERROR: constの宣言は値を初期化する必要があります
```

## 代入の左辺に定数は置けない

作成された定数はイミュータブル（不変）です。したがって、新しい値を代入しようとするとコンパイルエラーになります：

```typescript
const foo = 123;
foo = 456; // ERROR: 代入の左側に定数を置くことはできません
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

