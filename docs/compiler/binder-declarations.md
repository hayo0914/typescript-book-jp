### シンボルと宣言
`node`と`symbol`の間のリンクは、いくつかの関数によって実行されます。ソースファイルSymbol(外部モジュールの場合)に `SourceFile`ノードをバインドするために使われる一つの関数は`addDeclarationToSymbol`関数です

注：外部モジュールソースファイルの `Symbol`は`flags：SymbolFlags.ValueModule`と `name： '"' + removeFileExtension(file.fileName)+ '"` `)として設定されています。

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

重要な連結部分：
* ASTノード( `node.symbol`)からシンボルへのリンクを作成します。
* シンボルをシンボルの宣言の1つ*に追加します( `symbol.declarations`)。

#### 宣言
宣言はオプションの名前を持つ `node`です。 `types.ts`では

```ts
interface Declaration extends Node {
    _declarationBrand: any;
    name?: DeclarationName;
}
```
