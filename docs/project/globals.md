# globals.d.ts

我々は、[projects](./modules.md)や、ファイルベースのモジュールを使うことでグローバル名前空間の汚染を避ける手段を見ていく中で、グローバルモジュールとファイルモジュールの比較について議論しました。

しかしながら、もし初心者のTypeScriptの開発者がいる場合は、彼らにglobals.d.tsファイルを渡し、グローバルな名前空間にインターフェース/型を宣言し、全てのあなたのTypeScriptコードで魔法のように型を利用可能にすることができます。

> JavaScriptを生成するコードについては全て、ファイルモジュールの使用を強くお勧めします

* `globals.d.ts`は、必要に応じて`lib.d.ts`を拡張するのに最適です
* TSからJSに移行している時に、簡単に`declare module "some-library-you-dont-care-to-get-defs-for";`することができます
