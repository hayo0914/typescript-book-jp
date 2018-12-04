## ノード
抽象構文木（AST）の基本ビルディングブロック。一般に、「ノード」は言語文法の非終端記号を表す。ただし、識別子やリテラルなどのツリーには端末が保持されています。

2つの重要なことが、ASTノードのドキュメントを構成します。 AST内の型を識別するノードの「SyntaxKind」と、ASTにインスタンス化されたときにノードが提供するAPIである `interface`。

いくつかの主要な `interface Node`メンバーがあります：
ソースファイル内のノードの `start`と`end`を識別する `TextRange`メンバ。
* `parent ?: Node`は、ASTのノードの親です。

`Node`フラグと修飾子のための他の追加のメンバがあります。あなたはソースコード中で`interface Node`を検索することで検索することができますが、ここで言及したものはノードトラバーサルにとって不可欠です。

## ソースファイル

* `SyntaxKind.SourceFile`
* `interface SourceFile`。

各 `SourceFile`は`Program`に含まれるトップレベルのASTノードです。
