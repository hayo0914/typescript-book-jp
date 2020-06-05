# React以外のJSX

TypeScriptは、React with JSX以外のものをタイプセーフな方法で使用する機能を提供します。以下は、カスタマイズ可能なポイントを示していますが、これは高度なUIフレームワークの作成者向けです。

* `"jsx" : "preserve"`オプションを使って`react`形式の出力を無効にすることができます。これは、JSXが_そのままの状態で_出力されることを意味します。そして、あなた自身のカスタムトランスパイラを使用してJSX部分をトランスパイルすることができます
* `JSX`グローバルモジュールを使う：
  * `JSX.IntrinsicElements`インターフェースのメンバをカスタマイズすることで、どのHTMLタグが利用可能で、どのように型チェックされるかを制御することができます。
  * コンポーネントを使用する場合：
    * デフォルトの`interface ElementClass extends React.Component<any, any> { }`宣言をカスタマイズすることによって、どのクラスがコンポーネントによって継承されなければならないかを制御できます
    * どのプロパティが属性\(デフォルトは`props`\)の型チェックに使われるかを制御できます。`declare module JSX { interface ElementAttributesProperty { props: {}; } }`の宣言をカスタマイズすることで行います。

## `jsxFactory`

`--jsxFactory <JSX factory Name>`と `--jsx react`を一緒に渡すことで、デフォルトの`React`とは別のJSXファクトリを使うことができます。

新しいファクトリ名は`createElement`関数を呼び出すために使われます。

### 例

```typescript
import {jsxFactory} from "jsxFactory";

var div = <div>Hello JSX!</div>
```

コンパイル：

```text
tsc --jsx react --reactNamespace jsxFactory --m commonJS
```

結果：

```javascript
"use strict";
var jsxFactory_1 = require("jsxFactory");
var div = jsxFactory_1.jsxFactory.createElement("div", null, "Hello JSX!");
```

## `jsx`プラグマ\(`jsx` pragma\)

`jsxPragma`を使用してファイルごとに異なる`jsxFactory`を指定することもできます。

```javascript
/** @jsx jsxFactory */
import {jsxFactory} from "jsxFactory";

var div = <div>Hello JSX!</div>
```

`--jsx react`を指定すると、このファイルはjsxプラグマで指定されたファクトリを使用して出力されます：

```javascript
"use strict";
var jsxFactory_1 = require("jsxFactory");
var div = jsxFactory_1.jsxFactory.createElement("div", null, "Hello JSX!");
```

