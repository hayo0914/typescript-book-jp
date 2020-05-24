# JSX

TypeScriptは、JSXの翻訳とコード解析をサポートしています。 JSXに慣れていない方のために、[公式サイト](https://facebook.github.io/jsx/)を抜粋しました：

> JSXは、定義されたセマンティクスのないECMAScriptへのXMLのような構文拡張です。エンジンやブラウザでは実装することを意図したものではありません。JSXをECMAScript仕様自体に組み込むことを提案するものではありません。これらのトークンを標準のECMAScriptに変換するために、さまざまなプリプロセッサ\(transpilers\)によって使用されることを意図しています。

JSXの背景にある動機は、ユーザーがHTMLのようなビューをJavaScriptで記述できるようにすることです。

* あなたのJavaScriptと同じようにビューの型チェックをすること
* ビューを操作するコンテキストを認識させる\(つまり、従来のMVCでの_controller-view_の接続を強化する\)。
* HTMLのメンテナンスに、JavaScriptパターン\(`Array.prototype.map`、`?:`、`switch`など\)を\(新しい代替\(おそらくほとんど型付けされない\)を作成する代わりに\)再利用する。

これにより、エラーの可能性が減り、ユーザーインターフェースの保守性が向上します。現時点でのJSXの主なユーザーは[ReactJS from facebook](http://facebook.github.io/react/)です。ここではJSXの使い方について説明します。

