### 変数(Variables)
例えば、[`process`変数](https://nodejs.org/api/process.html)についてTypeScriptに伝える場合：

```ts
declare var process: any;
```

> すでに [コミュニティ](https://github.com/DefinitelyTyped/DefinitelyTyped/blob/master/types/node/index.d.ts) が`node.d.ts`をメンテナンスしているので、`process`のためにこれを行う必要はありません。

これにより、TypeScriptのエラーが発生することなく`process`変数を使うことができます：

```ts
process.exit();
```

可能な限りインターフェースを使用することをおすすめします。例：

```ts
interface Process {
    exit(code?: number): void;
}
declare var process: Process;
```

これにより、他の人がこれらのグローバル変数を拡張し、その変更についてTypeScriptに伝えることができます。例えば余興にexitWithLogging関数を追加する次のような場合を考えてみましょう。

```ts
interface Process {
    exitWithLogging(code?: number): void;
}
process.exitWithLogging = function() {
    console.log("exiting");
    process.exit.apply(process, arguments);
};
```

次はインターフェースを少し詳しく見ていきましょう。
