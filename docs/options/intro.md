# 便利さと健全性(Convenience vs. Soundness)

TypeScriptはデフォルトでいくつかのことをできないようにしています。例えば、宣言されていない変数を使用することです(もちろん、外部システムには*宣言ファイル*を使用できます)。

つまり、伝統的にプログラミング言語は、型システムによって許可されているものと許可されていないものとの間に厳しい境界を持っています。TypeScriptは、スライダーをどこに置くかを制御できる点で異なります。これは本当にあなたが知っているJavaScriptを**あなたが**望むような安全性で使用できるようにすることです。このスライダを正確に制御するためのコンパイラオプションがたくさんあるので、見てみましょう。

## ブール値のオプション(Boolean Options)

`boolean`である`compilerOptions`は`tsconfig.json`で`compilerOptions`として指定できます：

```json
{
    "compilerOptions": {
        "someBooleanOption": true
    }
}
```

またはコマンドラインで

```sh
tsc --someBooleanOption
```

> これらはすべてデフォルトでは`false`です。

[ここ](https://www.typescriptlang.org/docs/handbook/compiler-options.html)をクリックすると、すべてのコンパイラオプションが表示されます。
