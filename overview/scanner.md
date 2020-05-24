# Scanner

TypeScript Scannerのソースコードは、完全に`scanner.ts`にあります。ScannerはソースコードをASTに変換するために`Parser`によって内部的に制御されます。以下に示すのは、どんな結果が望まれるかです:

```text
SourceCode ~~ scanner ~~> Token Stream ~~ parser ~~> AST
```

## Parserによる使用法

Scannerを何度も作成するコストを避けるために、`parser.ts`にシングルトンの`scanner`が作成されています。このスキャナは、`initializeState`関数を使ってオンデマンドにParserによって準備されます。

ここでは、この概念を説明するParser内の実際のコードのシンプルバージョンを示します：

`code/compiler/scanner/runScanner.ts`

```typescript
import * as ts from "ntypescript";

// TypeScript has a singleton scanner
const scanner = ts.createScanner(ts.ScriptTarget.Latest, /*skipTrivia*/ true);

// That is initialized using a function `initializeState` similar to
function initializeState(text: string) {
    scanner.setText(text);
    scanner.setOnError((message: ts.DiagnosticMessage, length: number) => {
        console.error(message);
    });
    scanner.setScriptTarget(ts.ScriptTarget.ES5);
    scanner.setLanguageVariant(ts.LanguageVariant.Standard);
}

// Sample usage
initializeState(`
var foo = 123;
`.trim());

// Start the scanning
var token = scanner.scan();
while (token != ts.SyntaxKind.EndOfFileToken) {
    console.log(ts.formatSyntaxKind(token));
    token = scanner.scan();
}
```

これは以下を出力します：

```text
VarKeyword
Identifier
FirstAssignment
FirstLiteralToken
SemicolonToken
```

## スキャナの状態

`scan`を呼び出すと、スキャナはローカル状態\(スキャン中の位置、現在のトークンの詳細など\)を更新します。スキャナには、現在のスキャナの状態を取得するためのユーティリティ機能が用意されています。以下のサンプルでは、スキャナを作成し、それを使用してコード内のトークンとその位置を特定しています。

`code/compiler/scanner/runScannerWithPosition.ts`

```typescript
// Sample usage
initializeState(`
var foo = 123;
`.trim());

// Start the scanning
var token = scanner.scan();
while (token != ts.SyntaxKind.EndOfFileToken) {
    let currentToken = ts.formatSyntaxKind(token);
    let tokenStart = scanner.getStartPos();
    token = scanner.scan();
    let tokenEnd = scanner.getStartPos();
    console.log(currentToken, tokenStart, tokenEnd);
}
```

これは以下を出力します：

```text
VarKeyword 0 3
Identifier 3 7
FirstAssignment 7 9
FirstLiteralToken 9 13
SemicolonToken 13 14
```

## スタンドアロンScanner

TypeScript ParserはシングルトンのScannerを持っていますが、`createScanner`を使ってスタンドアロンScannerを作成し、`setText`/`setTextPos`を使って、一興のためにファイル内の異なる位置をスキャンすることができます。

