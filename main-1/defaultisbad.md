# Avoid Export Default

## `export default`は有害だと考えられます

以下の内容の`foo.ts`ファイルがあるとします：

```typescript
class Foo {
}
export default Foo;
```

次のように、ES6構文を使用して\(bar.tsで\)インポートします。

```typescript
import Foo from "./foo";
```

これには保守性の問題がいくつかあります：

* `foo.ts`で`Foo`をリファクタリングしても、`bar.ts`では名前が変更されません
* `foo.ts`\(これはあなたのファイルの多くが参照しているものです\)から、より多くのものをexportする必要がある場合、import構文をいじくる必要があります。

このため、私はシンプルなexports + 分解importを推奨します。例: `foo.ts`:

```typescript
export class Foo {
}
```

そして：

```typescript
import {Foo} from "./foo";
```

下にもいくつかの理由を書きます。

## CommonJSとの相互運用

`default`は、`const {Foo} = require('module/foo')`の代わりに、`const {default} = require('module/foo');`を書かないといけないCommonJSユーザーにとって、恐ろしい体験になります。あなたはたいてい`default`エクスポートをインポートしたときに他の何かにリネームすることになるでしょう。

## 低い検出性\(Poor Discoverability\)

デフォルトエクスポートは検出性\(Discoverability\)が低いです。あなたはインテリセンスでモジュールを辿り、それがデフォルトエクスポートを持っているかどうかを知ることができません。

デフォルトエクスポートでは、あなたは何も得られません\(それはデフォルトエクスポートを持っているかもしれませんし、持っていないかもしれません`¯\_(ツ)_/¯`\):

```typescript
import /* here */ from 'something';
```

デフォルトエクスポートが無ければ、素晴らしいインテリセンスが得られます。

```typescript
import { /* here */ } from 'something';
```

## オートコンプリート\(Autocomplete\)

エクスポートについて知っているか、いないかに関わらず、あなたはカーソル位置で`import {/*here*/} from "./foo";`をオートコンプリートできます。それはデベロッパーに少しの安心感を与えます。

## タイポに対する防御\(Typo Protection\)

あなたは`import Foo from "./foo";`をしながら、他で`import foo from "./foo";`をするようなタイポをしたくないでしょう。

## TypeScriptの自動インポート

自動インポート修正は、うまく動きます。あなたが`Foo`を使うと、自動インポートは`import { Foo } from "./foo";`を書き記します。なぜなら、それはきちんと定義された名前がモジュールからエクスポートされているからです。いくつかのツールは、魔法のようにデフォルトエクスポートの名前を推論します。しかし、風変わりな魔法です。

## 再エクスポート\(Re-exporting\)

再エクスポートは不必要に難しいです。再エクスポートはnpmパッケージのルートの`index`ファイルで一般的に行われます。例:`import Foo from "./foo"; export { Foo }`\(デフォルトエクスポート\) vs. `export * from "./foo"`\(名前付きエクスポート\)

## Dynamic Imports

デフォルトエクスポートは、`default`を動的にインポートしたときに、それ自身に悪い名前を付けます。例:

```typescript
const HighChart = await import('https://code.highcharts.com/js/es-modules/masters/highcharts.src.js');
Highcharts.default.chart('container', { ... }); // Notice `.default`
```

## 非クラス/非関数の場合、2行必要です

関数/クラスに対しては、1行で書けます:

```typescript
export default function foo() {
}
```

名前が無い/型アノテーションされたオブジェクトに対しても、1行で書けます:

```typescript
export default {
  notAFunction: 'Yeah, I am not a function or a class',
  soWhat: 'The export is now *removed* from the declaration'
};
```

しかし、他のものに対しては2行必要です:

```typescript
// If you need to name it (here `foo`) for local use OR need to annotate type (here `Foo`)
const foo: Foo = {
  notAFunction: 'Yeah, I am not a function or a class',
  soWhat: 'The export is now *removed* from the declaration'
};
export default foo;
```

