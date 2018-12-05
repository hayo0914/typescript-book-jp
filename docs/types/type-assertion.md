## 型アサーション
TypeScriptを使用すると、推論して分析したタイプのビューを任意の方法で上書きできます。これは、「型アサーション」と呼ばれるメカニズムによって行われます。 TypeScriptの型アサーションは、あなたが型よりも優れていることをコンパイラに伝えているだけでなく、後で推測するべきではないことをコンパイラに伝えています。

タイプアサーションの一般的な使用例は、JavaScriptからTypeScriptへコードを移植する場合です。たとえば、次のパターンを考えてみましょう。

```ts
var foo = {};
foo.bar = 123; // Error: property 'bar' does not exist on `{}`
foo.bas = 'hello'; // Error: property 'bas' does not exist on `{}`
```

ここでコードエラーは、 `foo`の*推論された*型が`{} `である、すなわちプロパティがゼロのオブジェクトです。したがって、 `bar`や`bas`を追加することはできません。これは、単純に型アサーション `as Foo`で修正することができます：

```ts
interface Foo {
    bar: number;
    bas: string;
}
var foo = {} as Foo;
foo.bar = 123;
foo.bas = 'hello';
```

### ``foo`と `<foo>`の違い
もともと追加された構文は `<foo>`でした。これは以下のとおりです：

```ts
var foo: any;
var bar = <string> foo; // bar is now of type "string"
```

しかし、JSXで `<foo>`スタイルアサーションを使用する場合、言語文法にあいまいさがあります。

```ts
var foo = <string>bar;
</string>
```

したがって、一貫性のために `as foo`を使うことをお勧めします。

### 型アサーションとキャスト
それが「型キャスト」と呼ばれない理由は、*キャスティング*は一般的に何らかのランタイムサポートを意味するからです。しかし、*型アサーション*は純粋にコンパイル時の構造体であり、コードをどのように解析するかについてのヒントをコンパイラに提供する方法です。

### アサーションは有害であるとみなす
多くの場合、アサーションを使用すると、従来のコードを簡単に移行したり、コードベースにコードサンプルを貼り付けたりすることもできますが、アサーションの使用には注意が必要です。オリジナルのコードをサンプルとして、コンパイラは約束したプロパティを実際に追加するのを忘れることからあなたを守りません*：

```ts
interface Foo {
    bar: number;
    bas: string;
}
var foo = {} as Foo;
// ahhhh .... forget something?
```

また、別の一般的な考え方として、* autocomplete *を提供する手段としてアサーションを使用しています。

```ts
interface Foo {
    bar: number;
    bas: string;
}
var foo = <Foo>{
    // the compiler will provide autocomplete for properties of Foo
    // But it is easy for the developer to forget adding all the properties
    // Also this code is likely to break if Foo gets refactored (e.g. a new property added)
};
```

コンパイラが不平を言っていないプロパティを忘れた場合、ここの危険は同じです。あなたが次のことをするのはより良いことです：

```ts
interface Foo {
    bar: number;
    bas: string;
}
var foo:Foo = {
    // the compiler will provide autocomplete for properties of Foo
};
```

場合によっては、一時変数を作成する必要があるかもしれませんが、少なくとも(おそらくfalse)約束をしておらず、代わりに型推論に頼ってあなたのためのチェックを行います。

### ダブルアサーション
タイプアサーションは、私たちが示したように少し安全ではありませんが、完全にオープンシーズン*ではありません。例えば。以下は非常に有効なユースケースです(たとえば、ユーザーが渡されたイベントはイベントのより具体的なケースと考えられます)、タイプアサーションは期待通りに機能します。

```ts
function handler (event: Event) {
    let mouseEvent = event as MouseEvent;
}
```

ただし、次のようなエラーが発生する可能性が最も高く、ユーザーのタイプアサーションにもかかわらず、TypeScriptがこのように表示されます。

```ts
function handler(event: Event) {
    let element = event as HTMLElement; // Error: Neither 'Event' nor type 'HTMLElement' is assignable to the other
}
```

あなたが*その型を依然として必要とするなら、二重アサーション*を使うことができますが、最初にすべての型と互換性のある `any`をアサートするので、コンパイラはもう文句を言うことはありません：

```ts
function handler(event: Event) {
    let element = event as any as HTMLElement; // Okay!
}
```

#### typescriptが単一のアサーションで十分でないかどうかを判断する方法
基本的に、 `S`が`T`のサブタイプであるか `T`が`S`のサブタイプである場合、 `S`から`T`へのアサーションは成功します。これは、タイプアサーションを行う際に特別な安全性を提供するためです。完全にワイルドなアサーションは非常に安全ではない可能性があり、 `any`を使用して安全でないものにする必要があります。
