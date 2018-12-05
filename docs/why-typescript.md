# なぜTypeScriptか？
TypeScriptの主な目的は2つあります。
* JavaScriptの*オプション*を提供します。
* 将来のJavaScriptのエディションで計画されている機能を現在のJavaScriptエンジンに提供します

これらのゴールへの願望は下記によって動機づけられています。

## TypeScriptの型システム

「** JavaScriptに型を追加する理由は？**」と思うかもしれません。

型は、コードの質と理解容易性を高める能力が実証されています。大規模なチーム（Google、Microsoft、Facebook）は、常に、この結論に至っています。具体的には：

* 型は、リファクタリングを行う際の開発速度を高めます。 *コンパイラがエラーをキャッチする方が、実行時(ランタイムで)にエラーが発生するよりも良いです*。
* 型は、最高の形式のドキュメントです。 *関数のシグネチャは定理であり、関数のボディは証明です*。

しかし、型には不必要に儀式的な面があります。TypeScriptは、障壁を可能な限り低く保つことに非常に特有です。方法は次のとおりです。

### あなたのJavaScriptはTypeScriptです
TypeScriptは、JavaScriptコードのコンパイル時の型安全性を提供します。その名前への驚きはありません。素晴らしいことは、型が完全にオプションであることです。あなたのJavaScriptコード `.js`ファイルは`.ts`ファイルに名前を変更することができ、それでもTypeScriptは元のJavaScriptファイルと同じ有効な `.js`を戻します。TypeScriptは*意図的に、そして、厳密に*、オプションの型チェックを持った、JavaScriptのスーパーセットです。

### 暗黙的な型推論が行われます
TypeScriptは、コード開発中の生産コストを最小限に抑えて型の安全性を確保するためにできるだけ多くの型情報を推測しようとします。たとえば、次の例では、TypeScriptはfooの型が数値の型であることを認識し、次のように2行目にエラーを返します。

```ts
var foo = 123;
foo = '456'; // Error: cannot assign `string` to `number`

// Is foo a number or a string?
```
この型推論が必要な動機があります。この例のようにしてコードの残りの部分で `foo`が`number`または `string`であることを確信することはできません。このような問題は、大規模な多くのファイルがあるコードベースで頻繁に発生します。後で型推論のルールを深く解説します。

### 型は明示的にすることができます
これまで述べたように、TypeScriptは安全な限り、できるだけ多く型を推論しますが、型を記述することによって、下記を行うことができます
1. コンパイラを助ける。さらに重要なことに、あなたのコードを読まなければならない次の開発者のための文書にする（将来のあなたかもしれない！）
1. コンパイラの理解を、あなたがそうであるべきと考える理解であるように強制できる。つまり、あなたのコードの理解が、コードのアルゴリズム分析（コンパイラによって行われる）と一致する

TypeScriptは、他の強制ではない型付き言語（ActionScriptやF#など）で一般的なPostfixタイプの型構文を使用します。

```ts
var foo: number = 123;
```
したがって、何か間違っていると、コンパイラはエラーになります。例：

```ts
var foo: number = '123'; // Error: cannot assign a `string` to a `number`
```

TypeScriptでサポートされているすべての型構文の詳細については、後の章で説明します。

### 型は構造です
いくつかの言語（特に名目上は型付け言語であるもの）では、静的な型指定は、コードがうまく動作することを知っているにもかかわらず、不必要に儀式的なコードになってしまいます。なぜなら、あなたがコードがうまく動作することを知っていたとしても、言語のセマンティクスがそこら中に同じコードをコピー・ペーストすることを強いるからです。これがC#用の[automapper for C#]（http://automapper.org/） のようなものが重要な理由です。 TypeScriptでは、JavaScript開発者にとって、認知的な負荷を最小限に抑え、簡単に使えるようにしたいので、タイプは構造的(structual)です。これが意味することは、* duck typing *が、ファーストクラスの言語構造であることです。次の例を考えてみましょう。関数 `iTakePoint2D`は、期待する全てのもの（例では、`x`と `y`）を含むものは、何でも受け入れます：

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

### 型エラーはJavaScriptの出力を妨げない
JavaScriptコードをTypeScriptに移行することを簡単にするため、コンパイルエラーがあったとしても、デフォルトでTypeScriptは有効なJavaScriptを出力します。例えば

```ts
var foo = 123;
foo = '456'; // Error: cannot assign a `string` to a `number`
```

次のjsを発行します：

```ts
var foo = 123;
foo = '456';
```

そのため、JavaScriptコードを段階的にTypeScriptにアップグレードすることができます。これは他の多くの言語コンパイラが動作するのとは非常に異なっており、そして、TypeScriptに移行する、その他１つの理由です。

### 型は周囲環境である可能性があります
TypeScriptの主要な設計目標は、TypeScriptで既存のJavaScriptライブラリを安全かつ簡単に使用できるようにすることでした。 TypeScriptはこれを宣言(declaration)で行います。 TypeScriptは、宣言にどれくらいの労力をかけるかの自由を提供します。より多くの労力をかければ、より多くの型安全性とコード補完が得られます。よく使われるJavaScriptライブラリの型定義は、[DefinitelyTyped community]（https://github.com/borisyankov/DefinitelyTyped） によって既に書かれているので、

1. 定義ファイルが既に存在します。
1. あるいは、少なくとも、よくレビューされた種類豊富なTypeScript宣言テンプレートの広大なリストが既に利用可能です

独自の型宣言ファイルを作成する方法の簡単な例として、[jquery]（https://jquery.com/） の簡単な例を考えてみましょう。デフォルトでは（良いJSコードのように）、TypeScriptは変数を使う前に宣言する（つまり、どこかで `var`を使う）ことを期待しています
```ts
$('.awesome').show(); // Error: cannot find name `$`
```
簡単な修正として、`$`が実際にあることをTypeScriptに伝えることができます：
```ts
declare var $: any;
$('.awesome').show(); // Okay!
```

必要に応じて、この基本的な定義に基づいて構築し、エラーからあなたを守るための詳細情報を提供することができます。
```ts
declare var $: {
    (selector:string): any;
};
$('.awesome').show(); // Okay!
$(123).show(); // Error: selector needs to be a string
```

後ほど、TypeScriptの詳細を知った後で、既存のJavaScript用のTypeScript定義を作成する方法について詳しく説明します（例えば、 `interface`や`any`など）。

## 将来のJavaScript => 今すぐ
TypeScriptは、現在のJavaScriptエンジン（ES5のみをサポートする）のためにES6で計画されている多くの機能を提供します。 typescriptチームは積極的にこれらの機能を追加しています。このリストは時間の経過とともに大きくなる予定です。これについては独自のセクションで説明します。しかし、ここにあるコードサンプルは、例としてのクラス:

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

と美しい太矢印の機能：

```ts
var inc = x => x+1;
```

### 要約
このセクションでは、TypeScriptの動機づけと設計のゴールを提供しました。これで、TypeScriptのきめ細かな詳細を掘り下げることができます。

[](Interfaces are open ended)
[](Type Inferernce rules)
[](Cover all the annotations)
[](Cover all ambients : also that there are no runtime enforcement)
[](.ts vs. .d.ts)
