# @types パッケージ \(DefinitelyTyped\)

[Definitely Typed](https://github.com/DefinitelyTyped/DefinitelyTyped) は、間違いなくTypeScriptの最大の強みの1つです。コミュニティは効率的に**トップJavaScriptプロジェクトのほぼ90％の型ドキュメント**を作成しました。

これは、これらのプロジェクトを非常にインタラクティブかつ探索的な方法で使用できることを意味します。タイプミスを防ぐためにドキュメントを別のウィンドウで開く必要はありません。

## `@types`を使う

インストールは `npm`の上で動作するのでかなり簡単です。例えば`jquery`の型定義を簡単にインストールすることができます：

```text
npm install @types/jquery --save-dev
```

`@types`はグローバルとモジュールの両方の型定義をサポートします。

### グローバル `@types`

デフォルトでは、グローバルに利用する定義は自動的に包含されます。`jquery`を例にすれば、あなたのプロジェクトで`$`をグローバルに使うことができるはずです。

しかし、`jquery`のようなライブラリでは、一般的にモジュールの使用をお勧めします：

### モジュール `@types`

実際のところ、インストール後に特別な設定は必要ありません。モジュールのように使用するだけです。例：

```typescript
import * as $ from "jquery";

// Use $ at will in this module :)
```

## グローバルの制御

予想されるように、グローバル定義を自動許可する設定をすることは、一部のチームでは問題になる可能性があります。したがって`tsconfig.json`の`compilerOptions.types`を使って、必要な型だけを指定して、明示的に取り込むことができます：

```javascript
{
    "compilerOptions": {
        "types" : [
            "jquery"
        ]
    }
}
```

上の例では、`jquery`だけを使用できることを示しています。誰かが`npm install @types/node`のように別の定義をインストールしても、そのグローバル\(例えば [`process`](https://nodejs.org/api/process.html)\) は、あなたが`tsconfig.json`の`types`オプションにそれを追加するまで、あなたのコードには入り込みません。

