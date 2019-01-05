# TypeScriptの型システム
[Why TypeScript？](../why-typescript.md)について説明したとき、TypeScriptの型システムの主な機能を取り上げました。下記は、改めて説明する必要がない、いくつかのキーポイントです：
* TypeScriptの型システムは*あなたのJavaScriptはTypeScriptである*ように、設計されています
* TypeScriptは型エラーがあってもJavaScript生成をブロックしないので、徐々にJSをTSに更新することができます

では、TypeScript型システムの構文から始めましょう。これにより、コード内でこれらのアノテーションをすぐに使用して、その利点を確認することができます。これは後で詳細を掘り下げる準備にもなります。

## 基本アノテーション
前述のように、`：TypeAnnotation`構文を使って型アノテーションを書きます。型宣言空間で使用可能なものは、型アノテーションとして使用できます。

次の例は、変数、関数パラメータ、および関数戻り値の型アノテーションを示しています。

```
var num: number = 123;
function identity(num: number): number {
    return num;
}
```

### プリミティブ型(Primitive Types)
JavaScriptプリミティブ型は、TypeScript型システムでカバーしています。これは、以下に示すように `string`、`number`、 `boolean`を意味します：

```ts
var num: number;
var str: string;
var bool: boolean;

num = 123;
num = 123.456;
num = '123'; // Error

str = '123';
str = 123; // Error

bool = true;
bool = false;
bool = 'false'; // Error
```

### 配列(Arrays)
TypeScriptは、配列に専用の構文を提供し、コードにアノテーションを付けて文書化するのを容易にします。構文は、基本的に`[]`を有効な型アノテーション(例えば `：boolean[]`)に後置します。これは通常行う配列操作を安全に行うことを可能にし、誤った型のメンバを割り当てるなどのエラーからあなたを守ります。これは以下のとおりです：

```ts
var boolArray: boolean[];

boolArray = [true, false];
console.log(boolArray[0]); // true
console.log(boolArray.length); // 2
boolArray[1] = true;
boolArray = [false, false];

boolArray[0] = 'false'; // Error!
boolArray = 'false'; // Error!
boolArray = [true, 'false']; // Error!
```

### インターフェース(Interfaces)
インターフェースは、複数の型アノテーションを単一の名前付きアノテーションに合成するための、TypeScriptにおける主要な方法です。次の例を考えてみましょう。

```ts
interface Name {
    first: string;
    second: string;
}

var name: Name;
name = {
    first: 'John',
    second: 'Doe'
};

name = {           // Error : `second` is missing
    first: 'John'
};
name = {           // Error : `second` is the wrong type
    first: 'John',
    second: 1337
};
```

ここでは、アノテーションを`first：string`+`second：string`という新しいアノテーション`Name`にまとめて、個々のメンバの型チェックを行います。インターフェースはTypeScriptで大きなパワーを持っているので、別途専用のセクションでその利点をどのように活かすかを説明します。

### インライン型アノテーション(Inline Type Annotation)
新しい`interface`を作成するのではなく、構造`：{/* Structure */}`を使って*インライン*で必要なものにアノテーションを付けることができます。前の例を、インライン型で再掲します：

```ts
var name: {
    first: string;
    second: string;
};
name = {
    first: 'John',
    second: 'Doe'
};

name = {           // Error : `second` is missing
    first: 'John'
};
name = {           // Error : `second` is the wrong type
    first: 'John',
    second: 1337
};
```

インライン型は、１回だけ使うようなアノテーションを素早く提供するのに最適です。それは(良くないかもしれない)型名を考える手間を省きます。しかし、同じ型アノテーションを複数回インラインで入れている場合は、それをインターフェース(またはこのセクションの後半で説明する`type alias`)にリファクタリングすることを検討することをお勧めします。

## 特殊な型
上記でカバーしたプリミティブ型以外にも、TypeScriptでは特別な意味を持ついくつかの型があります。これらは`any`、`null`、`undefined`、`void`です。

### any
`any`型は、TypeScript型システムにおいて特別なものです。これは、型システムからの脱出口を与えて、コンパイラに失せるよう指示します。`any`は型システムの全ての型と互換性があります。これは、*何かをそれに代入できる*ことを意味します。それは何でも代入することができます。以下に例を示します:

```ts
var power: any;

// Takes any and all types
power = '123';
power = 123;

// Is compatible with all types
var num: number;
power = num;
num = power;
```

JavaScriptコードをTypeScriptに移植する場合、最初は`any`と友達になります。しかし、型安全性を確保することはあなた次第であるため、この友情を真剣に受け止めてはいけません。これを使うことは、基本的に、コンパイラに意味のある静的解析を行わないように指示することです。

### `null`と`undefined`

`null`と`undefined`のJavaScriptリテラルは、型システムにおいて`any`型の何かと同じように扱われます。これらのリテラルは他のタイプに割り当てることができます。これは以下の例で示されます：

```ts
var num: number;
var str: string;

// These literals can be assigned to anything
num = null;
str = undefined;
```

### `：void`
関数に戻り値の型がないことを示すには`：void`を使います：

```ts
function log(message): void {
    console.log(message);
}
```

## ジェネリックス(Generics)
コンピュータサイエンスの多くのアルゴリズムとデータ構造は、オブジェクトの実際の型に依存しません。しかし、それでも、あなたは、さまざまな変数の間で制約を適用したいと考えているでしょう。単純なおもちゃの例は、項目のリストを取り、逆の項目のリストを返す関数です。ここでの制約は、関数に渡されるものと関数によって返されるものの間の制約です。

```ts
function reverse<T>(items: T[]): T[] {
    var toreturn = [];
    for (let i = items.length - 1; i >= 0; i--) {
        toreturn.push(items[i]);
    }
    return toreturn;
}

var sample = [1, 2, 3];
var reversed = reverse(sample);
console.log(reversed); // 3,2,1

// Safety!
reversed[0] = '1';     // Error!
reversed = ['1', '2']; // Error!

reversed[0] = 1;       // Okay
reversed = [1, 2];     // Okay
```

ここでは、`reverse`関数は何らかの型`T`の配列(`items：T []`)を受け取り(`reverse<T>`の型パラメータに注目)、`T`型の配列を返します(注目：`T []`)。 `reverse`関数は、同じ型の項目を返すので、`reversed`変数も`number []`型であることがTypeScriptに分かるため、型の安全性が得られます。同様に`string []`の配列を`reverse`関数に渡すと、返される結果も`string []`の配列になり、以下に示すような型安全性が得られます：

```ts
var strArr = ['1', '2'];
var reversedStrs = reverse(strArr);

reversedStrs = [1, 2]; // Error!
```

実際、JavaScript配列には既に`.reverse`関数があり、TypeScriptはジェネリックを使ってその構造を定義しています：

```ts
interface Array<T> {
 reverse(): T[];
 // ...
}
```

これは、以下のように任意の配列で `.reverse`を呼び出すときに型の安全性を得られることを意味します：

```ts
var numArr = [1, 2];
var reversedNums = numArr.reverse();

reversedNums = ['1', '2']; // Error!
```

後で、**アンビエント宣言**(Ambient Declarations)の節で`lib.d.ts`を説明するときに、`Array <T>`インターフェースについてもっと議論します。

## ユニオン型(Union Type)
JavaScriptでは多くの場合、プロパティを複数の型のうちの1つにする必要があります(例:`string`または`number`)。これは、*ユニオン型*(型アノテーションの`|`を使い`string | number`のように書く)が便利な場所です。一般的な使用例は、単一のオブジェクトまたはオブジェクトの配列をとることができる関数です。

```ts
function formatCommandline(command: string[]|string) {
    var line = '';
    if (typeof command === 'string') {
        line = command.trim();
    } else {
        line = command.join(' ').trim();
    }

    // Do stuff with line: string
}
```

## 交差型(Intersection Type)
`オブジェクト拡張`(extend)はJavaScriptで非常に一般的なパターンです。ここでは2つのオブジェクトを取得し、これらのオブジェクトの両方の機能を持つ新しいオブジェクトを作成します。**交差型**では、以下に示すようにこのパターンを安全な方法で使用できます。

```ts
function extend<T, U>(first: T, second: U): T & U {
    let result = <T & U> {};
    for (let id in first) {
        result[id] = first[id];
    }
    for (let id in second) {
        if (!result.hasOwnProperty(id)) {
            result[id] = second[id];
        }
    }
    return result;
}

var x = extend({ a: "hello" }, { b: 42 });

// x now has both `a` and `b`
var a = x.a;
var b = x.b;
```

## タプル型
JavaScriptには、第一級のタプルのサポートがありません。人々は、一般にタプルとして配列を使用します。これはまさにTypeScriptの型システムがサポートしているものです。タプルは、`： [typeofmember1, typeofmember2]`などを使ってアノテーションを付けることができます。タプルには、任意の数のメンバを含めることができます。タプルの例:

```ts
var nameNumber: [string, number];

// Okay
nameNumber = ['Jenny', 8675309];

// Error!
nameNumber = ['Jenny', '867-5309'];
```

これをTypeScriptの非構造化サポートと組み合わせると、タプルは配列であってもかなり第一級的だと感じます：

```ts
var nameNumber: [string, number];
nameNumber = ['Jenny', 8675309];

var [name, num] = nameNumber;
```

## 型エイリアス(Type Alias)
TypeScriptは、複数の場所で使用したい型アノテーションの名前を提供するための便利な構文を提供します。エイリアスは `type SomeName = someValidTypeAnnotation`構文を使用して作成できます。例:

```ts
type StrOrNum = string|number;

// Usage: just like any other notation
var sample: StrOrNum;
sample = 123;
sample = '123';

// Just checking
sample = true; // Error!
```

`interface`とは違って、文字通り、型アノテーションに型エイリアスを与えることができます(ユニオン型や交差型のようなものに便利です)。構文に慣れ親しむための例をいくつか次に示します。

```ts
type Text = string | { text: string };
type Coordinates = [number, number];
type Callback = (data: string) => void;
```

> ヒント： 型アノテーションの階層を持つ必要がある場合は、`interface`を使います。インターフェースは`implements`と`extends`で使うことができます

> ヒント：より単純なオブジェクト構造(`Coordinates`(座標)のような)のために、型名を使ってセマンティックな名前を付けるだけです。また、ユニオン型や交差型にセマンティクス名を付ける場合は、型エイリアスを使用します。

## まとめ
これで、ほとんどのJavaScriptコードに型アノテーションを付けることができるようになりました。これで、TypeScriptの型システムで使用可能なすべての機能の詳細を説明できます。
