# AST

## Node

抽象構文木\(AST\)の基本的な建設部材です。一般に、`Node`は言語文法の非終端記号を表します。ただし、識別子やリテラルなどとして、終端記号がツリーに保持されています。

ASTノードのドキュメントを構成するものは、2つのキーとなるものです。AST内の型を識別するノードの`SyntaxKind`と、ASTにインスタンス化されたときにノードが提供するAPIである `interface`です。

いくつかの主要な `interface Node`のメンバがあります：

* ソースファイル内のノードの`start`と`end`を識別する`TextRange`メンバ
* ASTの中でノードの親となる`parent?: Node`

`Node`のフラグと修飾子のために、いくつか他のメンバがあります。あなたはソースコード中で`interface Node`を検索することで見つけることができます。しかし、上記で言及したものは、ノードトラバーサル\(node traversal\)のために不可欠です。

## SourceFile

* `SyntaxKind.SourceFile`
* `interface SourceFile`。

各`SourceFile`は`Program`に含まれるトップレベルのASTノードです。

