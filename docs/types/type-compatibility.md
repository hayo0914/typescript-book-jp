* [型互換性](#型互換性)
* [健全性](健全性)
* [構造](#構造)
* [Generics](#ジェネリックス)
* [分散](#分散)
* [関数](#関数)
  * [戻り値の型](#return-type)
  * [引数の数](#引数の数)
  * [オプションパラメータと残りのパラメータ](#オプションと休止パラメータ)
  * [引数の種類](#種類の引数)
* [Enums](#enums)
* [クラス](#クラス)
* [Generics](#ジェネリックス)
* [脚注：不変量](#脚注 - 不変量)

## 型の互換性

タイプの互換性(ここで議論する)は、あるものを別のものに割り当てることができるかどうかを決定します。例えば。 `string`と`number`は互換性がありません：

```ts
let str: string = "Hello";
let num: number = 123;

str = num; // ERROR: `number` is not assignable to `string`
num = str; // ERROR: `string` is not assignable to `number`
```

## 健全性

TypeScriptの型システムは便利であるように設計されています。 `any`に何かを割り当てることができます。これは、コンパイラにあなたが望むことを何でもできるようにすることを意味します：

```ts
let foo: any = 123;
foo = "Hello";

// Later
foo.toPrecision(3); // Allowed as you typed it as `any`
```

## 構造

TypeScriptオブジェクトは構造的に型付けされています。つまり、* names *は構造が一致する限り重要ではありません

```ts
interface Point {
    x: number,
    y: number
}

class Point2D {
    constructor(public x:number, public y:number){}
}

let p: Point;
// OK, because of structural typing
p = new Point2D(1,2);
```

これにより、(バニラJSのように)オンザフライでオブジェクトを作成することができ、推論が可能な場合でも安全性が保たれます。

また、*もっと*データが細かいとみなされます：

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

## 分散

分散は、タイプの互換性分析のために理解しやすく、重要な概念です。

単純な型 `Base`と`Child`の場合、 `Child`が`Base`の子であれば、 `Child`のインスタンスは`Base`型の変数に代入することができます。

> 多型101です

このような `Base`型と`Child`型で構成される複合型の型互換性は、類似のシナリオにおける `Base`と`Child`が* variance *によって駆動されるところに依存します。

* 共変量：同じ方向にのみ(共に関節)
* コントラバナント：反対の方向にのみ(逆の反対)
* Bivariant：(共に両方とも)共同と反対の両方。
* 不変式：型がまったく同じでない場合、それらは互換性がありません。

> 注意：JavaScriptのような変更可能なデータの存在下で、完全に健全な型のシステムの場合、 `invariant`が唯一有効なオプションです。しかし、述べたように*利便性は私たちに不健全な選択を強いる。

## 関数

2つの機能を比較するときには、いくつか微妙なことを考慮する必要があります。

戻り値の型

`covariant`：戻り型は少な​​くとも十分なデータを含んでいなければなりません。

```ts
/** Type Hierarchy */
interface Point2D { x: number; y: number; }
interface Point3D { x: number; y: number; z: number; }

/** Two sample functions */
let iMakePoint2D = (): Point2D => ({ x: 0, y: 0 });
let iMakePoint3D = (): Point3D => ({ x: 0, y: 0, z: 0 });

/** Assignment */
iMakePoint2D = iMakePoint3D; // Okay
iMakePoint3D = iMakePoint2D; // ERROR: Point2D is not assignable to Point3D
```

### 引数の数

引数が少なくて済みます(つまり、関数は追加のパラメータを無視することができます)。結局のところ、あなたは少なくとも十分な引数で呼び出されることが保証されています。

```ts
let iTakeSomethingAndPassItAnErr
    = (x: (err: Error, data: any) => void) => { /* do something */ };

iTakeSomethingAndPassItAnErr(() => null) // Okay
iTakeSomethingAndPassItAnErr((err) => null) // Okay
iTakeSomethingAndPassItAnErr((err, data) => null) // Okay

// ERROR: Argument of type '(err: any, data: any, more: any) => null' is not assignable to parameter of type '(err: Error, data: any) => void'.
iTakeSomethingAndPassItAnErr((err, data, more) => null);
```

### オプションおよび残りのパラメータ

オプションの(事前に決定されたカウント)およびレストパラメーター(任意のカウント数)は、便宜上、再び互換性があります。

```ts
let foo = (x:number, y: number) => { /* do something */ }
let bar = (x?:number, y?: number) => { /* do something */ }
let bas = (...args: number[]) => { /* do something */ }

foo = bar = bas;
bas = bar = foo;
```

> 注意：strictNullChecksがfalseの場合、オプションの(ここでは `bar`)とオプションではない(この例では`foo`)のみ互換性があります。

### 引数のタイプ

`bivariant`：これは共通イベント処理シナリオをサポートするように設計されています

```ts
/** Event Hierarchy */
interface Event { timestamp: number; }
interface MouseEvent extends Event { x: number; y: number }
interface KeyEvent extends Event { keyCode: number }

/** Sample event listener */
enum EventType { Mouse, Keyboard }
function addEventListener(eventType: EventType, handler: (n: Event) => void) {
    /* ... */
}

// Unsound, but useful and common. Works as function argument comparison is bivariant
addEventListener(EventType.Mouse, (e: MouseEvent) => console.log(e.x + "," + e.y));

// Undesirable alternatives in presence of soundness
addEventListener(EventType.Mouse, (e: Event) => console.log((<MouseEvent>e).x + "," + (<MouseEvent>e).y));
addEventListener(EventType.Mouse, <(e: Event) => void>((e: MouseEvent) => console.log(e.x + "," + e.y)));

// Still disallowed (clear error). Type safety enforced for wholly incompatible types
addEventListener(EventType.Mouse, (e: number) => console.log(e));
```

また、 `Array <子> 'を`Array <Base> `(共分散)に割り当てることもできます。配列共分散は全ての `Array <Child>`関数が `Array <Base>`に代入可能であることを必要とする。 `push(t：Child)`は関数の引数二項演算によって可能になる `push(t：Base)`に代入可能です。

** これは、他の言語から来ている人には混乱を招く可能性があります**誰がエラーを次のように期待しますが、TypeScriptではそうではないでしょう：

```ts
/** Type Hierarchy */
interface Point2D { x: number; y: number; }
interface Point3D { x: number; y: number; z: number; }

/** Two sample functions */
let iTakePoint2D = (point: Point2D) => { /* do something */ }
let iTakePoint3D = (point: Point3D) => { /* do something */ }

iTakePoint3D = iTakePoint2D; // Okay : Reasonable
iTakePoint2D = iTakePoint3D; // Okay : WHAT
```

## Enums

* 列挙型は数値と互換性があり、数値は列挙型と互換性があります。

```ts
enum Status { Ready, Waiting };

let status = Status.Ready;
let num = 0;

status = num; // OKAY
num = status; // OKAY
```

* 異なる列挙型のEnum値は互換性がないとみなされます。これは、enumを名目上*(構造的にではなく)

```ts
enum Status { Ready, Waiting };
enum Color { Red, Blue, Green };

let status = Status.Ready;
let color = Color.Red;

status = color; // ERROR
```

## クラス

* インスタンスメンバーとメソッドのみが比較されます。 *コンストラクタ*と*静的*は何もしません。

```ts
class Animal {
    feet: number;
    constructor(name: string, numFeet: number) { /** do something */ }
}

class Size {
    feet: number;
    constructor(meters: number) { /** do something */ }
}

let a: Animal;
let s: Size;

a = s;  // OK
s = a;  // OK
```

* `private`と`protected`メンバー*は同じクラスから生まれなければなりません*。そのようなメンバーは本質的にクラス*名義*を作る。

```ts
/** A class hierarchy */
class Animal { protected feet: number; }
class Cat extends Animal { }

let animal: Animal;
let cat: Cat;

animal = cat; // OKAY
cat = animal; // OKAY

/** Looks just like Animal */
class Size { protected feet: number; }

let size: Size;

animal = size; // ERROR
size = animal; // ERROR
```

## ジェネリックス

TypeScriptは構造型システムを備えているため、型パラメータはメンバが使用するときの互換性にのみ影響します。例えば、以下の `T`は互換性に影響を与えません：

```ts
interface Empty<T> {
}
let x: Empty<number>;
let y: Empty<string>;

x = y;  // okay, y matches structure of x
```

しかし、 `T`を使用すると、以下に示すように*インスタンス化*に基づいて互換性の役割を果たします。

```ts
interface NotEmpty<T> {
    data: T;
}
let x: NotEmpty<number>;
let y: NotEmpty<string>;

x = y;  // error, x and y are not compatible
```

ジェネリック引数がインスタンス化されていない*場合、それらは互換性をチェックする前に `any`で置き換えられます：

```ts
let identity = function<T>(x: T): T {
    // ...
}

let reverse = function<U>(y: U): U {
    // ...
}

identity = reverse;  // Okay because (x: any)=>any matches (y: any)=>any
```

クラスを含むジェネリックは、前述のように関連するクラスの互換性によってマッチします。例えば

```ts
class List<T> {
  add(val: T) { }
}

class Animal { name: string; }
class Cat extends Animal { meow() { } }

const animals = new List<Animal>();
animals.add(new Animal()); // Okay 
animals.add(new Cat()); // Okay 

const cats = new List<Cat>();
cats.add(new Animal()); // Error 
cats.add(new Cat()); // Okay
```

## FootNote：不変性

私たちは不変性が唯一の選択肢だと言った。ここでは、 `contra`と`co`の分散の両方が配列にとって危険であると示されている例を示します。

```ts
/** Hierarchy */
class Animal { constructor(public name: string){} }
class Cat extends Animal { meow() { } }

/** An item of each */
var animal = new Animal("animal");
var cat = new Cat("cat");

/**
 * Demo : polymorphism 101
 * Animal <= Cat
 */
animal = cat; // Okay
cat = animal; // ERROR: cat extends animal

/** Array of each to demonstrate variance */
let animalArr: Animal[] = [animal];
let catArr: Cat[] = [cat];

/**
 * Obviously Bad : Contravariance
 * Animal <= Cat
 * Animal[] >= Cat[]
 */
catArr = animalArr; // Okay if contravariant
catArr[0].meow(); // Allowed but BANG 🔫 at runtime


/**
 * Also Bad : covariance
 * Animal <= Cat
 * Animal[] <= Cat[]
 */
animalArr = catArr; // Okay if covariant
animalArr.push(new Animal('another animal')); // Just pushed an animal into catArr!
catArr.forEach(c => c.meow()); // Allowed but BANG 🔫 at runtime
```
