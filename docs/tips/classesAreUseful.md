## クラスは有用です

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

これは*明らかなモジュールパターン*と呼ばれ、JavaScriptではかなり一般的です(JavaScriptクロージャを利用しています)。

[* file modules *(グローバルスコープが悪いので本当に必要です)]](../ project / modules.md)を使用すると、ファイルは事実上同じ*になります。しかし、人々が次のようなコードを書くことはあまりにも多くあります。

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

私は継承の大きなファンではありませんが、私は人々がクラスを使用させることでコードをより良く整理することができます*。同じ開発者が直感的に次のように書く：

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

また、開発者だけでなく、クラスの上で優れた視覚化を実現する開発ツールを作成することはずっと一般的であり、チームが理解し維持する必要があるパターンは1つ少なくなります。

> PS：ボイラープレートの大幅な再利用と削減を提供する場合は、* shallow *クラス階層については私の意見に間違いがありません。
