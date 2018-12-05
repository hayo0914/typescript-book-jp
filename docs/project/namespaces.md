## ネームスペース
ネームスペースは、JavaScriptで使用される一般的なパターンに関する便利な構文を提供します。

```ts
(function(something) {

    something.foo = 123;

})(something || (something = {}))
```

基本的には何か|| (something = {}) `は、無名関数`function(something){} `を既存のオブジェクト*(`something || `部分)に追加するか、 ( `||(something = {})`の部分)。つまり、いくつかの実行境界で分割された2つのブロックを持つことができます。

```ts
(function(something) {

    something.foo = 123;

})(something || (something = {}))

console.log(something); // {foo:123}

(function(something) {

    something.bar = 456;

})(something || (something = {}))

console.log(something); // {foo:123, bar:456}

```

これは、グローバルな名前空間にものが漏れないようにJavaScriptの土地でよく使われます。ファイルベースのモジュールでは、これを心配する必要はありませんが、パターンは、一連の関数の* logical grouping *にはまだ役立ちます。そのため、TypeScriptは、例えばnamespaceというキーワードをグループ化してグループ化します。

```ts
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

```ts
(function (Utility) {

// Add stuff to Utility

})(Utility || (Utility = {}));
```

注意すべきことは、名前空間を入れ子にすることができるので、 `名前空間Utility.Messaging`のようなものが`ユーティリティ `の下に`Messaging`名前空間を入れ子にすることができるということです。

ほとんどのプロジェクトでは、外部モジュールを使用し、デモと移植用の古いJavaScriptコードを移植するために `namespace`を使用することをお勧めします。
