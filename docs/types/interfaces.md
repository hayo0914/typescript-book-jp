## インタフェース(Interfaces)

インタフェースにはJSランタイムでの影響はゼロです。TypeScriptのインターフェースには、変数の構造を宣言するための多くの機能があります。

次の2つは同等の宣言で、最初は*インラインアノテーション*を使用し、2つ目は*インタフェース*を使用します。

```ts
// Sample A
declare var myPoint: { x: number; y: number; };

// Sample B
interface Point {
    x: number; y: number;
}
declare var myPoint: Point;
```

しかし、*サンプルB*の美しさは、`myPoint`ライブラリ上にライブラリを作る誰かが、新しいメンバを追加する際に、簡単に`myPoint`の宣言に新しいメンバを追加できることです：

```ts
// Lib a.d.ts
interface Point {
    x: number; y: number;
}
declare var myPoint: Point;

// Lib b.d.ts
interface Point {
    z: number;
}

// Your code
var myPoint.z; // Allowed!
```

これは、TypeScriptの**インターフェースがオープンエンド**であるためです。これはTypeScriptの重要な教えで、*インターフェース*を使ってJavaScriptの拡張性を模倣することができます。


## クラスはインタフェースを実装できる

誰かがあなたのために`interface`で宣言したオブジェクト構造に従わなければならない*クラス*を使いたい場合、互換性を保証するために`implements`キーワードを使うことができます：

```ts
interface Point {
    x: number; y: number;
}

class MyPoint implements Point {
    x: number; y: number; // Same as Point
}
```

基本的に`implements`したクラスがあるときに、その外部の`Point`インターフェースを変更すると、あなたのコードベースでコンパイルエラーになりますので、簡単に同期を取ることができます：

```ts
interface Point {
    x: number; y: number;
    z: number; // New member
}

class MyPoint implements Point { // ERROR : missing member `z`
    x: number; y: number;
}
```

`implements`はクラスの*インスタンス*の構造を制限することに注意してください。

```ts
var foo: Point = new MyPoint();
```

`foo：Point = MyPoint`のようなものは上記とは異なります。


## ヒント

### すべてのインターフェイスが簡単に実装できるとは限りません

インタフェースは、JavaScriptで可能などんなクレイジーな構造でも宣言できるように設計されています。

`new`をコールできる何かのインターフェースを考えてみましょう：

```ts
interface Crazy {
    new (): {
        hello: number
    };
}
```

基本的な実装は次のようなものです：

```ts
class CrazyClass implements Crazy {
    constructor() {
        return { hello: 123 };
    }
}
// Because
const crazy = new CrazyClass(); // crazy would be {hello:123}
```

インターフェイスを使って世にあるクレイジーなJSを宣言し、TypeScriptから安全に使用することもできます。しかし、それらをTypeScriptクラスとして実装できることを意味しているわけではありません。
