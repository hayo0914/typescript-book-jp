## プログラム

`program.ts`で定義されています。コンパイルコンテキスト([前に説明した概念](../ project / compilation-context.md))は、TypeScriptコンパイラ内で `Program`として表されます。 `SourceFile`とコンパイラオプションで構成されています。


### `CompilerHost`の使用法
OEとの相互作用メカニズム：

`Program`* -use  - > *` CompilerHost`* -uses  - > * `System`

インライン化のポイントとして `CompilerHost`を持つ理由は、`Program`のニーズに対してより細かく調整され、OEの必要性を気にしないためです(例えば `Program`は`fileExists`を気にしません。 Systemによって提供される機能)。

`System 'の他のユーザ(例えば、テスト)もあります。

### ソースファイル

このプログラムは、ソースファイル `getSourceFiles()：SourceFile [];`を取得するためのAPIを提供します。それぞれは、ASTのルートレベルノード( `SourceFile`と呼ばれます)として表されます。
