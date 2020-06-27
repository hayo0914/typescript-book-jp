# 名前空間

名前空間は、JavaScriptで一般的に使われる次のようなパターンと同じことを実現できる構文です。

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

このパターンは、グローバルな名前空間を汚染しないようにJavaScriptでよく使われるパターンです。ファイルモジュールの場合、グローバルの名前空間の汚染を心配する必要はありません。しかし、それでも、一連の関数を論理的にグループ化することに役立ちます。TypeScriptは、`namespace`キーワードを使って、次のようにコードをグループ化する手段を提供しています:

```typescript
namespace Utility {
    export function log(msg) {
        console.log(msg);
    }
    export function error(msg) {
        console.error(msg);
    }
}

// 使い方
Utility.log('Call me');
Utility.error('maybe!');
```

`namespace`キーワードは、先ほど見たのと同じJavaScriptを生成します：

```typescript
(function (Utility) {

// ユーティリティとして使う何らかのコード

})(Utility || (Utility = {}));
```

一点、注意していただきたいことは、名前空間を入れ子にすることができるということです。なので、`Utility`の下に`Messaging`名前空間を追加するために、`namespace Utility.Messaging`のようなことができます。

大抵のプロジェクトでは、`namespace`ではなく、ファイルモジュールを使うことを推奨します。`namespace`は単に試したり、古いJavaScriptコードを移植するために使うことを推奨します。

