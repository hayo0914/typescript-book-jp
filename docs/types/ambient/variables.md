### 変数
例えば、あなたができる* [`process`変数](https://nodejs.org/api/process.html)についてTypeScriptに伝えるために：

```ts
declare var process: any;
```

> すでに `コミュニティが`node.d.ts`を維持しているので、 `process`のためにこれを行う必要はありません(https://github.com/DefinitelyTyped/DefinitelyTyped/blob/master/types/ノード/ index.d.ts)。

これにより、TypeScriptを使わずに `process`変数を使うことができます：

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

これにより、他の人がこれらのグローバル変数の性質を拡張して、そのような変更についてTypeScriptに伝えることができます。例えば。アミューズメントを処理するためのexitWithLogging関数を追加する次のような場合を考えてみましょう。

```ts
interface Process {
    exitWithLogging(code?: number): void;
}
process.exitWithLogging = function() {
    console.log("exiting");
    process.exit.apply(process, arguments);
};
```

次はインターフェイスを少し詳しく見ていきましょう。
