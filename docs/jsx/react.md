# React JSX

> [Type ScriptとReactのPRO Eggheadコース](https://egghead.io/courses/use-typescript-to-develop-react-applications)

## セットアップ

私たちの[ブラウザ向けのクイックスタートに、すでにReactアプリケーションの開発のセットアップの仕方を説明しています](../quick/browser.md)。主なハイライトは次の通りです。

* ファイル拡張子`.tsx`(`.ts`の代わりに)を使用してください。
* あなたの`tsconfig.json`の`compilerOptions`で `"jsx" ： "react"を使ってください。
* JSXとReactの定義をあなたのプロジェクトにインストールします：(`npm i -D @types/react @types/react-dom`)。
* reactを`.tsx`ファイルにインポートします(`import * as React from "react"`となります)。

## HTMLタグとComponentの違い

Reactは、HTMLタグ(文字列)またはReact Component(クラス)をレンダリングします。これらに対するJavaScriptの出力は異なります(`React.createElement( 'div')`と`React.createElement(MyComponent)`)。これが決まる方法は最初の文字の*ケース*(大文字小文字)です。`foo`はHTMLタグとして扱われ、`Foo`はコンポーネントとして扱われます。

## 型チェック(Type Checking)

### HTMLタグ

HTMLタグ`foo`の型は`JSX.IntrinsicElements.foo`です。これらの型は、セットアップの一部としてインストールした`react-jsx.d.ts`ファイルにおいて主要なタグに対してすでに定義されています。次に、ファイルの内容のサンプルを示します。

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

### ステートレスな関数コンポーネント(Stateless Functional Components)

あなたは単に`React.SFC`インターフェースを使ってステートレスなコンポーネントを定義することができます。

```ts
type Props = {
  foo: string;
}
const MyComponent: React.SFC<Props> = (props) => {
    return <span>{props.foo}</span>
}

<MyComponent foo="bar" />
```

### ステートフルなコンポーネント(Stateful Components)

コンポーネントは、コンポーネントの`props`プロパティに基づいて型チェックされます。これは、JSXがどのように変換されるかによってモデル化されています。例えば属性がコンポーネントの`props`になるようにモデル化されています。

ReactのStatefulコンポーネントを作成するには、ES6クラスを使用します。`react.d.ts`ファイルはあなた自身の`Props`と`State`インターフェースを提供する、あなたのクラスで継承するべき`React.Component<Props,State>`クラスを定義しています。これは以下のとおりです：

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

### React JSX Tip： レンダリング可能なインターフェース

Reactは`JSX`や`string`のようなものをレンダリングすることができます。これらはすべて`React.ReactNode`型に統合されていますので、レンダリング可能なものを受け入れる場合などに使用してください。

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

React型の定義は、`React.ReactElement<T>`を提供しており、`<T/>`クラスコンポーネントのインスタンスにアノテーションを付けることができます。例えば

```js
class MyAwesomeComponent extends React.Component {
  render() {
    return <div>Hello</div>;
  }
}

const foo: React.ReactElement<MyAwesomeComponent> = <MyAwesomeComponent />; // Okay
const bar: React.ReactElement<MyAwesomeComponent> = <NotMyAwesomeComponent />; // Error!
```

> もちろん、これを関数の引数のアノテーションやReact componentのprop memberとして使用することもできます。

### React JSXヒント： propに作用し、JSXを使用してレンダリングできる*Component*を受け入れる

型`React.Component<Props>`は`React.ComponentClass<P> | React.StatelessComponent<P>`を統合しています。なので、`Props`型を受け取り、JSXを使ってレンダリングする*何か*を受け入れることができます。

```ts
const X: React.Component<Props> = foo; // from somewhere

// Render X with some props:
<X {...props}/>;
```

### React JSXヒント：ジェネリックコンポーネント(Generic Components)

期待どおりに動作します。次に例を示します。

```ts
/** A generic component */
type SelectProps<T> = { items: T[] }
class Select<T> extends React.Component<SelectProps<T>, any> { }

/** Usage */
const Form = () => <Select<string> items={['a','b']} />;
```

### ジェネリック関数(Generic Functions)

次のようなものがうまくいきます：

```ts
function foo<T>(x: T): T { return x; }
```

しかし、アローのジェネリック関数を使用しても、うまくいきません:

```ts
const foo = <T>(x: T) => x; // ERROR : unclosed `T` tag
```

**回避策**：ジェネリックパラメータに`extends`を使用すると、コンパイラがジェネリックであることを教えられます。

```ts
const foo = <T extends {}>(x: T) => x;
```

### Reactのヒント: React Tip: 厳密に型付けされた参照(Strongly Typed Refs)

あなたは基本的に参照のユニオンとして変数を`null`で初期化できます。そしてそれをコールバックとして初期化できます。
```ts
class Example extends React.Component {
  example() {
    // ... something
  }

  render() { return <div>Foo</div> }
}


class Use {
  exampleRef: Example | null = null; 

  render() {
    return <Example ref={exampleRef => this.exampleRef = exampleRef } />
  }
}
```
そしてネイティブ要素の参照に対しても同じです。
```ts
class FocusingInput extends React.Component<{ value: string, onChange: (value: string) => any }, {}>{
  input: HTMLInputElement | null = null;

  render() {
    return (
      <input
        ref={(input) => this.input = input}
        value={this.props.value}
        onChange={(e) => { this.props.onChange(this.ctrls.input.value) } }
        />
      );
    }
    focus() {
      if (this.input != null) { this.input.focus() }
    }
}
```

### 型アサーション(Type Assertions)

我々が [前に述べた](./type-assertion.md#as-foo-vs-foo) のように、型アサーションには`as Foo`構文を使います。

## デフォルトProps(Default Props)

* デフォルトPropsを持ったステートフルなコンポーネント：あなたは*Nullアサーション演算子*を使って、プロパティが外部から(Reactによって)提供されることをTypeScriptに伝えることができます(これは理想的ではありませんが、しかし私が思いつく中では、最もシンプルでミニマムなコードです)。

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

* デフォルトPropsを備えたSFC ：シンプルなJavaScriptパターンを活用してTypeScriptの型システムとうまく動作するようにすることをお勧めします。

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
