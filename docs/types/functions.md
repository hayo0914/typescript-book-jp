## 関数
TypeScript型システムは、関数の機能に対して多くの愛を与えています。結局の所、関数は、構成可能なシステムの核となる建築ブロックです。

### パラメータの型アノテーション
もちろん、他の変数にアノテーションを付けることができるように、関数のパラメータにアノテーションを付けることもできます。

```ts
// variable annotation
var sampleVariable: { bar: number }

// function parameter annotation
function foo(sampleParameter: { bar: number }) { }
```

ここでは、インライン型アノテーションを使用しました。もちろん、インターフェイスなどを使用することができます

### 戻り値の型アノテーション

戻り値の型には、変数に使用するのと同じスタイルの関数パラメータリストの後にアノテーションを付けることができます。`: Foo`の例です：

```ts
interface Foo {
    foo: string;
}

// Return type annotated as `: Foo`
function foo(sample: Foo): Foo {
    return sample;
}
```

もちろん、ここではインターフェースを使用しましたが、他のアノテーション（インライン型アノテーションなど）を自由に使用できます。

コンパイラが型推論できる場合は、関数の戻り値の型アノテーションが必要ないことはよくあります。

```ts
interface Foo {
    foo: string;
}

function foo(sample: Foo) {
    return sample; // inferred return type 'Foo'
}
```

しかし、一般的には、これらのアノテーションを追加してエラー対処をしやすくする方が良い考えです。例：

```ts
function foo() {
    return { fou: 'John Doe' }; // You might not find this misspelling of `foo` till it's too late
}

sendAsJSON(foo());
```

関数から何かを返す予定がないなら、`:void`とアノテーションを付けることができます。通常、`:void`を書かずに型推論に任せることができます。

### オプションパラメータ
パラメータをオプションとしてマークすることができます：

```ts
function foo(bar: number, bas?: string): void {
    // ..
}

foo(123);
foo(123, 'hello');
```

あるいは、パラメータ宣言の後に `= someValue`を使用してデフォルト値を提供することもできます。これは、呼び出し元がその引数を提供しない場合に設定されます。

```ts
function foo(bar: number, bas: string = 'hello') {
    console.log(bar, bas);
}

foo(123);           // 123, hello
foo(123, 'world');  // 123, world
```

### オーバーロード
TypeScriptでは、関数のオーバーロードを宣言できます。これは、ドキュメントと型の安全性を高める目的に役立ちます。次のコードを考えてみましょう：

```ts
function padding(a: number, b?: number, c?: number, d?: any) {
    if (b === undefined && c === undefined && d === undefined) {
        b = c = d = a;
    }
    else if (c === undefined && d === undefined) {
        c = a;
        d = b;
    }
    return {
        top: a,
        right: b,
        bottom: c,
        left: d
    };
}
```

コードを注意深く見ると、 `a`、`b`、 `c`、`d`の意味は、渡される引数の数に応じて変化することがわかります。関数の引数は`1`、`2`、または`4`つです。これらの制約は、関数のオーバーロードを使用して強制と文書化を行うことができます。関数ヘッダを複数回宣言するだけです。最後の関数ヘッダーは、関数本体内で実際に有効なものですが、外部では使用できません。

これを以下に示します。

```ts
// Overloads
function padding(all: number);
function padding(topAndBottom: number, leftAndRight: number);
function padding(top: number, right: number, bottom: number, left: number);
// Actual implementation that is a true representation of all the cases the function body needs to handle
function padding(a: number, b?: number, c?: number, d?: number) {
    if (b === undefined && c === undefined && d === undefined) {
        b = c = d = a;
    }
    else if (c === undefined && d === undefined) {
        c = a;
        d = b;
    }
    return {
        top: a,
        right: b,
        bottom: c,
        left: d
    };
}
```

ここで最初の3つの関数ヘッダは `padding`への有効な呼び出しとして利用できます：

```ts
padding(1); // Okay: all
padding(1,1); // Okay: topAndBottom, leftAndRight
padding(1,1,1,1); // Okay: top, right, bottom, left

padding(1,1,1); // Error: Not a part of the available overloads
```

もちろん、最後の宣言(関数内部から見た真の宣言)はすべてのオーバーロードと互換性があることが重要です。これは、それが関数本体が本当に必要とする関数呼び出しの性質であるからです。

> TypeScriptの関数オーバーロードにランタイムでのオーバーヘッドはありません。関数が呼び出されると予想される方法を文書化し、コンパイラがコードの残りの部分をチェックするだけです。

### 関数の宣言

> 簡単なヒント: *型の定義*とは、既存の実装に対してあなたが型をどのように書くかということです。

具体的な実装を示さずに関数の型を*宣言する*方法には、2つの方法があります。以下に例を示します。

```ts
type LongHand = {
    (a: number): number;
};

type ShortHand = (a: number) => number;
```

上の2つの例は*完全に*同じ宣言です。違いがあるのは、関数のオーバーロードを行おうとする場合です。前者の長い書き方の宣言で定義したときのみ、以下のようにオーバーロードを追加できます。

```ts
type LongHandAllowsOverloadDeclarations = {
    (a: number): number;
    (a: string): string;
};
```
