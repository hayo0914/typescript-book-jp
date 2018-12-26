# よくあるエラー(Common Errors)
このセクションでは、ユーザーが現実世界で経験する多くの一般的なエラーコードについて説明します。

## TS2304
サンプル：
> `Cannot find name ga` `Cannot find name $` `Cannot find module jquery`

おそらく第三者のライブラリ(Googleアナリティクスなど)を使用しており、宣言していません。TypeScriptは、*スペルミス*や宣言しないで変数を使用すると、あなたを助けようとします。あなたは外部ライブラリを取り込んでいるので実行時に利用可能なものに明示する必要があります[修正方法](../types/ambient/d.ts.html)。

## TS2307
サンプル：
> `Cannot find module 'underscore'`

おそらく、サードパーティのライブラリ(underscoreなど)を*モジュール*([モジュールの詳細](../project/modules.html)はこちらです)として使用していて、それに対する環境宣言ファイルがありません。

## TS1148
サンプル：
> `'Cannot compile modules unless the '--module' flag is provided`

[モジュール](../project/modules.html)のセクションをチェックしてください。

## キャッチ句の変数は型アノテーションを持つことはできません(Catch clause variable cannot have a type annotation)
サンプル：
```js
try { something(); }
catch (e: Error) { // Catch clause variable cannot have a type annotation
}
```
TypeScriptはワイルドで間違ったJavaScriptからあなたを守ろうとします。Type Guardを代わりに使ってください。
```js
try { something(); }
catch (e) {
  if (e instanceof Error){
    // Here you go.
  }
}
```

## Interface `ElementClass`は`Component`と `Component`の型を同時に継承することはできません。(Interface `ElementClass` cannot simultaneously extend types `Component` and `Component`)
これはコンパイルコンテキストに2つの`react.d.ts`(`@types/react/index.d.ts`)があるときに起こります。

**修正**：
* `node_modules`と`package-lock`(またはyarn lock)と`npm install`をもう一度削除してください。
* うまくいかない場合は、無効なモジュールを見つけてください(あなたのプロジェクトで使われているすべてのモジュールは`react.d.ts`を`peerDependency`とするべきです。hardな`dependency`は持たないようにしてください)。

[ambient]: ../types/ambient/d.ts.md
[modules]: ../project/modules.md
