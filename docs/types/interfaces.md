## インタフェース

インタフェースには*実行時JSの影響がありません。変数の構造を宣言するには、TypeScriptインターフェイスに多くの機能があります。

次の2つは同等の宣言で、最初は*インライン注釈*を使用し、2つ目は*インタフェース*を使用します。

```ts
// Sample A
declare var myPoint: { x: number; y: number; };

// Sample B
interface Point {
    x: number; y: number;
}
declare var myPoint: Point;
```

しかし、*サンプルB *の美しさは、新しいメンバを追加するために `myPoint`ライブラリ上に構築されたライブラリを作成する人は、`myPoint`の既存の宣言に簡単に追加することができます：

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

これは、TypeScriptの**インターフェースがオープンエンド**であるためです。これはTypeScriptの重要な教えで、* interfaces *を使ってJavaScriptの拡張性を模倣することができます。


## クラスはインタフェースを実装できます

誰かがあなたのために `interface`で宣言したオブジェクト構造に従わなければならない* classes *を使いたい場合、互換性を保証するために`implements`キーワードを使うことができます：

```ts
interface Point {
    x: number; y: number;
}

class MyPoint implements Point {
    x: number; y: number; // Same as Point
}
```

基本的には `implements`の存在下で、その外部`Point`インターフェースの変更はあなたのコードベースでコンパイルエラーになりますので、簡単に同期させることができます：

```ts
interface Point {
    x: number; y: number;
    z: number; // New member
}

class MyPoint implements Point { // ERROR : missing member `z`
    x: number; y: number;
}
```

`implements`はクラス*インスタンス*の構造を制限することに注意してください。

```ts
var foo: Point = new MyPoint();
```

`foo：Point = MyPoint`のようなものは同じものではありません。


## ヒント

### すべてのインターフェイスが簡単に実装可能ではありません

インタフェースは、JavaScriptに存在するかもしれない任意のクレイジー構造を宣言するように設計されています。

何かが `new`で呼び出し可能な次のインターフェースを考えてみましょう：

```ts
interface Crazy {
    new (): {
        hello: number
    };
}
```

基本的には次のようなものがあります：

```ts
class CrazyClass implements Crazy {
    constructor() {
        return { hello: 123 };
    }
}
// Because
const crazy = new CrazyClass(); // crazy would be {hello:123}
```

あなたはインターフェイスを使ってすべてのクレイジーなJSを宣言し、TypeScriptから安全に使用することもできます。 TypeScriptクラスを使用してそれらを実装できるわけではありません。
