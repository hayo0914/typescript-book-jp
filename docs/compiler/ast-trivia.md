### Trivia
Trivia(`trivial`だからそう呼ばれます)は、コードの正常な理解のためにはほとんど重要でないソーステキストの部分を表します。例えば;、空白、コメント、さらには競合マーカー(conflict markers)が含まれます。TriviaはASTに保存されません(軽量に保つため)。しかし、いくつかの`ts.*`APIを使用してオンデマンドでフェッチすることができます。

それらを表示する前に、以下を理解する必要があります。

#### Triviaのオーナーシップ
一般に：
* トークンは、次のトークンまでの間に何らかのtrivaを同じ行の後ろに保持しています
* その行の後の何らかのコメントは、次のトークンに関連付けられます。

ファイル内の先頭と末尾のコメント：
* ソースファイルの最初のトークンはすべての初期状態のtriviaを取得します。
* ファイル内のtriviaの最後のシーケンスは、ファイルの終わりのトークンに付けられます。それ以外の場合はゼロ幅です。

#### TriviaのAPI
ほとんどの基本的な用途では、コメントは"interesting"なtriviaです。Nodeに属するコメントは、次の関数を使用して取得できます。

関数|説明
--------- | ------------
`ts.getLeadingCommentRanges`|そのテキスト内のソーステキストと位置を指定すると、与えられた位置に続く、最初の改行と、トークン自体の間のコメントの範囲を返します(おそらく、`ts.Node.getFullStart`で最も有用です)。
`ts.getTrailingCommentRanges`|そのテキスト内のソーステキストと位置を指定すると、与えられた位置に続く最初の改行までのコメントの範囲を返します(おそらく `ts.Node.getEnd`で最も有用です)。

例として、ソースファイルのこの部分を想像してみてください：

```ts
debugger;/*hello*/
    //bye
  /*hi*/    function
```

`function`の`getLeadingCommentRanges`は、最後の2つのコメント`//bye`と`/*hi*/`だけを返します。

状況にフィットするように、debugger文の後ろで`getTrailingCommentRanges`を呼び出すと、`/*hello*/`コメントが展開されます。

#### Token Start/Full Start
Nodesには、"token start"と"full start"というものがあります。

* Token Start：より自然なバージョン。トークンのテキストが始まるファイル内の位置
* Full Start：Scannerが最後の意味のあるトークンからスキャンを開始した位置

ASTノードには、`getStart`と`getFullStart`のためのAPIがあります。次の例です:

```ts
debugger;/*hello*/
    //bye
  /*hi*/    function
```
`function`の場合、token startは`function`にありますが、full startは`/*hello*/`にあります。full startには、(それ以外の場合は前のノードに属する)Triviaも含まれます。
