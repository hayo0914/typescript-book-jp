### Global Namespace Merging
`initializeTypeChecker`の中に次のコードがあります：

```ts
// Initialize global symbol table
forEach(host.getSourceFiles(), file => {
    if (!isExternalModule(file)) {
        mergeSymbolTable(globals, file.locals);
    }
});
```

これは基本的にすべての`global`Symbolを`let globals：SymbolTable = {};`(`createTypeChecker`にあります)SymbolTableにマージします。`mergeSymbolTable`は主に`mergeSymbol`を呼び出します。
