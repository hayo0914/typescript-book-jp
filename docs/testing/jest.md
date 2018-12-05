# TypeScriptでJestを使う

> [Jest / TypeScriptのプロの卵ヘッドレッスン](https://egghead.io/lessons/typescript-getting-started-with-jest-using-typescript)

アウトテストソリューションは完璧です。つまり、jestは優れたTypeScriptサポートを提供する優れたユニットテストオプションです。

> 注意：単純なノードpackage.json setupで始めることを前提としています。また、すべてのTypeScriptファイルは `src`フォルダに置かれていなければなりません。このフォルダは、きれいなプロジェクト設定のために(Jestを使わなくても)常に推奨されます。

## ステップ1：インストール

npmを使用して次をインストールします。

```shell
npm i jest @types/jest ts-jest -D
```

説明：

* `jest`フレームワークをインストールします(`jest`)
* `jest`の型をインストールしてください(`@ types / jest`)
* Jest( `ts-jest`)用のTypeScriptプリプロセッサをインストールしてください。これにより、Jestはその場でTypeScriptを翻訳し、ソースマップのサポートを組み込みます。
* これらのすべてをあなたのdevの依存関係に保存してください(テストはほとんど常にnpmの依存関係です)

## ステップ2：Jestを設定する

次の `jest.config.js`ファイルをプロジェクトのルートに追加します：

```js
module.exports = {
  "roots": [
    "<rootDir>/src"
  ],
  "transform": {
    "^.+\\.tsx?$": "ts-jest"
  },
  "testRegex": "(/__tests__/.*|(\\.|/)(test|spec))\\.tsx?$",
  "moduleFileExtensions": [
    "ts",
    "tsx",
    "js",
    "jsx",
    "json",
    "node"
  ],
}
```

説明：

* すべての* TypeScriptファイルをプロジェクトの `src`フォルダに入れることを常にお勧めします。これが真であると仮定し、 `roots`オプションを使用してこれを指定します。
* `transform`設定は、`jest`にts / tsxファイルに対して `ts-jest`を使うように指示します。
* `testRegex`はJestに`__tests__`フォルダ内のテストを検索するよう指示します。また `(.test | .spec)。(ts | tsx)`拡張子を使用する任意のファイルを検索します。 `asdf.test.tsx`など
* `moduleFileExtensions`はjestにファイル拡張子を認識させます。これは `ts`/` tsx`をデフォルト( `js | jsx | json | node`)に追加するときに必要です。

## 手順3：テストを実行する

あなたのプロジェクトのルートから `npx jest`を実行すると、jestはあなたが持っているテストを実行します。

### オプション：npmスクリプトのスクリプトターゲットを追加する

`package.json`を追加してください：

```json
{
  "test": "jest"
}
```

* これにより、簡単な `npm t 'でテストを実行できます。
* また、 `npm t --watch`の時計モードでも。

### オプション：時計モードでjestを実行する

* `npx jest --watch`

### 例

* `foo.ts`ファイルの場合：

```js
export const sum
  = (...a: number[]) =>
    a.reduce((acc, val) => acc + val, 0);
```

* 単純な `foo.test.ts`：

```js
import { sum } from '../';

test('basic', () => {
  expect(sum()).toBe(0);
});

test('basic again', () => {
  expect(sum(1, 2)).toBe(3);
});
```

ノート：

* Jestは、グローバルな `test`関数を提供します。
* Jestには、グローバルな `expect`の形でアサーションがあらかじめ組み込まれています。

### Example async

Jestには、非同期/待機サポートが組み込まれています。例えば

```js
test('basic',async () => {
  expect(sum()).toBe(0);
});

test('basic again', async () => {
  expect(sum(1, 2)).toBe(3);
}, 1000 /* optional timeout */);
```

### 酵素の例

> [酵素/ Jest / TypeScriptのプロの卵レッスン](https://egghead.io/lessons/react-test-react-components-and-dom-using-enzyme)

酵素では、反応成分をDOMサポートでテストすることができます。酵素を設定するには3つのステップがあります：

1. 酵素の種類、酵素の種類、酵素のスナップショットシリアライザ、酵素 - アダプター - あなたの反応のバージョン `npm i酵素/酵素-json酵素 - アダプター - 反応-16 -D`
2. ``snapshotSerializers ``と ``setupTestFrameworkScriptFile '`を`jest.config.js`に追加します：

```js
module.exports = {
  // OTHER PORTIONS AS MENTIONED BEFORE

  // Setup Enzyme
  "snapshotSerializers": ["enzyme-to-json/serializer"],
  "setupTestFrameworkScriptFile": "<rootDir>/src/setupEnzyme.ts",
}
```

3. `src / setupEnzyme.ts`ファイルを作成します。

```js
import { configure } from 'enzyme';
import * as EnzymeAdapter from 'enzyme-adapter-react-16';
configure({ adapter: new EnzymeAdapter() });
```

次に、反応コンポーネントとテストの例を示します。

* `checkboxWithLabel.tsx`：

```ts
import * as React from 'react';

export class CheckboxWithLabel extends React.Component<{
  labelOn: string,
  labelOff: string
}, {
    isChecked: boolean
  }> {
  constructor(props) {
    super(props);
    this.state = { isChecked: false };
  }

  onChange = () => {
    this.setState({ isChecked: !this.state.isChecked });
  }

  render() {
    return (
      <label>
        <input
          type="checkbox"
          checked={this.state.isChecked}
          onChange={this.onChange}
        />
        {this.state.isChecked ? this.props.labelOn : this.props.labelOff}
      </label>
    );
  }
}

```

* `checkboxWithLabel.test.tsx`：

```ts
import * as React from 'react';
import { shallow } from 'enzyme';
import { CheckboxWithLabel } from './checkboxWithLabel';

test('CheckboxWithLabel changes the text after click', () => {
  const checkbox = shallow(<CheckboxWithLabel labelOn="On" labelOff="Off" />);
  
  // Interaction demo
  expect(checkbox.text()).toEqual('Off');
  checkbox.find('input').simulate('change');
  expect(checkbox.text()).toEqual('On');
  
  // Snapshot demo
  expect(shallow).toMatchSnapshot();
});
```

## 私たちは冗談が好きな理由

> [これらの機能の詳細についてはjest websiteを参照](http://facebook.github.io/jest/)

* アサーションライブラリを内蔵しています。
* 優れたTypeScriptサポート。
* 非常に信頼できるテストウォッチャー。
* スナップショットテスト。
* カバレッジレポートが組み込まれています。
* ビルトインの非同期/サポートを待っています。
