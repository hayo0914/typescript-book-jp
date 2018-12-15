### Parser Functions

前述のように`parseSourceFile`は初期状態をセットアップし、それを`parseSourceFileWorker`関数に渡します。

#### `parseSourceFileWorker`

最初に`SourceFile`ASTノードを作成します。次に、`parseStatements`関数から始まるソースコードを解析します。それが返ってくると、`nodeCount`、`identifierCount`などの追加情報を含む`SourceFile`ノードを完成させます。

#### `parseStatements`
最も重要な`parseFoo`スタイルの関数の1つです(次に説明する概念です)。これは、Scannerから返された現在の`token`によって切り替えられます。例えば現在のトークンが `SemicolonToken`であれば`parseEmptyStatement`を呼び出して空文のASTノードを作成します。

### Nodeの作成

パーサには、`Foo`ノードを生成する`parserFoo`関数がたくさんあります。これらは一般的に`Foo`Nodeが期待される時点で(他のParser関数から)呼び出されます。このプロセスの典型的なサンプルは、`;;;;;;`のような空文をパースするために使われる`parseEmptyStatement()`関数です。以下にその関数の全体があります:

```ts
function parseEmptyStatement(): Statement {
    let node = <Statement>createNode(SyntaxKind.EmptyStatement);
    parseExpected(SyntaxKind.SemicolonToken);
    return finishNode(node);
}
```

これは、3つの重要な関数`createNode`、`parseExpected`と`finishNode`を示しています。

#### `createNode`
Parserの`createNode`関数`function createNode(kind：SyntaxKind、pos ?: number)：Node`はノードの作成、渡されたときの`SyntaxKind`のセットアップ、渡された場合の初期位置の設定(または、現在のスキャナの位置を使います)を行います。

#### `parseExpected`
Parserの`parseExpected`関数`function parseExpected(kind：SyntaxKind、diagnosticMessage ?: DiagnosticMessage)：boolean`は、Parserの状態に含まれる現在のトークンが目的の`SyntaxKind`と一致することをチェックします。そうでなければ、送られた`diagnosticMessage`を報告するか、`foo expected`の形式の一般的なものを作成します。これは内部的に`parseErrorAtPosition`関数(スキャン位置を使用します)を使用して良いエラー報告を行います。

### `finishNode`
Parserの`finishNode`関数`function finishNode <T extends Node>(node：T、end ?:: number)：T`はNodeの`end`位置や、`parserContextFlags`のように便利なモノを設定します。これは、このNodeを解析する前にエラーがあったとしても、同じようにパースされます(その場合、インクリメンタルパーシングでこのASTノードを再利用できません)。
