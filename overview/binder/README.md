# Binder

ほとんどのJavaScriptトランスパイラはTypeScriptよりもシンプルです。コード解析の方法がほとんどないためです。典型的なJavaScriptのトランスパイラは、次のようなフローしかありません：

```typescript
SourceCode ~~Scanner~~> Tokens ~~Parser~~> AST ~~Emitter~~> JavaScript
```

上記のアーキテクチャーはTypeScriptのJS生成の単純化された理解と同じですが、TypeScriptの主な特徴は_Semantic_システムです。型チェック\(`checker`によって実行される\)を助けるために、`binder`\(`binder.ts`\)は、ソースコードの様々な部分を正しい型システムに接続するために使用されます。そして、`checker`により使用されます。`binder`の主な役目はSymbolの作成です。

## Symbol

シンボルは、AST内の宣言ノードを、同じエンティティに寄与する他の宣言に接続します。Symbolは、セマンティックシステムの基本的な建設部材です。Symbolコンストラクタは `core.ts`で定義されています\(そして`binder`は実際に`objectAllocator.getSymbolConstructor`を使ってそれを手に入れます\)。以下はSymbolコンストラクタです：

```typescript
function Symbol(flags: SymbolFlags, name: string) {
    this.flags = flags;
    this.name = name;
    this.declarations = undefined;
}
```

`SymbolFlags`はフラグ列挙型であり、Symbolの更なる分類を識別するために本当に使用されます\(例えば変数スコープフラグ`FunctionScopedVariable`や `BlockScopedVariable`など\)

## Checkerによる使用法

`binder`は実際に`checker`型で内部的に使用され、`checker`は`program`によって使用されます。単純化したコールスタックは次のようになります。

```text
program.getTypeChecker ->
    ts.createTypeChecker (in checker)->
        initializeTypeChecker (in checker) ->
            for each SourceFile `ts.bindSourceFile` (in binder)
            // followed by
            for each SourceFile `ts.mergeSymbolTable` (in checker)
```

binderの作業単位はSourceFileです。`binder.ts`は`checker.ts`によって駆動されます。

