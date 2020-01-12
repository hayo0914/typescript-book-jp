### アロー関数(Arrow Functions)

アロー関数は、可愛いらしく*fat arrow*(なぜなら`->`は細く `=>`は太い)、または*lambda関数*(他の言語でそう名付けられているため)とも呼ばれます。一般的に利用される機能のひとつは、このアロー関数`()=> something`です。これを使う理由は次の通りです：

1. `function`を何度も打ち込まなくて済む
1. `this`の意味をレキシカルスコープで捕捉する
1. `arguments`の意味をレキシカルスコープで捕捉する

関数型であると公言する言語と比べると、JavaScriptでは`function`を頻繁に打ち込まなければならない傾向があります。アロー関数を使うと、関数をシンプルに作成できます
```ts
var inc = (x)=>x+1;
```
`this`はJavaScriptにおいて昔から頭痛の種でした。
ある賢い人はかつて「私は`this`の意味をすぐに忘れるJavaScriptが嫌いだ」と言いました。アロー関数は、それを囲んだコンテキストから`this`を捕捉します。純粋なJavaScriptだけで書かれたクラスを使って考えてみましょう：

```ts
function Person(age) {
    this.age = age;
    this.growOld = function() {
        this.age++;
    }
}
var person = new Person(1);
setTimeout(person.growOld,1000);

setTimeout(function() { console.log(person.age); },2000); // 1, should have been 2
```
このコードをブラウザで実行すると、関数内の`this`は`window`を指します。なぜなら、`window`が`growOld`関数を実行しているからです。修正方法は、アロー関数を使うことです：
```ts
function Person(age) {
    this.age = age;
    this.growOld = () => {
        this.age++;
    }
}
var person = new Person(1);
setTimeout(person.growOld,1000);

setTimeout(function() { console.log(person.age); },2000); // 2
```
これがうまくいく理由は、アロー関数が、関数本体の外側の`this`を捕捉するからです。次のJavaScriptコードは同等の動きをします(TypeScriptを使用しない場合の書き方です)。
```ts
function Person(age) {
    this.age = age;
    var _this = this;  // capture this
    this.growOld = function() {
        _this.age++;   // use the captured this
    }
}
var person = new Person(1);
setTimeout(person.growOld,1000);

setTimeout(function() { console.log(person.age); },2000); // 2
```
TypeScriptを使っているので、はるかに快適な構文で書けます。アロー関数とクラスは、組み合わせることができます:
```ts
class Person {
    constructor(public age:number) {}
    growOld = () => {
        this.age++;
    }
}
var person = new Person(1);
setTimeout(person.growOld,1000);

setTimeout(function() { console.log(person.age); },2000); // 2
```

> [このパターンについてのSweetなビデオ🌹](https://egghead.io/lessons/typescript-make-usages-of-this-safe-in-class-methods)

#### Tip：アロー関数の必要性
簡潔な構文が得られることに加えて、関数を他の何かに呼び出してもらいたい場合も、アロー関数を使うだけで良いのです。本質的には以下の通りです:
```ts
var growOld = person.growOld;
// Then later someone else calls it:
growOld();
```
自分で呼び出す場合は以下のようになります:
```ts
person.growOld();
```
どちらでも、`this`は正しいコンテキストになります(この例では`person`)。

#### Tip：アロー関数の危険性

実は、`this`を*呼び出しコンテキストにしたい*場合は*アロー関数を使うべきではありません*。jquery、underscore、mochaのようなライブラリで使用するコールバックのケースです。ドキュメントが`this`の機能について言及している場合は、おそらくアロー関数の代わりに`function`を使うべきでしょう。同様に、あなたが`arguments`を使うことを予定している場合は、アロー関数を使用しないでください。

#### Tip：`this`を使用するライブラリのアロー関数
thisを使う多くのライブラリ、例えば`jQuery`の反復(例: <https://api.jquery.com/jquery.each/>)は`this`を使って現在反復中のオブジェクトを渡します。このようなケースにおいて、ライブラリが渡した`this`だけでなく周囲のコンテキストにもアクセスしたい場合は、アロー関数が無いときに行うように`_self`のような一時変数を使用してください。

```ts
let _self = this;
something.each(function() {
    console.log(_self); // the lexically scoped value
    console.log(this); // the library passed value
});
```

#### Tip：アロー関数と継承
クラスのプロパティとしてのアロー関数は、継承において正常に動作します：

```ts
class Adder {
    constructor(public a: number) {}
    add = (b: number): number => {
        return this.a + b;
    }
}
class Child extends Adder {
    callAdd(b: number) {
        return this.add(b);
    }
}
// Demo to show it works
const child = new Child(123);
console.log(child.callAdd(123)); // 246
```

しかし、子クラスで関数をオーバーライドした場合、`super`キーワードは動作しません。プロパティは`this`に行きます。`this`は1つしかないので、このような関数は、親クラスの同じ関数を呼び出すことはできません(`super`はprototypeのメンバだけで動作します)。メソッドを子にオーバーライドする前に、メソッドのコピーを作成することで回避できます。

```ts
class Adder {
    constructor(public a: number) {}
    // This function is now safe to pass around
    add = (b: number): number => {
        return this.a + b;
    }
}

class ExtendedAdder extends Adder {
    // Create a copy of parent before creating our own
    private superAdd = this.add;
    // Now create our override
    add = (b: number): number => {
        return this.superAdd(b);
    }
}
```

### Tip：Quick Object Return

時には単純なオブジェクトリテラルを返す関数が必要な場合もあります。しかし、下記のような場合:

```ts
// WRONG WAY TO DO IT
var foo = () => {
    bar: 123
};
```
JavaScriptランタイム(JavaScriptの仕様に原因がある)によって*JavaScript Label*を含む*ブロック*として解釈されます。

> この意味がわからなくても心配しないでください。いずれにしろ、"unused label"(未使用のラベル)というTypeScriptのナイスなコンパイラエラーが発生します。Labelは古い(そしてほとんどは使用されていない)JavaScript機能で、現代のGOTO(経験豊富な開発者は悪いものとみなす🌹)として無視して構いません。

`()`でオブジェクトのリテラルを囲むことで修正できます：

```ts
// Correct 🌹
var foo = () => ({
    bar: 123
});
```
