## Emitter
TypeScriptコンパイラには、2つの`emitter`が用意されています。

* `emitter.ts`：これはあなたが最も興味を持っているEmitterです。これがそのTS->JavaScript Emitterです。
* `declarationEmitter.ts`：これは*TypeScriptソースファイル*(`.ts`ファイル)の*宣言ファイル*(`.d.ts`)を生成するために使用されるEmitterです。

このセクションでは`emitter.ts`を見ていきます。

### Programによる使用法
Programは`emit`関数を提供します。この関数は主に`emitter.ts`の`emitFiles`関数にデリゲートします。コールスタックは次のとおりです:

```
Program.emit ->
    `emitWorker` (local in program.ts createProgram) ->
        `emitFiles` (function in emitter.ts)
```
`emitWorker`がEmitterに(`emitFiles`への引数を介して)提供するものの1つは`EmitResolver`です。`EmitResolver`はProgramのTypeCheckerによって提供され、基本的に`createChecker`のローカル関数のサブセットです。
