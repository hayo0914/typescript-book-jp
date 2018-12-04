## エミッタ
TypeScriptコンパイラには、2つの「エミッタ」が用意されています。

* `emitter.ts`：これはあなたが最も興味を持っているエミッタです。そのTS  - > JavaScriptエミッタです。
* `declarationEmitter.ts`：これは* TypeScriptソースファイル*（`.ts`ファイル）の*宣言ファイル*（ `.d.ts`）を生成するために使用されるエミッタです。

このセクションでは `emitter.ts`を見ていきます。

### プログラムによる使用法
プログラムは `emit`関数を提供します。この関数は主に `emitter.ts`の`emitFiles`関数に委譲します。コールスタックは次のとおりです。

```
Program.emit ->
    `emitWorker` (local in program.ts createProgram) ->
        `emitFiles` (function in emitter.ts)
```
`emitWorker`がエミッタに（emitFiles`への引数を介して）提供するものの1つは`EmitResolver`です。 `EmitResolver`はプログラムのTypeCheckerによって提供され、基本的に`createChecker`の* local *関数のサブセットです。
