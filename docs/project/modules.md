## モジュール(Modules)

### グローバルモジュール(Global Module)

デフォルトでは、新しいTypeScriptファイルにコードを入力すると、コードは*グローバル*名前空間(global namespace)に入ります。デモとして、`foo.ts`ファイルを考えてみましょう：

```ts
var foo = 123;
```

同じプロジェクトで新しいファイル`bar.ts`を作成すると、TypeScriptの型システムは、変数`foo`をグローバルに利用することを許容します：

```ts
var bar = foo; // allowed
```
言うまでもありませんが、グローバル名前空間を使うとコードで名前が競合する危険があります。次のファイルモジュール(File Module)を使用することをお勧めします。

### ファイルモジュール(File Module)
*external modules*とも呼ばれます。TypeScriptファイルのルートレベルに`import`または`export`が存在する場合、そのファイル内にローカルスコープ(local scope)が作成されます。したがって、以前の`foo.ts`を次のように変更した場合(`export`に注目)：

```ts
export var foo = 123;
```

我々はもはやグローバル名前空間の`foo`を持っていません。これは、次のように新しいファイル `bar.ts`を作成することで実証できます：

```ts
var bar = foo; // ERROR: "cannot find name 'foo'"
```

`bar.ts`で`foo.ts`のものを使いたい場合*明示的にインポートする必要があります*。これを以下の更新版の`bar.ts`に示します：

```ts
import { foo } from "./foo";
var bar = foo; // allowed
```
`bar.ts`で`import`を使うと、他のファイルから取り込むことができるだけでなく、ファイル`bar.ts`をモジュールとして認識するので、`bar.ts`での宣言は `グローバル名前空間を汚染しません。

外部モジュールを使用するTypeScriptファイルのJavaScriptへのコンパイルは、`module`というコンパイラフラグが必要です。
