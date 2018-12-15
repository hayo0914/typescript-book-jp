### SymbolとDeclaration
`node`と`symbol`の間のリンクは、いくつかの関数によって実行されます。ある1つの関数は、`SourceFile`NodeをSource File Symbolにバインドするために使われます。それは、`addDeclarationToSymbol`関数です。

注：外部モジュールソースファイルの`Symbol`は`flags ： SymbolFlags.ValueModule`と`name： '"' + removeFileExtension(file.fileName) + '"'`)としてセットアップされています。

```ts
function addDeclarationToSymbol(symbol: Symbol, node: Declaration, symbolFlags: SymbolFlags) {
    symbol.flags |= symbolFlags;

    node.symbol = symbol;

    if (!symbol.declarations) {
        symbol.declarations = [];
    }
    symbol.declarations.push(node);

    if (symbolFlags & SymbolFlags.HasExports && !symbol.exports) {
        symbol.exports = {};
    }

    if (symbolFlags & SymbolFlags.HasMembers && !symbol.members) {
        symbol.members = {};
    }

    if (symbolFlags & SymbolFlags.Value && !symbol.valueDeclaration) {
        symbol.valueDeclaration = node;
    }
}
```

重要なリンクを行っている部分：
* AST node(`node.symbol`)からSymbolへのリンクを作成します。
* NodeをSymbolのDeclaration(`symbol.declarations`)の1つとして追加します。

#### Declaration
Declarationはオプションの名前を持つ`node`です。`types.ts`にあります:

```ts
interface Declaration extends Node {
    _declarationBrand: any;
    name?: DeclarationName;
}
```
