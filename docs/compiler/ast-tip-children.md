### ASTのヒント：子供の訪問

ユーティリティ関数 `ts.forEachChild`があり、ASTの任意のノードのすべての子ノードを参照することができます。

以下はソースコードの簡単なスニペットです。

```ts

export function forEachChild<T>(node: Node, cbNode: (node: Node) => T, cbNodeArray?: (nodes: Node[]) => T): T {
        if (!node) {
            return;
        }
        switch (node.kind) {
            case SyntaxKind.BinaryExpression:
                return visitNode(cbNode, (<BinaryExpression>node).left) ||
                    visitNode(cbNode, (<BinaryExpression>node).operatorToken) ||
                    visitNode(cbNode, (<BinaryExpression>node).right);
            case SyntaxKind.IfStatement:
                return visitNode(cbNode, (<IfStatement>node).expression) ||
                    visitNode(cbNode, (<IfStatement>node).thenStatement) ||
                    visitNode(cbNode, (<IfStatement>node).elseStatement);

            // .... lots more
```

基本的に `node.kind`をチェックし、それに基づいて`node`が提供するインターフェースを仮定し、子に対して `cbNode`を呼び出します。ただし、この関数は* all *子（例えばSyntaxKind.SemicolonToken）に対して `visitNode`を呼び出さないことに注意してください。 * AST内のノードの子が* all *を望むのであれば、 `Node`の`.getChildren`メンバ関数を呼び出すだけです。

例えば。ここにはノードの冗長な `AST`を出力する関数があります：

```ts
function printAllChildren(node: ts.Node, depth = 0) {
    console.log(new Array(depth+1).join('----'), ts.syntaxKindToName(node.kind), node.pos, node.end);
    depth++;
    node.getChildren().forEach(c=> printAllChildren(c, depth));
}
```

この関数のサンプル使用法については、パーサーについてさらに説明します。
