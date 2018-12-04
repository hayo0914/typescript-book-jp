## パーサー
TypeScriptパーサーのソースコードは完全に `parser.ts`にあります。スキャナはソースコードをASTに変換するために `Parser`によって内部的に*制御されます。ここでは、望ましい結果が何であるかのレビューです。

```
SourceCode ~~ scanner ~~> Token Stream ~~ parser ~~> AST
```

パーサーはシングルトンとして実装されています（ `scanner`と同様の理由、再作成が可能な場合は再作成したくありません）。実際には、Parserのための* state *変数とシングルトン `scanner`を含む`namespace Parser`として実装されています。前に述べたように、 `const scanner`を含んでいます。パーサ関数はこのスキャナを管理します。

### プログラムによる使用
パーサーはプログラムによって間接的に駆動されます（間接的に、実際には前述の `CompilerHost`によって実際に実行されます）。基本的にこれは単純化されたコールスタックです：

```
Program ->
    CompilerHost.getSourceFile ->
        (global function parser.ts).createSourceFile ->
            Parser.parseSourceFile
```

`parseSourceFile`は、Parserの状態を準備するだけでなく、`initializeState`を呼び出すことによって `scanner`の状態を準備します。その後、 `parseSourceFileWorker`を使ってソースファイルを解析します。

### サンプルの使用法
パーザ内部を深く掘り下げる前に、（ts.createSourceFile`を使用して）ソースファイルのASTを取得するためにTypeScriptのパーサを使用するサンプルコードを次に示します。

`code / compiler / parser / runParser.ts`
```ts
import * as ts from "ntypescript";

function printAllChildren(node: ts.Node, depth = 0) {
    console.log(new Array(depth + 1).join('----'), ts.formatSyntaxKind(node.kind), node.pos, node.end);
    depth++;
    node.getChildren().forEach(c=> printAllChildren(c, depth));
}

var sourceCode = `
var foo = 123;
`.trim();

var sourceFile = ts.createSourceFile('foo.ts', sourceCode, ts.ScriptTarget.ES5, true);
printAllChildren(sourceFile);
```

これは以下を出力します：

```ts
SourceFile 0 14
---- SyntaxList 0 14
-------- VariableStatement 0 14
------------ VariableDeclarationList 0 13
---------------- VarKeyword 0 3
---------------- SyntaxList 3 13
-------------------- VariableDeclaration 3 13
------------------------ Identifier 3 7
------------------------ FirstAssignment 7 9
------------------------ FirstLiteralToken 9 13
------------ SemicolonToken 13 14
---- EndOfFileToken 14 14
```
あなたの頭を左に傾けると、これは非常に右側の木のように見えます。
