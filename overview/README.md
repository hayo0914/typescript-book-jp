# TypeScript コンパイラの内側

TypeScriptコンパイラのソースは、[`src/compiler`](https://github.com/Microsoft/TypeScript/tree/master/src/compiler)フォルダの下にあります。

それは以下の主要な部分に分割されます：

* Scanner\(`scanner.ts`\)
* Parser\(`parser.ts`\)
* Binder\(`binder.ts`\)
* checker\(`checker.ts`\)
* emitter\(`emitter.ts`\)

これらのそれぞれは、ソース内で独自のファイルを取得します。これらの部分については、この章の後半で説明します。

## BYOTS

私たちは、[Bring Your Own TypeScript\(BYOTS\)](https://github.com/basarat/byots)というプロジェクトを持っています。これは内部APIを公開する等によって、コンパイラのAPIを使って遊びやすくしています。あなたはこれを使用して、ローカルアプリケーションのTypeScriptのバージョンをグローバルに公開することができます。

## シンタックスとセマンティクスの違い

_文法_\(シンタックス\)が正しいものが_意味_\(セマンティクス\)が正しいことを意味するわけではありません。以下のTypeScriptコードを考えてみましょう。文法は有効ですが、意味は間違っています:

```typescript
var foo: number = "not a number";
```

`Semantic`は英語で「意味」を意味します。このコンセプトが頭の中にあると便利です。

## 処理の概要\(Processing Overview\)

以下は、TypeScriptコンパイラのこれらの主要部分の構成の概要です。

```text
SourceCode ~~ scanner ~~> Token Stream
```

```text
Token Stream ~~ parser ~~> AST
```

```text
AST ~~ binder ~~> Symbols
```

`Symbol`はTypeScript _semantic_システムの主要な建設部材です。示されているように、シンボルはバインディングの結果として作成されます。シンボルは、AST内の宣言ノードを、同じエンティティに寄与する他の宣言に接続します。

Symbols + ASTは、ソースコードの意味\(セマンティクス\)を検証するためにチェッカーが使用するものです

```text
AST + Symbols ~~ checker ~~> Type Validation
```

最後にJS出力が要求されたとき：

```text
AST + Checker ~~ emitter ~~> JS
```

TypeScriptコンパイラには、これらの主要部分にユーティリティを提供するいくつかのファイルがあります。次で説明します。

## File: Utilities

`core.ts`：TypeScriptコンパイラが使うコアユーティリティ。いくつか重要なもの：

* `let objectAllocator: ObjectAllocator`：シングルトンのグローバルとして定義された変数です。それは、`getNodeConstructor`\(Nodeは`parser`/`AST`を見るときに扱います\)、`getSymbolConstructor`\(シンボルは`binder`のときに扱います\)、`getTypeConstructor`\(型は`checker`で扱います\)、 `getSignatureConstructor`\(シグネチャはインデックス、シグネチャの呼び出しと構成物です\)。

## File： 主要なデータ構造

`types.ts`には、コンパイラ全体で使用される、主要なデータ構造とインターフェースがあります。いくつかの重要なサンプルの抜粋です：

* `SyntaxKind`

  ASTノードタイプは、`SyntaxKind`enumによって識別されます。

* `TypeChecker`

  TypeCheckerが提供するインターフェースです。

* `CompilerHost`

  これは`Program`が`System`と対話するために使用されます。

* `Node`

  ASTのノードです。

## File: System

`system.ts`です。TypeScriptコンパイラとオペレーティングシステムとのすべての対話は、`System`インターフェースを介して行われます。インターフェースとその実装\( `WScript`と`Node`\)は`system.ts`で定義されています。あなたはそれを_Operating Environment_\(OE\)として考えることができます。

主要なファイルの概要を知ったので、`Program`の概念を見ていきましょう。

