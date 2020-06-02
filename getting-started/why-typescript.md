# TypeScriptを使う理由

TypeScriptの主なゴールは2つです。

* JavaScriptに_任意の型システム_を追加すること\（型を使うかどうかは自由\）
* 次世代のJavaScriptで計画されている機能を、現在の\（モダンではない\）JavaScript実行環境でも使えるようにすること

これらのゴールに対する動機は以下の通りです。

## TypeScriptの型システム

「**なぜJavaScriptに型を追加する必要があるのか？**」と疑問に思うかもしれません。

型は、コードの品質と理解しやすさを高めることが実証されています。大規模なチーム\(Google、Microsoft、Facebook\)は、常に、この結論に至っています。具体的には：

* 型は、リファクタリングを行う際の開発速度を高めます。_コードを書いている時にエラーを検出する方が、ランタイムで実行時してエラーが発生して初めて気づくよりも優れています_
* 型は、完璧なドキュメントです。_関数のシグネチャは定理であり、関数の本体は証明です_

しかし、型には過剰に儀式的な面があります。TypeScriptは、次に述べるように、型を導入する障壁を可能な限り低くしています。

### あなたの書いたJavaScriptはTypeScriptです

TypeScriptは、JavaScriptコードのコンパイル時の型安全性を提供します。その名前はこれを表しています。素晴らしい点は、型の使用が完全に任意\（オプション\）であることです。あなたのJavaScriptコード`.js`ファイルを`.ts`ファイルに名前を変更したとしても、TypeScriptは元のJavaScriptファイルと同じ有効な`.js`を返します。TypeScriptは意図的かつ厳密なJavaScriptのスーパーセットであり、任意の型チェック機構を持ったプログラミング言語です。

### 暗黙的な型推論\(type inference\)

TypeScriptは、生産性へのコストを最小限に抑えて型の安全性を提供するために、可能な限り、型推論を行います。たとえば、次の例では、TypeScriptはfooの型が`number`であると推測し、2行目のコードにエラーを表示します。

```typescript
var foo = 123;
foo = '456'; // Error: cannot assign `string` to `number`

// Is foo a number or a string?
```

型推論を必要とすることには大きな理由があります。この例のようなコードを書いた場合、残りのコードにおいて`foo`が`number`であるか`string`であるかを確定できません。このような問題は、大規模なコードベースで頻繁に発生します。後で型推論のルールの詳細を説明します。

### 明示的な型\(type annotation\)

これまで述べたように、TypeScriptは、安全に行える場合は可能な限り、型推論を行います。しかし、明示的に型を指定するアノテーションを記述することによって、以下のメリットが得られます:

1. コンパイラを助けるだけでなく、より、重要なことに、あなたの書いたコードを次に読まなくてはならない開発者にとってのドキュメントになります。\(将来のあなたかもしれない!\)
2. コンパイラがどのように理解するかを強制します。つまり、コードに対するあなたの理解が、コンパイラのアルゴリズムによる分析に必ず反映されます。

TypeScriptは、他の任意な型付き言語\(ActionScriptやF\#など\)で一般的な、末尾型アノテーション\(Postfix type annotation\)を使用します。

```typescript
var foo: number = 123;
```

何かが間違っていたら、コンパイラはエラーを出します：

```typescript
var foo: number = '123'; // Error: cannot assign a `string` to a `number`
```

TypeScriptでサポートされている型アノテーションの詳細については、今後の章で説明します。

### 型は構造的

いくつかの言語\(特に型付き言語と呼ばれるもの\)において、静的な型付けは、過剰に儀式的なコードになってしまいます。なぜなら、コードが正しく動作することが確実である場合でも、構文ルールが同じコードをコピー＆ペーストすることを強制するからです。C\#の[automapper for C\#](http://automapper.org/)のようなものが必須である理由です。JavaScript開発者にとっての認知的な負荷を最小限に抑えるため、TypeScriptにおける型は構造的\(structural\)になっています。これが意味することは、ダックタイピング\(duck typing\)が、ファーストクラスの言語構造であるということです。次の例を考えてみましょう。関数`iTakePoint2D`は、期待するすべてのメンバ\(例では、`x`と `y`\)を含む構造であれば、何でも受け入れます：

```typescript
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

```typescript
var foo = 123;
foo = '456'; // Error: cannot assign a `string` to a `number`
```

次のjsを出力します：

```typescript
var foo = 123;
foo = '456';
```

これにより、JavaScriptコードを段階的にTypeScriptに移行することができます。これは他の言語のコンパイラの動作とは全く異なっており、そして、TypeScriptに移行する理由の1つです。

### 型による開発環境へのメリット

TypeScriptの設計における大きなゴールは、TypeScriptで既存のJavaScriptライブラリを安全かつ簡単に利用できることです。TypeScriptはこれを型宣言で行います。TypeScriptにおいて、型宣言にどれくらいの労力をかけるかは自由です。より多くの労力をかければ、より多くの型安全性とIDEによるコード補完が得られます。有名で人気のあるJavaScriptライブラリの型定義は、[DefinitelyTyped コミュニティ](https://github.com/borisyankov/DefinitelyTyped)によって既に作成されています。そのため、

1. 定義ファイルが既に存在します。
2. あるいは、最低でも、きちんとレビューされた多くのTypeScript宣言のテンプレートが既に利用可能です。

独自の型宣言ファイルを作成する簡単な例として、[jquery](https://jquery.com/)の簡単な例を考えてみましょう。TypeScriptは、デフォルトの設定では、\(望ましいJavaScriptコードのように\)、変数を使う前に宣言する\(つまり、どこかで`var`を使う\)ことを期待しています。

```typescript
$('.awesome').show(); // Error: cannot find name `$`
```

簡単な修正方法は、`declare`を使って、変数`$`が実際に存在することをTypeScriptに伝えることです。

```typescript
declare var $: any;
$('.awesome').show(); // Okay!
```

必要に応じて、より詳細に型を定義し、プログラミングエラーを防止することができます。

```typescript
declare var $: {
    (selector:string): any;
};
$('.awesome').show(); // Okay!
$(123).show(); // Error: selector needs to be a string
```

TypeScriptの基本を理解した後で、既存のJavaScriptコードのTypeScriptにおける型定義について、詳しく説明します\(`interface`や`any`など\)。

## 次世代のJavaScriptの機能を今すぐに利用できる

TypeScriptは、古いJavaScriptエンジン\(ES5のみをサポートする\)でも、ES6以降で計画されている多くの機能を使えるようにしています。TypeScriptチームは積極的に機能を追加しています。機能は今後もどんどん増えていく予定です。これらについては独自の章で説明します。サンプルとしてクラス\(ES6で追加された機能\)の例を提示しておきます:

```typescript
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

それと、かわいい太っちょのアロー関数も。:

```typescript
var inc = x => x+1;
```

### 要約

この章では、TypeScriptを使う理由と、TypeScriptが目指しているゴールを説明しました。これで、TypeScriptの隅々まで詳細を追うことができます。

