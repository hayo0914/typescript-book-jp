# コンパイラ
typescriptコンパイラのソースは、[`src / compiler`](https://github.com/Microsoft/TypeScript/tree/master/src/compiler)フォルダの下にあります。

それは以下の主要な部分に分割されます：
* スキャナ( `scanner.ts`)
* パーサー( `parser.ts`)
* バインダー( `バインダー.ts`)
* チェッカー( `checker.ts`)
* エミッタ( `emitter.ts`)

これらのそれぞれは、ソース内で独自のファイルを取得します。これらの部分については、この章の後半で説明します。

## バイツ
私たちは、[Bring Your Own TypeScript(BYOTS)]というプロジェクト(https://github.com/basarat/byots)を持っています。内部APIを公開することによってこれを使用して、ローカルアプリケーションのTypeScriptのバージョンをグローバルに公開することができます。

## シンタックスとセマンティクス
文法的に正しいものが*意味的*正しいことを意味するわけではありません。以下のTypeScriptコードを考えてみましょう。*構文的には有効ですが*意味的には*間違っています

```ts
var foo: number = "not a number";
```

「セマンティック」は英語で「意味」を意味します。このコンセプトはあなたの頭の中にあると便利です。

## 処理の概要
以下は、TypeScriptコンパイラのこれらの主要部分がどのように構成されているかを簡単に見直したものです。

```code
SourceCode ~~ scanner ~~> Token Stream
```

```code
Token Stream ~~ parser ~~> AST
```

```code
AST ~~ binder ~~> Symbols
```
`Symbol`はTypeScript * semantic *システムの主要ビルディングブロックです。示されているように、シンボルはバインディングの結果として作成されます。シンボルは、AST内の宣言ノードを、同じエンティティに寄与する他の宣言に接続します。

Symbols + ASTは、ソースコードを意味的に*検証するためにチェッカーが使用するものです
```code
AST + Symbols ~~ checker ~~> Type Validation
```

最後にJS出力が要求されたとき：
```code
AST + Checker ~~ emitter ~~> JS
```

TypeScriptコンパイラには、次に説明するキー部分の多くにユーティリティを提供するいくつかの追加ファイルがあります。

## ファイル：ユーティリティ
`core.ts`：TypeScriptコンパイラが使うコアユーティリティ。いくつか重要なもの：

* `let objectAllocator：ObjectAllocator`：シングルトングローバルとして定義された変数です。 `getSymbolConstructor`(シンボルは`binder`でカバーされています)、 `getTypeConstructor`(型は`checker`で扱います)、 `getNodeConstructor`(ノードは`parser` / `AST`を見るとカバーされます)、`getSymbolConstructor` 、 `getSignatureConstructor`(シグネチャはインデックス、コール、シグネチャを構成します)。

## ファイル：主要なデータ構造
`types.ts`には、主要なデータ構造とインタフェースがコンパイラ全体で使用されます。いくつかの重要なサンプルの抜粋です：
* `SyntaxKind`
ASTノードタイプは、 `SyntaxKind` enumによって識別されます。
* `TypeChecker`
TypeCheckerが提供するインターフェイスです。
* `CompilerHost`
これは `Program`が`System`と対話するために使用します。
* `Node`
ASTノード。

## ファイルシステム
`system.ts`です。 TypeScriptコンパイラとオペレーティングシステムとのすべての対話は、 `System`インタフェースを介して行われます。インターフェースとその実装( `WScript`と`Node`)は `system.ts`で定義されています。あなたは* Operating Environment *(OE)と考えることができます。

主要なファイルの概要を知ったので、 `Program`の概念を見ることができます
