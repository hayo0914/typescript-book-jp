# Type Instantiation

たとえば、ジェネリックパラメータを持つものがあるとします。クラス`Foo`です：

```typescript
class Foo<T>{
    foo: T;
}
```

特定の型の特殊バージョンを作成したいとします。このパターンは、項目を新しい変数にコピーし、ジェネリックを具体的な型に置き換えた型アノテーションを与えることです。例えば。 `Foo<number>`クラスが必要な場合です：

```typescript
class Foo<T>{
    foo: T;
}
let FooNumber = Foo as { new ():Foo<number> }; // ref 1
```

`ref 1`では、`FooNumber`は`Foo`と同じですが、`new`演算子で呼び出されたときに `Foo<Number>`のインスタンスを与えるものとして扱います。

## 継承

型アサーションパターンは、あなたが正しいことをする、と信じているという意味では安全ではありません。クラスの他の言語での共通パターンは継承を使うことです：

```typescript
class FooNumber extends Foo<number>{}
```

ここで注意しなければならないのは、デコレータをベースクラスで使用すると、継承されたクラスはベースクラスと同じ動作をしない可能性があることです\(それは、もはやデコレータでラップされません\)。

もちろん、クラスを特殊化していない場合でも、型強制/アサーションパターンがワークする方法を考える必要があります。なので、まず一般的なアサーションパターンを示します。

```typescript
function id<T>(x: T) { return x; }
const idNum = id as {(x:number):number};
```

> この[stackoverflowの質問](http://stackoverflow.com/a/34864705/390330)にインスパイアされました

