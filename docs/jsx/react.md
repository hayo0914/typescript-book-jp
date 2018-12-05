# React JSX

> [Type ScriptとReactのPRO Eggheadコース](https://egghead.io/courses/use-typescript-to-develop-react-applications)

## セットアップ

私たちのブラウザクイックスタートでは、すでに反応アプリケーションの開発をセットアップしています(../ quick / browser.md)。ここに主要なハイライトがあります。

* ファイル拡張子 `.tsx`(`.ts`の代わりに)を使用してください。
* あなたの `tsconfig.json`の`compilerOptions`で `` jsx "：" react "を使ってください。
* JSXとReactの定義をあなたのプロジェクトにインストールします：( `npm i -D @ types / react @ types / react-dom`)。
* Importは、あなたの `.tsx`ファイルに反応します(` import *はReactから "react"となります)。

## HTMLタグとコンポーネント

Reactは、HTMLタグ(文字列)またはReactコンポーネント(クラス)をレンダリングできます。これらの要素に対するJavaScriptの発行は異なります( `React.createElement( 'div')`対 `React.createElement(MyComponent)`)。これが決まる方法は*最初の*文字の* case *です。 `foo`はHTMLタグとして扱われ、`Foo`はコンポーネントとして扱われます。

## 型式チェック

### HTMLタグ

HTMLタグ `foo`の型は`JSX.IntrinsicElements.foo`です。これらのタイプは、セットアップの一部としてインストールした `react-jsx.d.ts`ファイルのすべてのメジャータグに対してすでに定義されています。次に、ファイルの内容のサンプルを示します。

```ts
declare module JSX {
    interface IntrinsicElements {
        a: React.HTMLAttributes;
        abbr: React.HTMLAttributes;
        div: React.HTMLAttributes;
        span: React.HTMLAttributes;

        /// so on ...
    }
}
```

### ステートレス機能コンポーネント

あなたは単に `React.SFC`インターフェースでステートレスコンポーネントを定義することができます。

```ts
type Props = {
  foo: string;
}
const MyComponent: React.SFC<Props> = (props) => {
    return <span>{props.foo}</span>
}

<MyComponent foo="bar" />
```

### ステートフルなコンポーネント

コンポーネントは、コンポーネントの `props`プロパティに基づいてタイプチェックされます。これは、JSXがどのように変換されるか、すなわち属性がコンポーネントの「小道具」になるようにモデル化されています。

React Statefulコンポーネントを作成するには、ES6クラスを使用します。 `react.d.ts`ファイルはあなた自身の`Props`と `State`インターフェースを提供するあなたのクラスで拡張すべき`React.Component <Props、State> `クラスを定義しています。これは以下のとおりです：

```ts
type Props = {
  foo: string;
}
class MyComponent extends React.Component<Props, {}> {
    render() {
        return <span>{this.props.foo}</span>
    }
}

<MyComponent foo="bar" />
```

### React JSX Tip：レンダリング可能なインターフェース

Reactは `JSX`や`string`のようなものをレンダリングすることができます。これらはすべて `React.ReactNode`型に統合されていますので、レンダラブルを受け入れる場合などに使用してください。

```ts
type Props = {
  header: React.ReactNode;
  body: React.ReactNode;
}
class MyComponent extends React.Component<Props, {}> {
    render() {
        return <div>
            {this.props.header}
            {this.props.body}
        </div>;
    }
}

<MyComponent foo="bar" />
```

### React JSXヒント：コンポーネントのインスタンスを受け入れる

反応型定義は、 `React.ReactElement <T>`を提供して、 `<T />`クラスコンポーネントのインスタンス化の結果に注釈を付けることができます。例えば

```js
class MyAwesomeComponent extends React.Component {
  render() {
    return <div>Hello</div>;
  }
}

const foo: React.ReactElement<MyAwesomeComponent> = <MyAwesomeComponent />; // Okay
const bar: React.ReactElement<MyAwesomeComponent> = <NotMyAwesomeComponent />; // Error!
```

> もちろん、これを関数の引数アノテーションやReact component prop memberとして使用することもできます。

### React JSXヒント：小道具に作用し、JSXを使用してレンダリングできる* component *を受け入れる

タイプ `React.Component <Props>`は `React.ComponentClass <P> |を統合します。 React.StatelessComponent <P> `で、`Props`型のJSXを使ってレンダリングするものを受け入れることができます。

```ts
const X: React.Component<Props> = foo; // from somewhere

// Render X with some props:
<X {...props}/>;
```

### React JSXヒント：汎用コンポーネント

期待どおりに動作します。次に例を示します。

```ts
/** A generic component */
type SelectProps<T> = { items: T[] }
class Select<T> extends React.Component<SelectProps<T>, any> { }

/** Usage */
const Form = () => <Select<string> items={['a','b']} />;
```

### 汎用関数

次のようなものがうまくいきます：

```ts
function foo<T>(x: T): T { return x; }
```

しかし、矢印汎用関数を使用しても、

```ts
const foo = <T>(x: T) => x; // ERROR : unclosed `T` tag
```

** 回避策**：ジェネリックパラメータに `extends`を使用すると、コンパイラがジェネリックであることをヒントできます。

```ts
const foo = <T extends {}>(x: T) => x;
```

### 型アサーション

我々が[前に述べた](./type-assertion.md#as-foo-vs-foo)のように、タイプアサーションには `as Foo`構文を使います。

## デフォルトの小道具

* デフォルトの小道具を持ったステートフルなコンポーネント：あなたは* Nullアサーション*演算子を使ってプロパティを外部から(Reactによって)提供することをTypeScriptに伝えることができます(これは理想的ではありませんが、 )。

```tsx
class Hello extends React.Component<{
  /**
   * @default 'TypeScript'
   */
  compiler?: string,
  framework: string
}> {
  static defaultProps = {
    compiler: 'TypeScript'
  }
  render() {
    const compiler = this.props.compiler!;
    return (
      <div>
        <div>{compiler}</div>
        <div>{this.props.framework}</div>
      </div>
    );
  }
}

ReactDOM.render(
  <Hello framework="React" />, // TypeScript React
  document.getElementById("root")
);
```

* デフォルトの小道具を備えたSFC：シンプルなJavaScriptパターンを活用することをお勧めします。

```tsx
const Hello: React.SFC<{
  /**
   * @default 'TypeScript'
   */
  compiler?: string,
  framework: string
}> = ({
  compiler = 'TypeScript', // Default prop
  framework
}) => {
    return (
      <div>
        <div>{compiler}</div>
        <div>{framework}</div>
      </div>
    );
  };


ReactDOM.render(
  <Hello framework="React" />, // TypeScript React
  document.getElementById("root")
);
```
