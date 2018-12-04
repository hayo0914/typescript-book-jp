## バインダー
ほとんどのJavaScriptトランスパイラは、コード解析の方法がほとんどないため、TypeScriptよりもシンプルです。典型的なJavaScriptのトランスパイライザーは、次のような流れしかありません：

```ts
SourceCode ~~Scanner~~> Tokens ~~Parser~~> AST ~~Emitter~~> JavaScript
```

上記のアーキテクチャーはTypeScript js世代の単純化された理解として真実ですが、TypeScriptの主な特徴は* Semantic *システムです。 （ `checker 'によって実行される）型チェックを助けるために、バインダ`（binder.ts内）は、ソースコードの様々な部分をコヒーレント型システムに接続するために使用されます。 `チェッカー`バインダーの主な責任は_Symbols_を作成することです。

### シンボル
シンボルは、AST内の宣言ノードを、同じエンティティに寄与する他の宣言に接続します。シンボルは、セマンティックシステムの基本的なビルディングブロックです。シンボルコンストラクタは `core.ts`で定義されています（そして`バインダ `は実際に`objectAllocator.getSymbolConstructor`を使ってそれを手に入れます）。以下はシンボルコンストラクタです：

```ts
function Symbol(flags: SymbolFlags, name: string) {
    this.flags = flags;
    this.name = name;
    this.declarations = undefined;
}
```

`SymbolFlags`はフラグ列挙型であり、シンボルの追加の分類を識別するために実際に使用されます（例えば、可変スコープフラグ`FunctionScopedVariable`や `BlockScopedVariable`など）

### Checkerによる使用法
`バインダー`は実際に `checker`型で内部的に使用され、`プログラム `によって使用されます。単純化されたコールスタックは次のようになります。
```
program.getTypeChecker ->
    ts.createTypeChecker (in checker)->
        initializeTypeChecker (in checker) ->
            for each SourceFile `ts.bindSourceFile` (in binder)
            // followed by
            for each SourceFile `ts.mergeSymbolTable` (in checker)
```
バインダーの作業単位はSourceFileです。 `binder.ts`は`checker.ts`によって駆動されます。
