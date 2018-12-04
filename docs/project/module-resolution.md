# TypeScriptモジュールの解像度

TypeScriptのモジュール解決は、実際のモジュールシステム/ローダー（commonjs / nodejs、amd / requirejs、ES6 / systemjsなど）をモデル化してサポートしようとします。最も簡単なルックアップは相対ファイルパスルックアップです。その後、さまざまなモジュールローダーによって行われる魔法のモジュールロードの性質のために、少し複雑になります*。

## ファイル拡張子

`foo`や`。/ foo`のようなモジュールをインポートします。任意のファイルパス検索のために、TypeScriptはコンテキストに応じて `.ts`または`.d.ts`または `.tsx`または`.js`（オプション）または `.jsx`（オプション）ファイルを正しい順序で自動的にチェックします。モジュール名をファイル拡張子で指定しないでください（ `foo.ts`、`foo`だけではありません）。

## 相対ファイルモジュール

相対パス（例：

```ts
import foo = require('./foo');
```

TypeScriptコンパイラに相対位置でTypeScriptファイルを探すように指示します。現在のファイルに対して `。/ foo.ts`を実行します。この種の輸入にはそれ以上の魔法はありません。もちろん、それはより長い経路にすることができる。 `。/ foo / bar / bas`や`../../../ foo / bar / bas`のように他の*相対パスと同じように*あなたはディスク上で慣れています。

## 名前付きモジュール

次の文：

```ts
import foo = require('foo');
```

TypeScriptコンパイラに、次の順序で外部モジュールを検索するよう指示します。

* すでにコンパイルコンテキストにあるファイルから名前付きの[module declaration]（#module-declaration）
* まだ解決されておらず、 `--module commonjs`でコンパイルしているか、`--moduleResolution node`を設定している場合は、[* node modules *]（#node-modules）解決アルゴリズムを使って調べます。
* まだ解決されず、 `baseUrl`（オプションで`paths`）を指定した場合、[* path substitutions *]（#path-substitution）解決アルゴリズムが起動します。

``foo '`はより長いパス文字列にすることができます。 ``foo / bar / bas "`となります。ここでの鍵は、 `。/`や `../`*で始まらないことです。

## モジュール宣言

モジュールの宣言は次のようになります：

```ts
declare module "foo" {

    /// Some variable declarations

    export var bar:number; /*sample*/
}
```

これは、モジュールを "foo" `、* importable *にします。

## ノードモジュール
ノードモジュールの解像度は、Node.js / NPM（[official nodejs docs]（https://nodejs.org/api/modules.html#modules_all_together））で使用されている解像度とほぼ同じです。ここに私が持っているシンプルな精神モデルがあります：

* モジュール `foo / bar`はいくつかのファイルに解決されます：`node_modules / foo`（モジュール）+ `foo / bar`

## パスの置換

TODO。

[//Comment1]:https://github.com/Microsoft/TypeScript/issues/2338
[//Comment2]:https://github.com/Microsoft/TypeScript/issues/5039
[//Comment3ExampleRedirectOfPackageJson]:https://github.com/Microsoft/TypeScript/issues/8528#issuecomment-219172026
[//Coment4ModuleResolutionInHandbook]:https://github.com/Microsoft/TypeScript-Handbook/blob/release-2.0/pages/Module%20Resolution.md#base-url
