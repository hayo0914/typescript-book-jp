### AST Tip：SyntaxKind

`SyntaxKind`は`const enum`として定義されています。これはサンプルです：

```ts
export const enum SyntaxKind {
    Unknown,
    EndOfFileToken,
    SingleLineCommentTrivia,
    // ... LOTS more
```

それは*インライン展開*(例えば`ts.SyntaxKind.EndOfFileToken`が`1`になる)されるための`const enum`([前に説明した概念](../enums.md))です。それにより、ASTを扱う際に、デリファレンスするコストが発生しません。しかしコンパイラは`--preserveConstEnums`コンパイラフラグでコンパイルされるので、enumは実行時にも利用可能です。なので、JavaScriptでは、必要に応じて`ts.SyntaxKind.EndOfFileToken`を使用できます。さらに、次の関数を使用してこれらの列挙型メンバを変換し、文字列を表示することもできます。

```ts
export function syntaxKindToName(kind: ts.SyntaxKind) {
    return (<any>ts).SyntaxKind[kind];
}
```
