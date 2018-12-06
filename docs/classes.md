### クラス(Classes)
JavaScriptでクラスをファーストクラスの道具として持つことが重要な理由は、次のとおりです。
1. [クラスは有用な構造抽象化を提供する](./tips/classesAreUseful.md)
1. それぞれのフレームワーク(emberjs、reactjsなど)が独自にクラスを実装するのではなく、クラスを使用する一貫した方法を提供します
1. オブジェクト指向の開発者はすでにクラスを理解しています

最後に、JavaScript開発者は `class` *を持つことができます。ここではPointという基本クラスがあります：
```ts
class Point {
    x: number;
    y: number;
    constructor(x: number, y: number) {
        this.x = x;
        this.y = y;
    }
    add(point: Point) {
        return new Point(this.x + point.x, this.y + point.y);
    }
}

var p1 = new Point(0, 10);
var p2 = new Point(10, 20);
var p3 = p1.add(p2); // {x:10,y:30}
```
このクラスは、ES5で次のJavaScriptを生成します。
```ts
var Point = (function () {
    function Point(x, y) {
        this.x = x;
        this.y = y;
    }
    Point.prototype.add = function (point) {
        return new Point(this.x + point.x, this.y + point.y);
    };
    return Point;
})();
```
これは、ファーストクラスの言語構造として、かなり慣用的な従来のJavaScriptクラスパターンです。

### 継承(Inheritance)
TypeScriptのクラス(他の言語のように)は、以下に示すように `extends`キーワードを使って*単一*継承をサポートします：

```ts
class Point3D extends Point {
    z: number;
    constructor(x: number, y: number, z: number) {
        super(x, y);
        this.z = z;
    }
    add(point: Point3D) {
        var point2D = super.add(point);
        return new Point3D(point2D.x, point2D.y, this.z + point.z);
    }
}
```
クラスにコンストラクタがある場合、コンストラクタから親コンストラクタを呼び出す必要があります(TypeScriptはこれをあなたに指摘します)。これにより、`this`で設定する必要があるものが確実に設定されます。`super`を呼び出すした後に、コンストラクタでやりたいことを追加できます(ここでは別のメンバ`z`を追加します)。

親メンバーの関数を簡単にオーバーライドする(ここでは `add`をオーバーライドします)、メンバでsuperクラスの機能を使用することに注意してください。

### 静的プロパティ(Statics)
TypeScriptクラスは、クラスのすべてのインスタンスで共有される`static`プロパティをサポートします。それらを置く(そしてアクセスする)自然な場所はクラスそのものであり、これがTypeScriptの動作です。

```ts
class Something {
    static instances = 0;
    constructor() {
        Something.instances++;
    }
}

var s1 = new Something();
var s2 = new Something();
console.log(Something.instances); // 2
```

静的メンバーだけでなく静的関数も使用できます。

### アクセス修飾子(Access Modifiers)
TypeScriptは `public`、`private`、`protected`のアクセス修飾子をサポートしています。これらは`class`メンバのアクセシビリティを次のように決定します：

|アクセス可能な場所(accessible on) | `public` | `protected` | `private`|
| ----------------- | ---------- | ------------- | ------ ----- |
|クラス(class)              |yes|yes|yes|
|子クラス(class children)    |yes|yes|no|
|クラスのインスタンス(class instances)|yes|no|no|

アクセス修飾子が指定されていない場合は、暗黙的に`public`となり、JavaScriptの*便利な*性質に一致します。

実行時(生成されたJS内)には意味がありませんが、間違って使用するとコンパイル時エラーが発生します。それぞれの例を以下に示します。

```ts
class FooBase {
    public x: number;
    private y: number;
    protected z: number;
}

// EFFECT ON INSTANCES
var foo = new FooBase();
foo.x; // okay
foo.y; // ERROR : private
foo.z; // ERROR : protected

// EFFECT ON CHILD CLASSES
class FooChild extends FooBase {
    constructor() {
      super();
        this.x; // okay
        this.y; // ERROR: private
        this.z; // okay
    }
}
```

いつものように、これらの修飾子はメンバプロパティとメンバ関数の両方で機能します。

### Abstract修飾子
`abstract`はアクセス修飾子と考えることができます。前述の修飾子とは対照的に、クラスのメンバーだけでなく`class`にも適用できるので、別に提示します。 `abstract`修飾子を持つことは、主に、その機能を直接呼び出すことができず、子クラスがその機能を提供しなければならないことを意味します。

* 抽象クラスを直接インスタンス化することはできません。その代わりに、ユーザは、`抽象クラス`から継承するいくつかの`class`を作成しなければなりません。
* 抽象メンバーに直接アクセスすることはできず、子クラスが機能を提供する必要があります。

### コンストラクタはオプションです

クラスはコンストラクタを持つ必要はありません。例えば以下は完全に動作します。

```ts
class Foo {}
var foo = new Foo();
```

### コンストラクタを使用して定義する

クラスのメンバーを下記のように初期化しています：

```ts
class Foo {
    x: number;
    constructor(x:number) {
        this.x = x;
    }
}
```
TypeScriptが提供する省略形を使うことができる一般的なパターンです。省略形では、アクセス修飾子を持ったメンバを自動的にクラスに定義し、コンストラクターからコピーされます。したがって、前の例は次のように書き直すことができます(`public x：number`に注意してください)：

```ts
class Foo {
    constructor(public x:number) {
    }
}
```

### プロパティ初期化子(Property Initializer)
これは、実際にES7からTypeScriptでサポートされている素晴らしい機能です。クラスコンストラクタの外でクラスの任意のメンバを初期化することができ、デフォルトを提供するのに便利です( `members = []`に注意してください)。

```ts
class Foo {
    members = [];  // Initialize directly
    add(x) {
        this.members.push(x);
    }
}
```
