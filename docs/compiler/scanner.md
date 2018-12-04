## スキャナ
TypeScriptスキャナのソースコードは、完全に `scanner.ts`にあります。スキャナはソースコードをASTに変換するために `Parser`によって内部的に*制御されます。ここでは、望ましい結果が何であるかです。

```
SourceCode ~~ scanner ~~> Token Stream ~~ parser ~~> AST
```

### パーサーによる使用法
スキャナーを何度も作成するコストを避けるために、 `parser.ts`に*シングルトン*`scanner`が作成されています。このスキャナは、 `initializeState`関数を使ってオンデマンドでパーサーによってプリムされます。

ここでは、このコンセプトを実証できるパーザー内の実際のコードの*シンプル*バージョンを示します：

`code / compiler / scanner / runScanner.ts`
```ts
import * as ts from "ntypescript";

// TypeScript has a singelton scanner
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

```
VarKeyword
Identifier
FirstAssignment
FirstLiteralToken
SemicolonToken
```

### スキャナの状態
`scan`を呼び出すと、スキャナはローカル状態（スキャン中の位置、現在のトークンの詳細など）を更新します。スキャナには、現在のスキャナの状態を取得するためのユーティリティ機能が用意されています。以下のサンプルでは、​​スキャナを作成し、それを使用してコード内のトークンとその位置を特定しています。

`code / compiler / scanner / runScannerWithPosition.ts`
```ts
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
```
VarKeyword 0 3
Identifier 3 7
FirstAssignment 7 9
FirstLiteralToken 9 13
SemicolonToken 13 14
```

### スタンドアロンスキャナ
typescriptパーサーはシングルトンスキャナーを持っていますが、 `createScanner`を使ってスタンドアロンスキャナーを作成し、`setText` / `setTextPos`を使って、アミューズメントのためにファイル内の異なる点をスキャンすることができます。
