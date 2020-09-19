## インターフェース(Interfaces)

インターフェースは、JavaScriptランタイム上では、何の影響もありません。TypeScriptのインターフェースは、オブエジェクトの構造を宣言するための多くの機能があります。

次の2つは同じ意味の宣言です。１つ目はインラインの型定義を使用し、2つ目はインターフェースを使用しています。

```ts
// Sample A
declare var myPoint: { x: number; y: number; };

// Sample B
interface Point {
    x: number; y: number;
}
declare var myPoint: Point;
```

しかし、*サンプル B*の美しいところは、`myPoint` このライブラリを使って、別のライブラリを作る誰かが、新しいプロパティを追加する際に、簡単に`myPoint`の宣言を拡張して、新しいプロパティを追加できることです：

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

これは、TypeScriptの**インターフェースが拡張に対してオープン**であるためです。これはTypeScriptの重要な教えです。*インターフェース*は、JavaScriptの拡張性と同じことを実現しています。

## クラスはインターフェースを実装できる

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

### すべてのインターフェースが簡単に実装できるとは限りません

インターフェースは、JavaScriptで可能などんな変な構造でも宣言できるように設計されています。

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

インターフェースを使って変な構造を宣言し、TypeScriptの型のサポートを得つつ、安全に使用することもできます。しかし、それらをTypeScriptのクラスとして実装できるとは限りません。
