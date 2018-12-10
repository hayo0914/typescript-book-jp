# `@types`

[Definitely Typed](https://github.com/DefinitelyTyped/DefinitelyTyped) は、間違いなくTypeScriptの最大の強みの1つです。コミュニティは効率的に**トップJavaScriptプロジェクトのほぼ90％の型ドキュメント**を作成しました。

これは、これらのプロジェクトを非常にインタラクティブかつ探索的な方法で使用できることを意味します。ドキュメントを別のウィンドウで開き、タイポしないようにする必要はありません。

## `@types`を使う

インストールは `npm`の上で動作するのでかなり簡単です。例として、`jquery`の型定義を以下のように単純にインストールすることができます：

```
npm install @types/jquery --save-dev
```

`@types`はグローバルとモジュールの両方の型定義をサポートします。


### グローバル `@types`

デフォルトでは、グローバルに利用する定義は自動的にインクルードされます。例えば`jquery`のために、あなたのプロジェクトで`$`をグローバルに使うことができるはずです。

しかし、ライブラリ(`jquery`のような)では、一般的にモジュールの使用をお勧めします：

### モジュール `@types`

インストール後、実際に特別な設定は必要ありません。モジュールのように使用するだけです。例：

```ts
import * as $ from "jquery";

// Use $ at will in this module :)
```

## グローバルの制御

予想できるように、グローバルへの定義を自動的に許可する設定をすることは、一部のチームにとっては問題になる可能性があります。したがって`tsconfig.json`の`compilerOptions.types`を使って意味を持つ型だけを明示的に取り込むようにすることができます：

```json
{
    "compilerOptions": {
        "types" : [
            "jquery"
        ]
    }
}
```

上の例は、 `jquery`だけを使用できるサンプルを示しています。誰かが`npm install @types/node`のような別の定義をインストールしても、そのグローバル(例： [`process`](https://nodejs.org/api/process.html)) はあなたが`tsconfig.json`の`types`オプションに追加するまで、あなたのコードに流入しません。
