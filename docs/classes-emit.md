#### IIFE(Immediately-Invoked Function Expression)には何がありますか？
クラスのために生成されたjsは、このようになっている可能性もありました。
```ts
function Point(x, y) {
    this.x = x;
    this.y = y;
}
Point.prototype.add = function (point) {
    return new Point(this.x + point.x, this.y + point.y);
};
```

Immediately-Invoked Function Expression(IIFE)に包む理由です。例:

```ts
(function () {

    // BODY

    return Point;
})();
```

継承に関係しています。これは、IIFEは、TypeScriptがベースクラスを変数 `_super`として取り込むことを可能にします。例:

```ts
var Point3D = (function (_super) {
    __extends(Point3D, _super);
    function Point3D(x, y, z) {
        _super.call(this, x, y);
        this.z = z;
    }
    Point3D.prototype.add = function (point) {
        var point2D = _super.prototype.add.call(this, point);
        return new Point3D(point2D.x, point2D.y, this.z + point.z);
    };
    return Point3D;
})(Point);
```

IIFEは、TypeScriptが基本クラス `Point`を`_super`変数に簡単に取り込むことを可能にし、クラス本体で一貫して使用されることに注意してください。

### `__extends`
クラスを継承するとすぐに、TypeScriptは次の関数も生成します：
```ts
var __extends = this.__extends || function (d, b) {
    for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p];
    function __() { this.constructor = d; }
    __.prototype = b.prototype;
    d.prototype = new __();
};
```
ここで `d`は派生クラスを指し、`b`は基底クラスを指す。この関数は2つのことを行います：
1. `(b.hasOwnProperty(p))d [p] = b [p];`であれば、基本クラスの静的メンバーを子クラスにコピーする。
1. 子クラス関数のプロトタイプをセットアップし、親の`proto`のメンバーを検索できるようにする。例:`d.prototype.__ proto__ = b.prototype`

人々は 1 を理解するのに苦労することはほとんどありませんが、多くの人が 2 と格闘します。なので順番に説明します。

#### `d.prototype .__ proto__ = b.prototype`

これについて多くの人を教えた後、私は以下の説明が最も簡単であることを見出します。まず、 `__extends`のコードが単純な`d.prototype .__ proto__ = b.prototype`とどのように等価であるのか、そしてなぜこの行自体が重要であるのかを説明します。これらすべてを理解するには、これらのことを知る必要があります。

1. `__proto__`
1. `prototype`
1. 呼び出された関数内の`this`に対する`new`の効果
1. `prototype`と`__proto__`に対する`new`の効果

JavaScriptのすべてのオブジェクトには `__proto__`メンバが含まれています。このメンバは古いブラウザではアクセスできないことがよくあります(ドキュメントでは、この魔法のプロパティを `[[prototype]]`と呼ぶこともあります)。 1つの目的があります：ルックアップ中にオブジェクトにプロパティが見つからない場合(例えば `obj.property`)、`obj .__ proto __。property`でルックアップされます。それでもまだ見つからなければ、 `obj .__ proto __.__ proto __。property`を見つけられます： それが見つかるか、最後の`.__ proto__`自体が`null`となるまでです。これはJavaScriptがなぜプロトタイプの継承をサポートすると言われているのかを説明しています。これは次の例に示されています。これはchromeコンソールまたはNode.jsで実行できます。

```ts
var foo = {}

// setup on foo as well as foo.__proto__
foo.bar = 123;
foo.__proto__.bar = 456;

console.log(foo.bar); // 123
delete foo.bar; // remove from object
console.log(foo.bar); // 456
delete foo.__proto__.bar; // remove from foo.__proto__
console.log(foo.bar); // undefined
```

これで、あなたは `__proto__`を理解できました。もう一つの有用な事実は、JavaScriptの`function`には`prototype`というプロパティがあり、そして、`prototype`は、その関数を指す`constructor`というメンバーを持っているということです。これを以下に示します。

```ts
function Foo() { }
console.log(Foo.prototype); // {} i.e. it exists and is not undefined
console.log(Foo.prototype.constructor === Foo); // Has a member called `constructor` pointing back to the function
```

次に、呼び出された関数内の`this`に`new`が及ぼす影響を見てみましょう。基本的には、呼び出された関数内の `this`は、関数から返される新しく生成されたオブジェクトを指します。関数内で `this`のプロパティを変更するのは簡単です：

```ts
function Foo() {
    this.bar = 123;
}

// call with the new operator
var newFoo = new Foo();
console.log(newFoo.bar); // 123
```

関数で `new`を呼び出すと、関数呼び出しから返された新しく作成されたオブジェクトの`__proto__`に関数の `prototype`が代入されるということだけです。完全に理解するために実行できるコードは次のとおりです。

```ts
function Foo() { }

var foo = new Foo();

console.log(foo.__proto__ === Foo.prototype); // True!
```

それでおしまい。今度は、 `__extends`の中を次のようにストレートに見てください。私はこれらの行に番号を付けることにした：

```ts
1  function __() { this.constructor = d; }
2   __.prototype = b.prototype;
3   d.prototype = new __();
```

この関数を3行目の `d.prototype = new __()`と逆に読むと `d.prototype = {__proto__：__.prototype}`を意味します(`prototype`と`__proto__`に対する`new`の効果によるものです)、それを前の行(つまり、行2 `__.prototype = b.prototype;`)と組み合わせると、`d.prototype = {__proto__：b.prototype}`となります。

しかし、待ってください。私達は、単に`d.prototype.__proto__`が変更され、古い`d.prototype.constructor`が維持されることを望んでいました。そこで、最初の行(`function __(){this.constructor = d;}`)の意味が重要です。これは`d.prototype = {__proto__：__.prototype, constructor：d}`の効果があります(これは呼び出された関数の中で`this`に `new`が及ぼす影響のためです)。したがって、`d.prototype.constructor`を復元するので、私たちが本当に変更したのは`__proto__`だけなので、 `d.prototype .__ proto__ = b.prototype`です。

#### `d.prototype .__ proto__ = b.prototype`の意義

重要な点は、子クラスにメンバー関数を追加し、基本クラスから他のメンバー関数を継承できることです。これは次の簡単な例で示されます。

```ts
function Animal() { }
Animal.prototype.walk = function () { console.log('walk') };

function Bird() { }
Bird.prototype.__proto__ = Animal.prototype;
Bird.prototype.fly = function () { console.log('fly') };

var bird = new Bird();
bird.walk();
bird.fly();
```
基本的に `bird.fly`は`bird.__ proto __.fly`(`new`は`bird.__ proto__`が `Bird.prototype`を指すようにすることを思い出してください)から検索され、`bird.walk`(継承されたメンバー) は`bird.__proto__.__proto__.walk`から検索されます(`bird .__ proto__ == Bird.prototype`と`bird.__ proto __.__ proto__` == `Animal.prototype`)。
