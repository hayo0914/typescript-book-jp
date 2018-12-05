# `@ types`

[Definitely Typed](https://github.com/DefinitelyTyped/DefinitelyTyped)は、間違いなくTypeScriptの最大の強みの1つです。コミュニティは効果的に先に進んで**トップJavaScriptプロジェクトのほぼ90％の性質を文書化**しました。

これは、これらのプロジェクトを非常にインタラクティブかつ探索的な方法で使用できることを意味します。ドキュメントを別のウィンドウで開き、誤植をしないようにする必要はありません。

## `@ types`を使う

インストールは `npm`の上で動作するのでかなり簡単です。例として、 `jquery`の型定義を以下のように単純にインストールすることができます：

```
npm install @types/jquery --save-dev
```

`@ types`は* global *と* module *型定義の両方をサポートします。


### グローバル `@ types`

デフォルトでは、グローバル消費をサポートする定義は自動的に含まれます。例えば。 `jquery`のためには、あなたのプロジェクトで`$ `*をグローバルに*使うことができるはずです。

しかし、*ライブラリ*( `jquery`のような)では、一般的に* modules *の使用をお勧めします：

### モジュール `@ types`

インストール後、実際に特別な設定は必要ありません。モジュールのように使用するだけです(例：

```ts
import * as $ from "jquery";

// Use $ at will in this module :)
```

## グローバルの制御

わかるように、グローバルなリークインを自動的に許可する定義を持つことは、一部のチームにとっては問題になる可能性があります。したがって、 `tsconfig.json``compilerOptions.types`を使って意味を持つ型だけを明示的に取り込むように選択することができます：

```json
{
    "compilerOptions": {
        "types" : [
            "jquery"
        ]
    }
}
```

上の例は、 `jquery`だけを使用できるサンプルを示しています。人が `npm install @ types / node`のような別の定義をインストールしても、そのグローバル(例：[`process`](https://nodejs.org/api/process.html))はあなたが追加するまであなたのコードに漏れませんそれらを `tsconfig.json`型オプションに渡します。
