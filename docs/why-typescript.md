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
これまで述べたように、TypeScriptはできるだけ多く推論しますが、型を記述して、以下を行うことができます。
1. コンパイラに沿って、さらに重要なことに、あなたのコードを読まなければならない次の開発者のための文書を書いてください。
1. コンパイラが見ていることを強制する、それはあなたが見なければならないと思ったものです。つまり、コードの理解は、コードのアルゴリズム分析（コンパイラによって行われる）と一致します。

TypeScriptは、他の任意の*注釈付き言語（ActionScriptやF#など）で一般的なポストフィックスタイプの注釈を使用します。

```ts
var foo: number = 123;
```
したがって、何か間違っていると、コンパイラはエラーになります。例：

```ts
var foo: number = '123'; // Error: cannot assign a `string` to a `number`
```

TypeScriptでサポートされているすべてのアノテーション構文の詳細については、後の章で説明します。

### タイプは構造的です
いくつかの言語（具体的には名目上の型付けされたもの）では、静的な型指定は、コードがうまく動作することを知っているにもかかわらず、言語セマンティクスがあなたに物事をコピーすることを強いるので、これがC#用の[automapper for C#]（http://automapper.org/）のようなものが*重要な*理由です。 TypeScriptでは、コグニティブなオーバーロードを最小限に抑えたJavaScript開発者にとって、簡単に使いたいので、タイプは*構造*です。つまり、* duck typing *はファーストクラスの言語構造です。次の例を考えてみましょう。関数 `iTakePoint2D`は、期待するすべてのもの（`x`と `y`）を含むものを受け入れます：

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

### 型エラーはJavaScriptの送出を妨げない
コンパイルエラーがあっても、JavaScriptコードをTypeScriptに簡単に移行できるようにするため、デフォルトでTypeScript *は有効なJavaScript *を出力します。例えば

```ts
var foo = 123;
foo = '456'; // Error: cannot assign a `string` to a `number`
```

次のjsを発行します：

```ts
var foo = 123;
foo = '456';
```

そのため、JavaScriptコードを段階的にTypeScriptにアップグレードすることができます。これは他の多くの言語コンパイラが動作するのとは非常に異なりますが、TypeScriptに移行するもう一つの理由です。

### 型は周囲環境である可能性があります
TypeScriptの主要な設計目標は、TypeScriptで既存のJavaScriptライブラリを安全かつ簡単に使用できるようにすることでした。 TypeScriptはこれを*宣言*で行います。 TypeScriptは、宣言にどれくらいの労力をかけるかをスライディングスケールで提供します。より多くの型安全性+コードインテリジェンスを取り入れる努力がますます重要になります。よく使われるJavaScriptライブラリの定義は、[DefinitelyTyped community]（https://github.com/borisyankov/DefinitelyTyped）によって既に書かれているので、

1. 定義ファイルが既に存在します。
1. あるいは、少なくとも既に見直されている種類豊富なTypeScript宣言テンプレートのリストがあります

独自の宣言ファイルを作成する方法の簡単な例として、[jquery]（https://jquery.com/）の簡単な例を考えてみましょう。デフォルトでは（良いJSコードのように）、TypeScriptは変数を使う前に宣言する（つまり、どこかで `var`を使う）ことを期待しています
```ts
$('.awesome').show(); // Error: cannot find name `$`
```
簡単な修正*として、実際に `$`と呼ばれるものがあることをTypeScript *に伝えることができます：
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

## 将来のJavaScript =>今すぐ
TypeScriptは、現在のJavaScriptエンジン（ES5のみをサポートする）のためにES6で計画されている多くの機能を提供します。 typescriptチームは積極的にこれらの機能を追加しています。このリストは時間の経過とともに大きくなる予定です。これについては独自のセクションで説明します。しかし、ここの標本はクラスの例です：

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

と美しい太い矢印の機能：

```ts
var inc = x => x+1;
```

### 要約
このセクションでは、TypeScriptの動機づけと設計目標を提供しました。これで、TypeScriptのきめ細かな詳細を掘り下げることができます。

[]（インタフェースはオープンエンド）
[]（タイプの見越しルール）
[]（すべての注釈をカバーする）
[]（すべてのアンビエントをカバーする：実行時強制がないことも）
[]（.s対.d.ts）
