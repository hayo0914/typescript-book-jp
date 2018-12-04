## バレル

バレルとは、複数のモジュールから1つの便利なモジュールにエクスポートをロールアップする方法です。バレル自体は、他のモジュールの選択されたエクスポートを再エクスポートするモジュールファイルです。

ライブラリ内の次のクラス構造を想像してみてください。

```ts
// demo/foo.ts
export class Foo {}

// demo/bar.ts
export class Bar {}

// demo/baz.ts
export class Baz {}
```

バレルがなければ、消費者は3つの輸入明細書を必要とするでしょう：

```ts
import { Foo } from '../demo/foo';
import { Bar } from '../demo/bar';
import { Baz } from '../demo/baz';
```

代わりに、以下を含む `demo / index.ts`バレルを追加することができます：

```ts
// demo/index.ts
export * from './foo'; // re-export all of its exports
export * from './bar'; // re-export all of its exports
export * from './baz'; // re-export all of its exports
```

今、消費者は必要なものをバレルからインポートできます：

```ts
import { Foo, Bar, Baz } from '../demo'; // demo/index.ts is implied
```

### 名前付きエクスポート
`*`をエクスポートする代わりに、モジュールを名前でエクスポートすることができます。たとえば、 `baz.ts`に次のような機能があるとします。

```ts
// demo/foo.ts
export class Foo {}

// demo/bar.ts
export class Bar {}

// demo/baz.ts
export function getBaz() {}
export function setBaz() {}
```

デモから `getBaz`/` setBaz`をエクスポートするのではなく、名前の中にそれらをインポートし、その名前を以下のようにエクスポートすることで変数に入れることができます：

```ts
// demo/index.ts
export * from './foo'; // re-export all of its exports
export * from './bar'; // re-export all of its exports

import * as baz from './baz'; // import as a name
export { baz }; // export the name
```

そして今、消費者は次のようになります：

```ts
import { Foo, Bar, baz } from '../demo'; // demo/index.ts is implied

// usage
baz.getBaz();
baz.setBaz();
// etc. ...
```
