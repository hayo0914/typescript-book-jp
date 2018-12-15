### Binder function
2つの重要なバインダー関数は`bindSourceFile`と`mergeSymbolTable`です。これらを次に見ていきます。

#### `bindSourceFile`
基本的に`file.locals`が定義されているかどうかを確認し、そうでなければ(ローカル関数)`bind`に渡します。

注： `locals`は`Node`で定義され、`SymbolTable`型です。`SourceFile`もまた`Node`(実際にはASTのルートNode)であることに注意してください。

TIP: ローカル関数は、TypeScriptコンパイラで頻繁に使用されます。ローカル関数は親関数(クロージャによって捕捉される)からの変数を使用することが非常に多いです。`bind`(`bindSourceFile`内のローカル関数)の場合、それ(またはそれが呼び出す関数)は`symbolCount`と`classifiableNames`をセットアップし、返された `SourceFile`に格納されます。

#### `bind`
Bindは(ただの`SourceFile`ではなく)何らかの`Node`を取ります。最初に行うことは、`node.parent`(もし`parent`変数がセットアップされていれば ... それは、Binderが`bindChildren`関数内の処理中に行うことです)を代入し、重い作業を行う`bindWorker`に渡します。最後に、これは`bindChildren`を呼び出します(単にバインダーの状態を格納する関数です。例えば現在の`parent`をその関数のローカル変数に格納し、子それぞれに`bind`を呼び出して、それからbinderの状態を復元します)。もっと興味深い関数である`bindWorker`を見てみましょう。

#### `bindWorker`
この関数は`node.kind`(`SyntaxKind`型)によってスイッチし、適切な`bindFoo`関数(`binder.ts`で定義されています)に処理をデリゲートします。例えば`node`が`SourceFile`であれば`bindAnonymousDeclaration`を呼び出します(最終的に外部ファイルモジュールである場合のみ)。

#### `bindFoo`関数
`bindFoo`関数に共通するパターンと、これらが使用するいくつかのユーティリティ関数があります。ほぼ常に使用される関数の1つは、`createSymbol`関数です。以下にその全体を示します。

```ts
function createSymbol(flags: SymbolFlags, name: string): Symbol {
    symbolCount++;
    return new Symbol(flags, name);
}
```
ご覧のとおり、`symbolCount`(`bindSourceFile`のローカル)を最新の状態にし、指定されたパラメータでSymbolを作成しています。
