## プログラム

`program.ts`で定義されています。コンパイルコンテキスト([前に説明した概念](../project/compilation-context.md))は、TypeScriptコンパイラ内で `Program`として表されます。`SourceFile`とコンパイラオプションで構成されています。


### `CompilerHost`の使用法
OEとの相互作用メカニズムを示します：

`Program`*-uses->*`CompilerHost`*-uses->*`System`

接続するものとして`CompilerHost`を持つ理由は、`Program`のニーズに対して、より細かく調整できるようにし、OEの要求に悩まされないようにするためです(例えば `Program`は`System`によって提供される`fileExists`関数を考慮しません)。

`System`と同様に他のユーザ(例えば、テスト)もあります。

### ソースファイル

programは、ソースファイルを取得するためのAPI`getSourceFiles()：SourceFile [];`を提供します。それぞれは、ASTのルートレベルのノード(`SourceFile`と呼ばれます)として表されます。
