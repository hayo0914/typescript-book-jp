### アロー関数(Arrow Functions)

アロー関数は*fat arrow*(なぜなら`->`は薄い矢印で `=>`は太い矢印であるため)、またはlambda関数(他の言語にならって)と呼ばれています。もう1つの一般的に使用される機能は、アロー関数`()=> something`です。これを使う理由：

1. `function`を何度もタイプしなくて済む
1. `this`をレキシカルに捕捉する
1. `arguments`をレキシカルに捕捉する

関数的であると公言する言語、JavaScriptでは`function`を頻繁にタイプしやすい傾向があります。アロー関数を使うと、関数をシンプルに作成できます
```ts
var inc = (x)=>x+1;
```
`this`はJavaScriptにおいて昔から頭痛の種でした。
ある賢い人はかつて「私は`this`の意味をすぐに忘れるJavaScriptが嫌いだ」と言いました。アロー関数は、それを囲んだコンテキストから`this`を捕捉します。この純粋なJavaScriptだけで書かれたクラスを考えてみましょう：

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
このコードをブラウザで実行すると、関数内の`this`は`window`を指します。なぜなら、`window`が`growOld`関数を実行するものだからです。修正方法は、アロー関数を使うことです：
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
これがうまくいく理由は、アロー関数が、関数ボディの外側の`this`を捕捉するからです。次のJavaScriptコードは同等の動きをします(TypeScriptを使用しない場合の書き方です)。
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
TypeScriptを使っているので、ずっと気持ち良い構文で書けます。アロー関数とクラスを組み合わせることができます:
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
簡潔な構文が得られること以外に、もし関数を他の誰かに呼び出してほしい場合は、アロー関数を使うだけでできます。つまり:
```ts
var growOld = person.growOld;
// Then later someone else calls it:
growOld();
```
自分で呼び出す場合:
```ts
person.growOld();
```
いずれにしても`this`は正しい呼び出しコンテキストになります(この例では`person`)。

#### Tip：アロー関数の危険性

実際に`this`を呼び出しコンテキスト(calling context)にしたい場合はアロー関数を使うべきではありません。jquery、underscore、mochaなどのライブラリで使用されるコールバックのケースです。ドキュメントが`this`の関数を記述している場合は、たぶんアロー関数の代わりに`function`を使うべきでしょう。同様に、`arguments`を使う場合は、アロー関数を使用しないでください。

#### Tip：`this`を使用するライブラリのアロー関数
多くのライブラリ、例えば`jQuery`の反復(例: https://api.jquery.com/jquery.each/)は`this`を使って現在反復中のオブジェクトを渡します。このようなケースでは、ライブラリが渡した`this`だけでなく周囲のコンテキストにもアクセスしたい場合は、アロー関数が無いときに行うように`_self`のような一時変数を使用してください。

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
JavaScriptランタイム(JavaScriptの仕様に原因がある)によって*JavaScript Label*を含むブロックとして解釈されます。

> この意味がわからなくても心配しないでください。いずれにしろ、"unused label"(未使用のラベル)というTypeScriptのナイスなコンパイラエラーが発生します。Labelは古い(そしてほとんどは使用されていない)JavaScript機能で、現代のGOTO(経験豊富な開発者が悪いと考える🌹)として無視して構いません。

`()`でオブジェクトのリテラルを囲むことで修正できます：

```ts
// Correct 🌹
var foo = () => ({
    bar: 123
});
```
