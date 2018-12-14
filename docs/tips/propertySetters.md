## プロパティのsetterの使用を制限する(Limit usage of property setters)

setter/getterより明示的なset/get関数(例えば`setBar`や`getBar`関数)を使うことをお勧めします。

次のコードを考えてみましょう：

```ts
foo.bar = {
    a: 123,
    b: 456
};
```

setter/getterの存在する例:

```ts
class Foo {
    a: number;
    b: number;
    set bar(value:{a:number,b:number}) {
        this.a = value.a;
        this.b = value.b;
    }
}
let foo = new Foo();
```

これはプロパティのsetterの良い使い方ではありません。最初のコードサンプルを読んでいる人は、fooの何かが変わるとは思っていません。一方、`foo.setBar(value)`を呼び出す人は、`foo`で何かが変わるかもしれないと考える可能性が高いです。

> ボーナスポイント：異なる複数の関数がある場合は、参照を探す方が良いです。TypeScriptツールでは、getterまたはsetterの参照が見つかった場合は両方を取得しますが、明示的な関数呼び出しでは関係がある関数への参照のみを取得します。
