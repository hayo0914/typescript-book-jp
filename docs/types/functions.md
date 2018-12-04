* [パラメータ注釈]（#パラメータ注釈）
* [リターン型アノテーション]（#return-type-annotation）
* [オプションのパラメータ]（#オプションのパラメータ）
* [オーバーロード]（#オーバーロード）

## 関数
TypeScript型システムは、構成可能なシステムの核となるビルディングブロックであり、機能に多くの恩恵を払っています。

### パラメータの注釈
もちろん、他の変数に注釈を付けることができるように、関数のパラメータに注釈を付けることもできます。

```ts
// variable annotation
var sampleVariable: { bar: number }

// function parameter annotation
function foo(sampleParameter: { bar: number }) { }
```

ここでは、インライン型アノテーションを使用しました。もちろん、インターフェイスなどを使用することができます

### 戻り型アノテーション

戻り値の型には、変数に使用するのと同じスタイルの関数パラメータリストの後に注釈を付けることができます。 `：Foo`の例です：

```ts
interface Foo {
    foo: string;
}

// Return type annotated as `: Foo`
function foo(sample: Foo): Foo {
    return sample;
}
```

もちろん、ここでは「インターフェース」を使用しましたが、他の注釈を自由に使用できます。インライン注釈。

関数の戻り値の型をアノテートするためには、一般的にコンパイラが推論できるように*必要はありません。

```ts
interface Foo {
    foo: string;
}

function foo(sample: Foo) {
    return sample; // inferred return type 'Foo'
}
```

しかし、一般的には、これらのアノテーションを追加してエラーを助けるのが良い考えです。例：

```ts
function foo() {
    return { fou: 'John Doe' }; // You might not find this misspelling of `foo` till it's too late
}

sendAsJSON(foo());
```

関数から何かを返す予定がないなら、 `：void`と注釈を付けることができます。通常、 `：void`を落として推論エンジンに残すことができます。

### オプションのパラメータ
パラメータをオプションとしてマークすることができます：

```ts
function foo(bar: number, bas?: string): void {
    // ..
}

foo(123);
foo(123, 'hello');
```

あるいは、パラメータ宣言の後に `= someValue`を使用してデフォルト値を提供することもできます。これは、呼び出し元がその引数を提供しない場合に注入されます。

```ts
function foo(bar: number, bas: string = 'hello') {
    console.log(bar, bas);
}

foo(123);           // 123, hello
foo(123, 'world');  // 123, world
```

### オーバーロード
TypeScriptでは、関数のオーバーロードを宣言できます。これは、ドキュメント+型の安全性の目的に役立ちます。次のコードを考えてみましょう：

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

コードを注意深く見ると、 `a`、`b`、 `c`、d`の意味は、渡される引数の数に応じて変化することがわかります。関数は`1`、 `2`、または` `4`引数。これらの制約は、関数のオーバーロードを使用して*施行*および*文書化*することができます。関数ヘッダを複数回宣言するだけです。最後の関数ヘッダーは、関数本体内で実際にアクティブ*ですが、外界では使用できません。

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

もちろん、最終宣言（関数内部から見た真の宣言）はすべてのオーバーロードと互換性があることが重要です。これは、それが関数本体が本当に必要とする関数呼び出しの性質であるからです。

> TypeScriptの関数オーバーロードにランタイムオーバーヘッドはありません。関数が呼び出されると予想される方法を文書化するだけで、コンパイラはコードの残りの部分をチェックします。

[]（###宣言関数）
[]（オーバーラッピング宣言を可能にするインタフェースを持つラムダで）

[]（###型の互換性）
