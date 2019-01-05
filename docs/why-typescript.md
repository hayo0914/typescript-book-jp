# なぜTypeScriptか？
TypeScriptの主要なゴールは2つです。
* JavaScriptに*オプショナルな型システム*を提供します
* 将来のJavaScriptで計画されている機能を現在のJavaScriptエンジンに提供します

これらのゴールへの希求は以下に述べる理由によって動機づけられています。

## TypeScriptの型システム(type system)

「**JavaScriptに型を追加する理由は？**」と不思議に思うかもしれません。

型は、コードの品質と理解容易性を高めることが実証されています。大規模なチーム(Google、Microsoft、Facebook)は、常に、この結論に至っています。具体的には：

* 型は、リファクタリングを行う際の開発速度を高めます。*コンパイルの時点でエラーを検出する方が、ランタイムでの実行時にエラーが発生するよりも優れています*
* 型は、完璧なドキュメントです。*関数のシグネチャは定理であり、関数の本体は証明です*

しかし、型には過剰に儀式的な面があります。TypeScriptは、次に述べるように、型を導入する障壁を可能な限り低くしています。

### あなたの書いたJavaScriptはTypeScriptです
TypeScriptは、JavaScriptコードのコンパイル時の型安全性を提供します。その名前はこれを表しています。素晴らしい点は、型の使用が完全に任意（オプション）であることです。あなたのJavaScriptコード`.js`ファイルを`.ts`ファイルに名前を変更したとしても、TypeScriptは元のJavaScriptファイルと同じ有効な`.js`を返します。TypeScriptは意図的かつ厳密なJavaScriptのスーパーセットであり、任意の型チェック機構を持ったプログラミング言語です。

### 暗黙的な型推論(type inference)
TypeScriptは、生産性へのコストを最小限に抑えて型の安全性を提供するために、可能な限り、型推論を行います。たとえば、次の例では、TypeScriptはfooの型が`number`であると推測し、2行目のコードにエラーを表示します。

```ts
var foo = 123;
foo = '456'; // Error: cannot assign `string` to `number`

// Is foo a number or a string?
```
型推論を必要とする大きな理由があります。この例のようなコードを書いた場合、残りのコードにおいて`foo`が`number`であるか`string`であるかを確定できません。この問題は、大規模なコードベースで頻繁に勃発します。後で型推論のルールの詳細を説明します。

### 明示的な型(type annotation)
これまで述べたように、TypeScriptは安全に行える場合は可能な限り型推論を行います。しかし、注釈(型アノテーション)を記述することによって、以下のメリットが得られます:

1. あなたの書いたコードを次に読まなくてはならない開発者のためのドキュメントを補強する(将来のあなたかもしれない!)
1. コンパイラがどのように理解するかを強制する。つまり、コードに対するあなたの理解が、コンパイラのアルゴリズムによる分析結果と一致する

TypeScriptは、他の任意な型付き言語(ActionScriptやF#など)で一般的な後置タイプの型アノテーション(Postfix type annotation)を使用します。

```ts
var foo: number = 123;
```

何か間違っていると、コンパイラはエラーを表示します：

```ts
var foo: number = '123'; // Error: cannot assign a `string` to a `number`
```

TypeScriptでサポートされている型アノテーションの詳細については、今後のチャプターで説明します。

### 構造的部分型(structural typing)
いくつかの言語(特に型付き言語と呼ばれるもの)において、静的な型付けは、過剰に冗長なコードになってしまいます。なぜならコードが正常に動作することを確信できていたとしても、構文ルールがあたり一面に同じコードをコピー＆ペーストすることを強制するからです。C#の[automapper for C#](http://automapper.org/)のようなものが必要になる理由です。TypeScriptは、JavaScript開発者にとって、コードの可読性に対する悪影響を最小限に抑え、簡単に型を使えるようにしたいので、構造的部分型(structural typing)を採用しています。これは、ダックタイピング(duck typing)が、ファーストクラスの言語機構であることを意味します。次の例を考えてみましょう。関数`iTakePoint2D`は、期待する全てのメンバ(例では、`x`と `y`)を含む構造は、何でも受け入れます：

```ts
interface Point2D {
    x: number;
    y: number;
}
interface Point3D {
    x: number;
    y: number;
    z: number;
}
var point2D: Point2D = { x: 0, y: 10 }
var point3D: Point3D = { x: 0, y: 10, z: 20 }
function iTakePoint2D(point: Point2D) { /* do something */ }

iTakePoint2D(point2D); // exact match okay
iTakePoint2D(point3D); // extra information okay
iTakePoint2D({ x: 0 }); // Error: missing information `y`
```

### 型エラーがあってもJavaScriptは出力される
JavaScriptのコードをTypeScriptに移行することを簡単にするため、デフォルトでは、コンパイルエラーがあったとしても、TypeScriptは有効なJavaScriptを出力します。例:

```ts
var foo = 123;
foo = '456'; // Error: cannot assign a `string` to a `number`
```

次のjsを出力します：

```ts
var foo = 123;
foo = '456';
```

そのため、JavaScriptコードを段階的にTypeScriptへの移行を行うことができます。これは他の言語のコンパイラの動作とは全く異なっており、そして、TypeScriptに移行する理由の1つです。

### 型による開発環境へのメリット
TypeScriptの設計における大きなゴールは、TypeScriptで既存のJavaScriptライブラリを安全かつ簡単に利用できることです。TypeScriptはこれを型宣言(declaration)で行います。TypeScriptにおいて、型宣言にどれくらいの労力をかけるかは調整可能です。より多くの労力をかければ、より多くの型安全性とIDEによるコード補完(code intelligence)が手に入ります。メジャーなJavaScriptライブラリの型定義は、[DefinitelyTyped community](https://github.com/borisyankov/DefinitelyTyped)によって既に作成されているため、

1. 定義ファイルが既に存在する
1. あるいは、最低でも、きちんとレビューされた多くのTypeScript宣言のテンプレートが既に利用可能である

独自の型宣言ファイルを作成する短い例として、[jquery](https://jquery.com/)の簡単な例を考えてみましょう。TypeScriptは、デフォルト設定において(望ましいJavaScriptコードのように)、変数を使う前に宣言する(つまり、どこかで`var`を使う)ことを期待しています。
```ts
$('.awesome').show(); // Error: cannot find name `$`
```
簡単な修正方法は、変数`$`が実際に存在することをTypeScriptに伝えることです。
```ts
declare var $: any;
$('.awesome').show(); // Okay!
```

必要に応じて、より多くの詳細を記述し、あなた自身をプログラミングのエラーから守ることができます。
```ts
declare var $: {
    (selector:string): any;
};
$('.awesome').show(); // Okay!
$(123).show(); // Error: selector needs to be a string
```

TypeScriptの詳細を理解した後で、既存のJavaScriptコードのTypeScript定義に関して詳しく説明します(`interface`や`any`など)。

## Future JavaScript => Now
TypeScriptは、現在のJavaScriptエンジン(ES5のみをサポートする)に対して、ES6以降で計画されている多くの機能を提供します。TypeScriptチームは積極的に機能を追加しています。機能の一覧は時間とともに増えていく予定です。これらについては独自の章で説明します。ただのサンプルとしてクラスの例を提示しておきます:

```ts
class Point {
    constructor(public x: number, public y: number) {
    }
    add(point: Point) {
        return new Point(this.x + point.x, this.y + point.y);
    }
}

var p1 = new Point(0, 10);
var p2 = new Point(10, 20);
var p3 = p1.add(p2); // { x: 10, y: 30 }
```

それと、かわいい太っちょのアロー関数:

```ts
var inc = x => x+1;
```

### 要約
この章では、TypeScriptを使う動機とTypeScriptの設計ゴールを説明しました。これで、TypeScriptの微に入り細を穿つ詳細の説明を行うことができます。

[](Interfaces are open ended)
[](Type Inferernce rules)
[](Cover all the annotations)
[](Cover all ambients : also that there are no runtime enforcement)
[](.ts vs. .d.ts)
