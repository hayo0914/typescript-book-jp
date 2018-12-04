### バインダー関数
2つの重要なバインダー関数は `bindSourceFile`と`mergeSymbolTable`です。これらを次に見ていきます。

#### `bindSourceFile`
基本的に `file.locals`が定義されているかどうかを確認し、そうでなければ（ローカル関数）`bind`に渡します。

注： `locals`は`Node`で定義され、 `SymbolTable`型です。 `SourceFile`も`Node`（実際にはASTのルートノード）であることに注意してください。

ヒント：ローカル関数は、TypeScriptコンパイラで頻繁に使用されます。局所関数は親関数（閉包によって捕捉された）からの変数を使用する可能性が非常に高い。 `bind`（`bindSourceFile`内のローカル関数）の場合、それ（またはそれが呼び出す関数）は `symbolCount`と`classifiableNames`を設定し、返された `SourceFile`に格納されます。

#### `bind`
Bindは（ `SourceFile`だけでなく）`Node`を取ります。最初に行うことは、 `node.parent`（もし`parent`変数が設定されていれば... bindChildren`関数内で処理中にバインダーが何かすることです）を割り当て、 `bindWorker`に渡します。 *重い*持ち上げますか？最後に、これは `bindChildren`（単にバインダー状態、例えば現在の`parent`をその関数のローカル変数に格納し、各子に `bind`を呼び出してバインダー状態を復元する関数）を呼び出します。もっと興味深い関数である `bindWorker`を見てみましょう。

#### `bindWorker`
この関数は（ `SyntaxKind`型の）`node.kind`を有効にし、適切な `bindFoo`関数（`binder.ts`で定義されています）に作業を委譲します。例えば ​​`node`が`SourceFile`であれば（最終的には外部ファイルモジュールである場合のみ） `bindAnonymousDeclaration`

#### `bindFoo`関数
`bindFoo`関数に共通するパターンと、これらが使用するいくつかのユーティリティ関数があります。ほぼ常に使用される関数の1つは、 `createSymbol`関数です。以下にその全体を示す。

```ts
function createSymbol(flags: SymbolFlags, name: string): Symbol {
    symbolCount++;
    return new Symbol(flags, name);
}
```
ご覧のとおり、 `symbolCount`（`bindSourceFile`のローカル）を最新の状態に保ち、指定されたパラメータでシンボルを作成しています。
