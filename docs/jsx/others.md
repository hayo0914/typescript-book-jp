# 非リアクションJSX

TypeScriptは、React with JSX以外のものをタイプセーフな方法で使用する機能を提供します。以下は、カスタマイズ可能ポイントを示していますが、これは高度なUIフレームワークの作成者向けです。

* ``jsx '： "preserve" `オプションを使って`react`スタイルのemitを無効にすることができます。これは、JSXが*そのままの状態で放出されることを意味します。そして、あなた自身のカスタムトランスパイラを使用してJSX部分を透明化することができます。
* `JSX`グローバルモジュールを使う：
    * `JSX.IntrinsicElements`インターフェースメンバをカスタマイズすることで、どのHTMLタグが利用可能で、どのように型チェックされているかを制御することができます。
    *コンポーネントを使用する場合：
        *デフォルトの `Interface ElementClass extends React.Component <any any> {}`宣言をカスタマイズすることによって、どのクラスがコンポーネントによって継承されなければならないかを制御できます。
        * declare module JSX {interface ElementAttributesProperty {props：{};}をカスタマイズすることで、どのプロパティをタイプするのに使われる属性を制御できます（デフォルトは `props`です）。 }} `宣言。

## `jsxFactory`

`--jsxFactory <JSX factory name>`と `--jsx react`を一緒に渡すことで、デフォルトの`React`から別のJSXファクトリを使うことができます。

新しいファクトリ名は `createElement`関数を呼び出すために使われます。

### 例

```ts
import {jsxFactory} from "jsxFactory";

var div = <div>Hello JSX!</div>
```

コンパイル済み：

```shell
tsc --jsx react --reactNamespace jsxFactory --m commonJS
```

結果：

```js
"use strict";
var jsxFactory_1 = require("jsxFactory");
var div = jsxFactory_1.jsxFactory.createElement("div", null, "Hello JSX!");
```

## `jsx`プラグマ

`jsxPragma`を使用してファイルごとに異なる`jsxFactory`を指定することもできます。


```js
/** @jsx jsxFactory */
import {jsxFactory} from "jsxFactory";

var div = <div>Hello JSX!</div>
```

`--jsx react`を指定すると、このファイルはjsxプラグマで指定されたファクトリを使用して出力されます：
```js
"use strict";
var jsxFactory_1 = require("jsxFactory");
var div = jsxFactory_1.jsxFactory.createElement("div", null, "Hello JSX!");
```
