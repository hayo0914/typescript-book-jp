## 型の互換性(Type Compatibility)

型の互換性は、あるものを別のものに割り当てることができるかどうかを決定します。例えば`string`と`number`は互換性がありません：

```ts
let str: string = "Hello";
let num: number = 123;

str = num; // ERROR: `number` is not assignable to `string`
num = str; // ERROR: `string` is not assignable to `number`
```

## 健全性(Soundness)

TypeScriptの型システムは便利であるように設計されているため、不健全な振る舞いをすることも可能にしています。例えば、何かを`any`型にすることができます。これは、あなたが望むことを何でもできるようにすることをコンパイラに指示することを意味します：

```ts
let foo: any = 123;
foo = "Hello";

// Later
foo.toPrecision(3); // Allowed as you typed it as `any`
```

## 構造的(Structual)

TypeScriptオブジェクトは構造的に型付けされています。つまり、型名は構造が一致する限り重要ではありません

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

これにより、(素のJSのように)すばやくオブジェクトを作成することができ、推論が可能な場合でも安全性が保たれます。

また、より多くのデータが存在することは問題なしとされます:

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

## バリアンス(Variance)

バリアンスは、型の互換性分析のために理解しやすく、重要な概念です。

単純な型`Base`と`Child`の場合、`Child`が`Base`の子であれば、`Child`のインスタンスは`Base`型の変数に代入することができます。

> これはポリモーフィズム101です

このような`Base`型と`Child`型で構成される複合型の型互換性は、類似のシナリオにおける`Base`と`Child`がバリアンス(variance)によって制御されることに依存しています。

* コバリアント(Covariant)：(coはjointの意味)同じ方向のみ
* コントラバリアント(Contravariant)：(contraはnegativeの意味)反対の方向にのみ
* バイバリアント(Bivariant)：(biはbothの意味)coとcontraの両方。
* インバリアント(Invariant)：型がまったく同じでない場合、それらは互換性がありません。

> 注意：JavaScriptのようなミュータブル(変更可能)なデータの存在下で、完全に健全な型システムのためには`invariant`が唯一有効なオプションです。しかし、述べたように利便性によって、私たちは不健全な選択をせざるを得ません。

## 関数(Functions)

2つの関数を比較するときには、いくつか些細なことを考慮する必要があります。

### 戻り値の型(Return Type)

`covariant`：戻り型は少なくとも十分なデータを含んでいなければなりません。

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

引数が少ないのは問題ありません(つまり、関数は追加のパラメータを無視することができます)。少なくとも十分な引数で呼び出されることが保証されています。

```ts
let iTakeSomethingAndPassItAnErr
    = (x: (err: Error, data: any) => void) => { /* do something */ };

iTakeSomethingAndPassItAnErr(() => null) // Okay
iTakeSomethingAndPassItAnErr((err) => null) // Okay
iTakeSomethingAndPassItAnErr((err, data) => null) // Okay

// ERROR: Argument of type '(err: any, data: any, more: any) => null' is not assignable to parameter of type '(err: Error, data: any) => void'.
iTakeSomethingAndPassItAnErr((err, data, more) => null);
```

### オプションおよび可変長(Rest)パラメータ

(事前に決定された数の)オプションパラメータおよび可変長パラメータ(任意の数)は、(繰り返しになりますが)利便性のために互換性があります。

```ts
let foo = (x:number, y: number) => { /* do something */ }
let bar = (x?:number, y?: number) => { /* do something */ }
let bas = (...args: number[]) => { /* do something */ }

foo = bar = bas;
bas = bar = foo;
```

> 注意：strictNullChecksがfalseの場合、オプション引数(ここでは`bar`)とオプションではない引数(この例では`foo`)のみ互換性があります。

### 引数のタイプ

`bivariant`：これは一般的なイベント処理のシナリオをサポートするように設計されています

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

また、`Array<Child>`を`Array<Base>`(Covariance)に関数として割り当てることもできます。配列のCovarianceはすべての`Array<Child>`関数が`Array<Base>`に代入可能であることを必要とします。例えば`push(t:Child)`は関数パラメータのBivarianceによって`push(t:Base)`に代入可能です。

これは他の言語から来た人はエラーになると予測するかもしれません。**混乱を招く可能性がありますが、**これはTypeScriptではエラーになりません：

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

## 列挙型(Enums)

* 列挙型は数値と互換性があり、数値は列挙型と互換性があります。

```ts
enum Status { Ready, Waiting };

let status = Status.Ready;
let num = 0;

status = num; // OKAY
num = status; // OKAY
```

* 異なる列挙型のEnum値は互換性がないとみなされます。これによって、列挙型を(構造的にではなく)nominalに使うことができます

```ts
enum Status { Ready, Waiting };
enum Color { Red, Blue, Green };

let status = Status.Ready;
let color = Color.Red;

status = color; // ERROR
```

## クラス(Classes)

* インスタンスメンバとメソッドのみが比較されます。コンストラクタと静的メンバに関しては何もしません。

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

* `private`と`protected`メンバは同じクラスで書かれたものでなければなりません。そのようなメンバは、本質的にそのクラスをnominalにします。

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

## ジェネリクス(Generics)

TypeScriptは構造的な型システムを備えているため、型パラメータはメンバが使用するときの互換性にのみ影響します。例えば、以下の`T`は互換性に影響を与えません：

```ts
interface Empty<T> {
}
let x: Empty<number>;
let y: Empty<string>;

x = y;  // okay, y matches structure of x
```

しかし、`T`を使用すると、以下に示すようにインスタンス化に基づいて互換性チェックの働きをします。

```ts
interface NotEmpty<T> {
    data: T;
}
let x: NotEmpty<number>;
let y: NotEmpty<string>;

x = y;  // error, x and y are not compatible
```

ジェネリック引数がインスタンス化されていない場合、それらは互換性をチェックする前に`any`で置き換えられます：

```ts
let identity = function<T>(x: T): T {
    // ...
}

let reverse = function<U>(y: U): U {
    // ...
}

identity = reverse;  // Okay because (x: any)=>any matches (y: any)=>any
```

クラスを含むジェネリックは、前述のように関連するクラスの互換性によってマッチされます。例:

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

## ノート： Invariance

私たちは不変性が唯一の健全な選択肢だと言いました。ここでは、`contra`と`co`のVarianceの両方が配列に危険である例を示します。

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
