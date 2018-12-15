## Checker
以前に述べたように*checker*は、TypeScriptを他のJavaScriptトランスパイラよりもユニークに強力にするものです。Checkerは`checker.ts`にあり、この時点ではTypeScriptの23k+行(コンパイラの最大部分)です。

### Programによる使用方法
`checker`は`program`により初期化されます。以下はコールスタックのサンプルです(`binder`で見たものと同じです)：

```
program.getTypeChecker ->
    ts.createTypeChecker (in checker)->
        initializeTypeChecker (in checker) ->
            for each SourceFile `ts.bindSourceFile` (in binder)
            // followed by
            for each SourceFile `ts.mergeSymbolTable` (in checker)
```

### Emitterとの関連付け
`getDiagnostics`が呼び出されると、本当の型チェックが行われます。この機能は、例えば、`Program.emit`が一度要求されると、Checkerは`EmitResolver`を返します(ProgramはCheckerの`getEmitResolver`関数を呼び出します)。これは単に`createTypeChecker`のローカル関数の集合です。Emitterを見るときにこれについて再び言及します。

`checkSourceFile`(`createTypeChecker`のローカル関数)の下のコールスタックは以下の通りです。

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
