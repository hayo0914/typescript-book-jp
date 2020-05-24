# namespace（名前空間）

名前空間は、JavaScriptで使用される次の一般的なパターンの便利な構文を提供します。

```typescript
(function(something) {

    something.foo = 123;

})(something || (something = {}))
```

基本的に、`something || (something = {})`は、無名関数`function(something) {}`が何かを既存オブジェクト\(`something ||`部分\)に追加するか、新しいオブジェクト\( `|| (something = {})`の部分\)を作って何かを追加することを可能にします。これが意味することは、このように何らかの分岐で分割された2つのブロックを持つことができるということです。

```typescript
(function(something) {

    something.foo = 123;

})(something || (something = {}))

console.log(something); // {foo:123}

(function(something) {

    something.bar = 456;

})(something || (something = {}))

console.log(something); // {foo:123, bar:456}
```

これは、グローバルな名前空間を汚染しないようにJavaScriptでよく使われます。ファイルベースのモジュールでは、これを心配する必要はありませんが、このパターンは、それでも、一連の関数の論理グループ化\(logical grouping\)に役立ちます。そのため、TypeScriptは、`namespace`キーワードを使ってグループ化する手段を提供します:

```typescript
namespace Utility {
    export function log(msg) {
        console.log(msg);
    }
    export function error(msg) {
        console.error(msg);
    }
}

// usage
Utility.log('Call me');
Utility.error('maybe!');
```

`namespace`キーワードは、先ほど見たのと同じJavaScriptを生成します：

```typescript
(function (Utility) {

// Add stuff to Utility

})(Utility || (Utility = {}));
```

注意すべきことは、名前空間を入れ子にすることができるので、`Utility`の下に`Messaging`名前空間を入れ子にするために`namespace Utility.Messaging`のようなことができるということです。

たいていのプロジェクトでは、簡単なデモと古いJavaScriptコードを移植するために、外部モジュールと`namespace`を使用することをオススメします。

