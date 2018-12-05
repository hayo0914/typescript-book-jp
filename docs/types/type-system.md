# タイプスクリプトタイプシステム
[Why TypeScript？](../ why-typescript.md)について説明したとき、TypeScript Type Systemの主な機能を取り上げました。次の説明は、その説明からのさらなる説明を必要としないいくつかの主要な取り組みです：
* typescriptの型システムは* javascriptがtypescript *になるように*オプションです*ように設計されています。
* TypeScriptはType Errorsの存在下で* JavaScript emit *をブロックしないので、JSをTS *に徐々に更新することができます。

では、TypeScript型システムの*構文*から始めましょう。これにより、コード内でこれらの注釈をすぐに使用して、その利点を確認することができます。これは後でより深い潜水を準備します。

## 基本アノテーション
前述のように、型は `：TypeAnnotation`構文を使って注釈されます。型宣言空間で使用可能なものは、型注釈として使用できます。

次の例は、変数、関数パラメータ、および関数戻り値の型の注釈を示しています。

```
var num: number = 123;
function identity(num: number): number {
    return num;
}
```

### プリミティブ型
JavaScriptプリミティブ型は、TypeScript型システムでよく表現されています。これは、以下に示すように `string`、`number`、 `boolean`を意味します：

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

### 配列
TypeScriptは、配列に専用の構文を提供し、コードに注釈を付けて文書化するのを容易にします。構文は、基本的に `[]`を有効な型の注釈(例えば `：boolean []`)に後置します。これは通常行う配列操作を安全に行うことを可能にし、誤った型のメンバを割り当てるなどのエラーからあなたを守ります。これは以下のとおりです：

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

### インターフェイス
インターフェイスは、複数のタイプの注釈を単一の名前付き注釈に合成するための、TypeScriptの中心的な方法です。次の例を考えてみましょう。

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

ここでは、アノテーションを `first：string`+` second：string`という新しいアノテーション `Name`にまとめて、個々のメンバのタイプチェックを行います。インターフェイスはTypeScriptで多くのパワーを持っており、セクション全体をあなたの利点にどのように使うことができるかということに専念します。

### インライン型注釈
新しい `interface`を作成するのではなく、`：{/ * Structure * /} `を使って*インライン*で必要なものに注釈を付けることができます。前の例は、インライン型を再び示しました：

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

インラインタイプは、何かのためのワンタッチアノテーションを素早く提供するのに最適です。それは(潜在的に悪い)型名を考え出す手間を省きます。しかし、同じタイプの注釈を複数回インラインで入れている場合は、それをインターフェース(またはこのセクションの後半で説明する `type alias ')にリファクタリングすることを検討することをお勧めします。

## 特殊なタイプ
カバーされているプリミティブ型以外にも、TypeScriptでは特別な意味を持ついくつかの型があります。これらは `any`、`null`、 `undefined`、`void`です。

### どれか
`any`型は、TypeScript型システムにおいて特別な場所を保持します。これは、タイプシステムからのエスケープハッチを与えて、コンパイラにバグを告げるように指示します。 `any`は型システムの* any型とall型と互換性があります。これは、*何かをそれに割り当てることができることを意味します。*それは何にでも割り当てることができます*。これは以下の例で実証されています：

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

JavaScriptコードをTypeScriptに移植する場合、最初は `any`と親しい友人になります。しかし、タイプセーフティを確保することはあなた次第であるため、この友情を真剣に受け止めてはいけません。基本的にコンパイラに意味のある静的解析*を行わないように指示しています。

### ``ヌル `と` `未定義` `

`null`と`undefined` JavaScriptリテラルは、 `any`型のものと同じ型システムによって効果的に扱われます。これらのリテラルは他のタイプに割り当てることができます。これは以下の例で示されます：

```ts
var num: number;
var str: string;

// These literals can be assigned to anything
num = null;
str = undefined;
```

### `：void`
関数に戻り値の型がないことを示すには `：void`を使います：

```ts
function log(message): void {
    console.log(message);
}
```

## ジェネリックス
コンピュータサイエンスの多くのアルゴリズムとデータ構造は、オブジェクトの実際のタイプ*に依存しません。しかし、いまだにさまざまな変数の間で制約を適用したいと思っています。単純なおもちゃの例は、項目のリストを取り、逆の項目のリストを返す関数です。ここでの制約は、関数に渡されるものと関数によって返されるものの間の制約です。

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

ここでは、 `reverse`関数は* some *型`T`の配列( `items：T []`)( `reverse <T>`の型パラメータに注意してください)を取り、型の配列を返します`T`(注意：`T [] `)。 `reverse`関数は、同じ型の項目を返すので、`reversed`変数も `number []`型であることを知り、型の安全性を与えます。同様に `string []`の配列をリバース関数に渡すと、返される結果も `string []`の配列になり、以下に示すような型安全性が得られます：

```ts
var strArr = ['1', '2'];
var reversedStrs = reverse(strArr);

reversedStrs = [1, 2]; // Error!
```

実際、JavaScript配列には既に `.reverse`関数があり、TypeScriptは実際にその構造を定義するためにジェネリックを使用します：

```ts
interface Array<T> {
 reverse(): T[];
 // ...
}
```

これは、以下のように任意の配列で `.reverse`を呼び出すときに型の安全性を得ることを意味します：

```ts
var numArr = [1, 2];
var reversedNums = numArr.reverse();

reversedNums = ['1', '2']; // Error!
```

後で、 `Ambient Declarations ** 'の節で`lib.d.ts`を提示するときに、 `Array <T>'インターフェースについてもっと議論します。

## ユニオンタイプ
JavaScriptでは多くの場合、プロパティを複数のタイプのうちの1つにする必要があります。 * `string`または`number` *です。これは、* union type *(型アノテーションの `|`で示される `string | number`)が便利な場所です。一般的な使用例は、単一のオブジェクトまたはオブジェクトの配列をとることができる関数です。

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

## 交差点タイプ
`extend`はJavaScriptで非常に一般的なパターンです。ここでは2つのオブジェクトを取得し、これらのオブジェクトの両方の機能を持つ新しいオブジェクトを作成します。 ** Intersection Type **では、以下に示すようにこのパターンを安全な方法で使用できます。

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

## タプルタイプ
JavaScriptには、ファーストクラスタプルのサポートがありません。人々は一般にタプルとして配列を使用します。これはまさにTypeScript型システムがサポートしているものです。タプルは、 `：[typeofmember1、typeofmember2]`などを使って注釈を付けることができます。タプルには、任意の数のメンバを含めることができます。タプルは以下の例で示されます：

```ts
var nameNumber: [string, number];

// Okay
nameNumber = ['Jenny', 8675309];

// Error!
nameNumber = ['Jenny', '867-5309'];
```

これをTypeScriptの非構造化サポートと組み合わせると、タプルは配列の下にあってもかなりファーストクラスだと感じます：

```ts
var nameNumber: [string, number];
nameNumber = ['Jenny', 8675309];

var [name, num] = nameNumber;
```

## 型エイリアス
TypeScriptは、複数の場所で使用したいタイプ注釈の名前を提供するための便利な構文を提供します。エイリアスは `type SomeName = someValidTypeAnnotation`構文を使用して作成されます。例を以下に示します。

```ts
type StrOrNum = string|number;

// Usage: just like any other notation
var sample: StrOrNum;
sample = 123;
sample = '123';

// Just checking
sample = true; // Error!
```

`interface`とは違って、文字通り型アノテーションに型エイリアスを与えることができます(共用体や交差型のようなものに便利です)。構文に慣れ親しむための例をいくつか次に示します。

```ts
type Text = string | { text: string };
type Coordinates = [number, number];
type Callback = (data: string) => void;
```

> ヒント：Typeアノテーションの階層を持つ必要がある場合は、 `interface`を使います。それらは `implements`と`extends`で使うことができます

> ヒント：より単純なオブジェクト構造( `Coordinates`のような)のために、型名を使ってセマンティックな名前を付けるだけです。また、連合型や交差型にセマンティクス名を付ける場合は、型エイリアスを使用します。

## まとめ
これで、ほとんどのJavaScriptコードに注釈を付けることができるようになりました。これは、TypeScriptのタイプシステムで使用可能なすべての機能の詳細にジャンプできます。
