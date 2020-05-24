# モジュール

## グローバルモジュール\(Global Module\)

デフォルトでは、新しいTypeScriptファイルにコードを入力すると、コードは_グローバル_名前空間\(global namespace\)に入ります。デモとして、`foo.ts`ファイルを考えてみましょう：

```typescript
var foo = 123;
```

同じプロジェクトで新しいファイル`bar.ts`を作成すると、TypeScriptの型システムは、変数`foo`をグローバルに利用することを許容します：

```typescript
var bar = foo; // allowed
```

言うまでもありませんが、グローバル名前空間を使うと、あなたのコードが名前競合の危険にさらされます。次のファイルモジュール\(File Module\)を使用することをお勧めします。

## ファイルモジュール\(File Module\)

外部モジュール\(_external modules_\)とも呼ばれます。TypeScriptファイルのルートレベルに`import`または`export`が存在する場合、そのファイル内にローカルスコープ\(_local scope_\)が作成されます。以前の`foo.ts`を次のように変更した場合を見てください\(`export`に注目してください\)：

```typescript
export var foo = 123;
```

我々はもはやグローバル名前空間の`foo`を持っていません。これは、次のように新しいファイル `bar.ts`を作成することで実証できます：

```typescript
var bar = foo; // ERROR: "cannot find name 'foo'"
```

`bar.ts`で`foo.ts`のものを使いたい場合_明示的にインポートする必要があります_。これを以下の更新版の`bar.ts`に示します：

```typescript
import { foo } from "./foo";
var bar = foo; // allowed
```

`bar.ts`で`import`を使うと、他のファイルから取り込むことができるだけでなく、ファイル`bar.ts`をモジュールとして認識するので、`bar.ts`での宣言はグローバル名前空間を汚染しません。

外部モジュールを使用するTypeScriptファイルのJavaScriptへのコンパイルは、`module`というコンパイラフラグが必要です。

