## アンビエント宣言

[なぜTypeScript]（../../ why-typescript.md）で述べたように：

> TypeScriptの主要な設計目標は、TypeScriptで既存のJavaScriptライブラリを安全かつ簡単に使用できるようにすることでした。 TypeScriptはこれを*宣言*で行います。

アンビエント宣言を使用すると、既存の一般的なJavaScriptライブラリを安全に使用したり、JavaScript / CoffeeScript / Other-Compile-To-Js-LanguageプロジェクトをTypeScript *に段階的に移行することができます。

* サードパーティのJavaScriptコード*の環境宣言でパターンを学習することは、*あなたの* TypeScriptコードベースにも注釈を付ける良い習慣です。これが早い時期にそれを提示する理由です。
