### ASTのヒント：SyntaxKind

`SyntaxKind`は`const enum`として定義されています。ここではサンプルです：

```ts
export const enum SyntaxKind {
    Unknown,
    EndOfFileToken,
    SingleLineCommentTrivia,
    // ... LOTS more
```

* インライン展開*（例えば、 `ts.SyntaxKind.EndOfFileToken`が`1`になるように） `const enum`（コンセプト[前に説明した概念（../ enums.md））です。 ASTを扱う際の逆参照コスト。しかしコンパイラは `--preserveConstEnums`コンパイラフラグでコンパイルされるので、enum *は実行時にも利用可能です*。 JavaScriptでは、必要に応じて `ts.SyntaxKind.EndOfFileToken`を使用できます。さらに、これらの列挙型メンバを変換して、次の関数を使用して文字列を表示することもできます。

```ts
export function syntaxKindToName(kind: ts.SyntaxKind) {
    return (<any>ts).SyntaxKind[kind];
}
```
