### パーサー関数

前述のように `parseSourceFile`は初期状態を設定し、`parseSourceFileWorker`関数に渡します。

#### `parseSourceFileWorker`

`SourceFile`ASTノードを作成します。次に、 `parseStatements`関数から始まるソースコードを解析します。それが返ってくると、 `nodeFount`、`identifierCount`などの追加情報を含む `SourceFile`ノードを完成させます。

#### `parseStatements`
最も重要な `parseFoo`スタイル関数の1つです(次のコンセプト)。これは、スキャナから返された現在のトークンによって切り替えられます。例えば。現在のトークンが `SemicolonToken`であれば`parseEmptyStatement`を呼び出して空文のASTノードを作成します。

### ノードの作成

パーサには、 `Foo`ノードを生成する本体を持つ`parserFoo`関数がたくさんあります。これらは一般的に `Foo`ノードが期待される時点で(他のパーサー関数から)呼び出されます。このプロセスの典型的なサンプルは、 `;;;;;;のような空文を解析するために使われる`parseEmptyStatement() `関数です。ここには、その全体の機能があります

```ts
function parseEmptyStatement(): Statement {
    let node = <Statement>createNode(SyntaxKind.EmptyStatement);
    parseExpected(SyntaxKind.SemicolonToken);
    return finishNode(node);
}
```

これは、3つの重要な関数 `createNode`、`parseExpected`と `finishNode`を示しています。

#### `createNode`
パーサの `createNode`関数`function createNode(kind：SyntaxKind、pos ?: number)：Node`はノードの作成、渡されたときの `SyntaxKind`の設定、渡された場合の初期位置の設定を行います現在のスキャナ状態からの位置)。

#### `parseExpected`
パーサーの `parseExpected`関数`function parseExpected(kind：SyntaxKind、diagnosticMessage ?: DiagnosticMessage)：boolean`は、パーサ状態の現在のトークンが目的の `SyntaxKind`と一致することをチェックします。そうでなければ、送られた `diagnosticMessage`を報告するか、`foo expected`の形式の一般的なものを作成します。これは内部的に `parseErrorAtPosition`関数(走査位置を使用します)を使用して良いエラー報告を行います。

### `finishNode`
パーサーの `finishNode`関数`function finishNode <T extends Node>(node：T、end ?:: number)：T`はノードの `end`位置を設定し、`parserContextFlags`のようにこのノードを解析する前にエラーがあった場合(インクリメンタル解析でこのASTノードを再利用できない場合)
