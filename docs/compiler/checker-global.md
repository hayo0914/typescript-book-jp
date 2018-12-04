### グローバル名前空間マージ
`initializeTypeChecker`の中に次のコードがあります：

```ts
// Initialize global symbol table
forEach(host.getSourceFiles(), file => {
    if (!isExternalModule(file)) {
        mergeSymbolTable(globals, file.locals);
    }
});
```

これは基本的にすべての `global`シンボルを`let globals：SymbolTable = {}; `（`createTypeChecker`内の）SymbolTableにマージします。 `mergeSymbolTable`は主に`mergeSymbol`を呼び出します。
