## チェッカー
以前に述べたように* checker *は、TypeScriptを他のJavaScriptトランスファーよりもユニークに強力にするものです。チェッカーは `checker.ts 'にあり、この時点ではTypeScriptの23k +行（コンパイラの最大部分）です。

### プログラムによる使用
`checker`は`program`で初期化されます。以下はコールスタックのサンプルです（ `バインダー`を見ると同じものを示しています）：

```
program.getTypeChecker ->
    ts.createTypeChecker (in checker)->
        initializeTypeChecker (in checker) ->
            for each SourceFile `ts.bindSourceFile` (in binder)
            // followed by
            for each SourceFile `ts.mergeSymbolTable` (in checker)
```

### エミッタとの関連
`getDiagnostics`が呼び出されると、真の型チェックが行われます。この機能は、例えば、 `Program.emit`が要求されると、チェッカーは`EmitResolver`（プログラムはチェッカー `getEmitResolver`関数を呼び出します）を返します。これは`createTypeChecker`のローカル関数の集合です。エミッタを見ると再びこれについて言及します。

ここでコールスタックは `checkSourceFile`（`createTypeChecker`のローカル関数）です。

```
program.emit ->
    emitWorker (program local) ->
        createTypeChecker.getEmitResolver ->
            // First call the following functions local to createTypeChecker
            call getDiagnostics ->
                getDiagnosticsWorker ->
                    checkSourceFile

            // then
            return resolver
            (already initialized in createTypeChecker using a call to local createResolver())
```
