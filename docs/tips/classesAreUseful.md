## クラスは便利です(Classes Are Useful)

次の構造を持つことは非常に一般的です。

```ts
function foo() {
    let someProperty;

    // Some other initialization code

    function someMethod() {
        // Do some stuff with `someProperty`
        // And potentially other things
    }
    // Maybe some other methods

    return {
        someMethod,
        // Maybe some other methods
    };
}
```

これはリビーリングモジュールパターン(revealing module pattern)と呼ばれ、JavaScriptではかなり一般的です(JavaScriptのクロージャを利用しています)。

[*ファイルモジュール*(グローバルスコープは良くないので、あなたは本当にそれを使うべきです)]](../project/modules.md)を使用している場合、あなたのファイルは事実上同じです。しかし、人々が次のようなコードを書くケースがあまりにも多くあります。

```ts
let someProperty;

function foo() {
   // Some initialization code
}
foo(); // some initialization code

someProperty = 123; // some more initialization

// Some utility function not exported

// later
export function someMethod() {

}
```

私は継承が大好きではありませんが、私は人々がクラスを使用することで、コードをより良く整理することができる、ということを発見しました。同じ開発者が直感的に次のように書きます：

```ts
class Foo {
    public someProperty;

    constructor() {
        // some initialization
    }

    public someMethod() {
        // some code
    }

    private someUtility() {
        // some code
    }
}

export = new Foo();
```

また、単に開発者のことだけでなく、クラスを使って、優れた視覚化を実現する開発ツールを作成することはずっと一般的であり、また、チームが理解し維持する必要があるパターンが1つ少なくなります。

> PS：*shallow*なクラス階層に関して、それが大幅な再利用とボイラープレートの削減を提供する場合、私の意見には間違いがありません。
