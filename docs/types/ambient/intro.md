## アンビエント宣言(Ambient Declarations)

[なぜTypeScriptを使うのか？](../../why-typescript.md)で述べたように：

> TypeScriptの主要な設計目標は、TypeScriptで既存のJavaScriptライブラリを安全かつ簡単に使用できるようにすることでした。TypeScriptはこれを*宣言*で行います。

アンビエント型宣言(declare) を使用すると、既存の一般的なJavaScriptライブラリを安全に使用したり、JavaScript/CoffeeScript/など、他のJavaScriptにコンパイルされるプロジェクトを TypeScript に段階的に移行することができます。

サードパーティ製のJavaScriptコードがアンビエント型を定義しているか、というパターンを見てみることは、あなたのプロジェクトで、TypeScriptの型を定義することにも役に立ちます。それが、これを説明する理由です。
