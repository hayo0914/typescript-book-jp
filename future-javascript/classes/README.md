# クラス

## クラス\(Classes\)

JavaScriptにおいて、クラスを第一級\(first class\)のものとして持つことが重要である理由は次の通りです:

1. [クラスが提供する便利な構造の抽象化](../../main-1/classesareuseful.md)
2. それぞれのフレームワーク\(emberjs、reactjsなど\)がそれぞれ独自のクラス構文を提供するのではなく、一貫したクラス構文を提供する
3. オブジェクト指向の開発者にとっての親和性

TypeScriptでは、ブラウザの互換性を気にすることなく`class`を使うことができます。ここに、Pointという簡単なクラスの例を示します：

```typescript
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

このクラスをコンパイルすると、古いブラウザ\(ES5\)で動作する次のJavaScriptを生成します。

```typescript
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

これは慣用的に使われてきた従来のJavaScriptのクラスのパターンです。今は第一級\(first class\)の言語の構成要素としてのクラスが利用できます。

## 継承\(Inheritance\)

TypeScriptにおけるクラスは\(他の言語のように\)`extends`キーワードを使った_単一_継承をサポートします:

```typescript
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

クラスにコンストラクタがある場合、コンストラクタから親コンストラクタを呼び出さなければなりません\(TypeScriptはこれをしていない場合はエラーを表示します\)。これにより、`this`のプロパティが正しく設定されます。`super`を呼び出した後、コンストラクタで必要な処理を追加することができます\(例えば、他のプロパティ`z`を追加します\)。

親のメンバ関数をオーバーライドする\(ここでは`add`をオーバーライドします\)場合でも、親クラスの機能を呼び出せることに注意してください\(`super.`構文を使います\)。

## 静的メンバ\(Statics\)

TypeScriptクラスは、クラスの全インスタンスで共有される`static`なプロパティをサポートします。静的メンバを置き、アクセスする自然な場所はクラスそのものです。TypeScriptでは、`static`がサポートされています。

```typescript
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

静的メンバと同様に静的関数も使用できます。

## アクセス修飾子\(Access Modifiers\)

TypeScriptはアクセス修飾子として`public`、`private`、`protected`をサポートしています。これらは`class`メンバのアクセシビリティを次のように決定します：

| アクセス可能な場所\(accessible on\) | `public` | `protected` | `private` |
| :--- | :--- | :--- | :--- |
| クラス\(class\) | yes | yes | yes |
| 子クラス\(class children\) | yes | yes | no |
| クラスのインスタンス\(class instances\) | yes | no | no |

アクセス修飾子が指定されていない場合は、JavaScriptの便利な性質と同じように、暗黙的に`public`となります🌹。

アクセス修飾子は、ランタイム上\(生成されたJSの実行時\)では何の影響もありませんが、間違った使い方をするとコンパイルエラーが出力されることに注意してください。それぞれの例を以下に示します:

```typescript
class FooBase {
    public x: number;
    private y: number;
    protected z: number;
}

// インスタンスにおける効果
var foo = new FooBase();
foo.x; // okay
foo.y; // ERROR : private
foo.z; // ERROR : protected

// サブクラスにおける効果
class FooChild extends FooBase {
    constructor() {
      super();
        this.x; // okay
        this.y; // ERROR: private
        this.z; // okay
    }
}
```

いつもと同じように、これらの修飾子はメンバ変数とメンバ関数の両方で利用可能です。

## Abstract修飾子

`abstract`はアクセス修飾子の1つと考えることができます。上で述べた修飾子とは異なり、クラスのメンバと同様に`class`に対しても利用できるため、アクセス修飾子とは分けて説明します。`abstract`修飾子が主に意味することは、その機能を親クラスに対して直接的に呼び出すことができず、子クラスがその具体的な機能を提供しなければならないということです。

* 抽象クラスを直接インスタンス化することはできません。その代わりに、`abstract class`を継承した`class`を作成しなければなりません

```typescript
abstract class FooCommand {}

class BarCommand extends FooCommand {}

const fooCommand: FooCommand = new FooCommand(); // Cannot create an instance of an abstract class.

const barCommand = new BarCommand(); // You can create an instance of a class that inherits from an abstract class.
```

* 抽象メンバは直接アクセスできません。子クラスがその具体的な機能（実装）を提供しなくてはなりません

```typescript
abstract class FooCommand {
  abstract execute(): string;
}

class BarErrorCommand extends FooCommand {} // 'BarErrorCommand' needs implement abstract member 'execute'.

class BarCommand extends FooCommand {
  execute() {
    return `Command Bar executed`;
  }
}

const barCommand = new BarCommand();

barCommand.execute(); // Command Bar executed
```

## コンストラクタは必須ではありません

クラスは必ずコンストラクタを持っている必要はありません。例えば、以下は正しく動作します。

```typescript
class Foo {}
var foo = new Foo();
```

## コンストラクタを定義する

以下のように、クラスのメンバを定義し、初期化することができます:

```typescript
class Foo {
    x: number;
    constructor(x:number) {
        this.x = x;
    }
}
```

これはTypeScriptの省略形を使うことができるパターンです。コンストラクタ引数にアクセス修飾子を付けることができ、それが自動的にクラス内に宣言され、コンストラクタの引数によって値が初期化されます。なので、前の例は次のように書き直すことが可能です\(`public x:number`に注目してください\)：

```typescript
class Foo {
    constructor(public x:number) {
    }
}
```

## プロパティ初期化子\(Property initializer\)

これはTypeScript\(及びES7以降\)でサポートされている気の利いた機能です。クラスのコンストラクタの外側でクラスのメンバ変数を初期化できます。デフォルト値を指定するのに便利です\(`members = []`に注目してください\)。

```typescript
class Foo {
    members = [];  // Initialize directly
    add(x) {
        this.members.push(x);
    }
}
```

