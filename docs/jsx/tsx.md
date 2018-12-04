# JSXのサポート

TypeScriptは、JSXの翻訳とコード解析をサポートしています。 JSXに慣れていない方は、[公式サイト]（https://facebook.github.io/jsx/）の抜粋です：

> JSXは、定義されたセマンティクスのないECMAScriptへのXMLのような構文拡張です。エンジンやブラウザでは実装されていません。 JSXをECMAScript仕様自体に組み込むことは提案ではありません。これらのトークンを標準のECMAScriptに変換するために、さまざまなプリプロセッサ（transpilers）によって使用されることを意図しています。

JSXの背後にある動機は、ユーザーがHTML *のようなHTML *をJavaScript *で記述できるようにすることです。

* あなたのJavaScriptをチェックしようとしている同じコードでビューのタイプをチェックする
* ビューを操作するコンテキストを認識させる（つまり、従来のMVCでの* controller-view *接続を強化する）。
HTMLメンテナンスのためのJavaScriptパターンの再利用`Array.prototype.map`、`？： `、`switch`などの新しい（おそらくタイプのない）代替ファイルを作成するのではなく、

これにより、エラーの可能性が減り、ユーザーインターフェイスの保守性が向上します。この時点でのJSXの主な消費者は[ReactJS from facebook]（http://facebook.github.io/react/）です。ここではJSXの使い方について説明します。
