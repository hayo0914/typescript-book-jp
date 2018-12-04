### SymbolTable

SymbolTableは単純なHashMapとして実装されています。ここにインターフェイスがあります（ `types.ts`）：

```ts
interface SymbolTable {
    [index: string]: Symbol;
}
```

シンボルテーブルはバインディングで初期化されます。コンパイラで使用されるいくつかのSymbolTableがあります：

`Node`について：
```ts
locals?: SymbolTable;                   // Locals associated with node
```

`Symbol`について：

```ts
members?: SymbolTable;                  // Class, interface or literal instance members
exports?: SymbolTable;                  // Module exports
```

注： `ContainerFlags`に基づいて`bindChildren`によって `locals`が（{}}に）初期化されているのを見ました。

#### シンボルテーブルの人口
SymbolTablesは主に `declareSymbol`の呼び出しによって`Symbols`で埋められます。この機能の全体を以下に示す：

```ts
/**
 * Declares a Symbol for the node and adds it to symbols. Reports errors for conflicting identifier names.
 * @param symbolTable - The symbol table which node will be added to.
 * @param parent - node's parent declaration.
 * @param node - The declaration to be added to the symbol table
 * @param includes - The SymbolFlags that node has in addition to its declaration type (eg: export, ambient, etc.)
 * @param excludes - The flags which node cannot be declared alongside in a symbol table. Used to report forbidden declarations.
 */
function declareSymbol(symbolTable: SymbolTable, parent: Symbol, node: Declaration, includes: SymbolFlags, excludes: SymbolFlags): Symbol {
    Debug.assert(!hasDynamicName(node));

    // The exported symbol for an export default function/class node is always named "default"
    let name = node.flags & NodeFlags.Default && parent ? "default" : getDeclarationName(node);

    let symbol: Symbol;
    if (name !== undefined) {

        // Check and see if the symbol table already has a symbol with this name.  If not,
        // create a new symbol with this name and add it to the table.  Note that we don't
        // give the new symbol any flags *yet*.  This ensures that it will not conflict
        // with the 'excludes' flags we pass in.
        //
        // If we do get an existing symbol, see if it conflicts with the new symbol we're
        // creating.  For example, a 'var' symbol and a 'class' symbol will conflict within
        // the same symbol table.  If we have a conflict, report the issue on each
        // declaration we have for this symbol, and then create a new symbol for this
        // declaration.
        //
        // If we created a new symbol, either because we didn't have a symbol with this name
        // in the symbol table, or we conflicted with an existing symbol, then just add this
        // node as the sole declaration of the new symbol.
        //
        // Otherwise, we'll be merging into a compatible existing symbol (for example when
        // you have multiple 'vars' with the same name in the same container).  In this case
        // just add this node into the declarations list of the symbol.
        symbol = hasProperty(symbolTable, name)
            ? symbolTable[name]
            : (symbolTable[name] = createSymbol(SymbolFlags.None, name));

        if (name && (includes & SymbolFlags.Classifiable)) {
            classifiableNames[name] = name;
        }

        if (symbol.flags & excludes) {
            if (node.name) {
                node.name.parent = node;
            }

            // Report errors every position with duplicate declaration
            // Report errors on previous encountered declarations
            let message = symbol.flags & SymbolFlags.BlockScopedVariable
                ? Diagnostics.Cannot_redeclare_block_scoped_variable_0
                : Diagnostics.Duplicate_identifier_0;
            forEach(symbol.declarations, declaration => {
                file.bindDiagnostics.push(createDiagnosticForNode(declaration.name || declaration, message, getDisplayName(declaration)));
            });
            file.bindDiagnostics.push(createDiagnosticForNode(node.name || node, message, getDisplayName(node)));

            symbol = createSymbol(SymbolFlags.None, name);
        }
    }
    else {
        symbol = createSymbol(SymbolFlags.None, "__missing");
    }

    addDeclarationToSymbol(symbol, node, includes);
    symbol.parent = parent;

    return symbol;
}
```

どのSymbolTableが実装されるかは、この関数の最初の引数によって決まります。例えば`SyntaxKind.ClassDeclaration`または`SyntaxKind.ClassExpression`の* container *に宣言を追加すると、 `declareClassMember`関数が呼び出され、次のコードを持ちます：

```ts
function declareClassMember(node: Declaration, symbolFlags: SymbolFlags, symbolExcludes: SymbolFlags) {
    return node.flags & NodeFlags.Static
        ? declareSymbol(container.symbol.exports, container.symbol, node, symbolFlags, symbolExcludes)
        : declareSymbol(container.symbol.members, container.symbol, node, symbolFlags, symbolExcludes);
}
```
