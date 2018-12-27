# シングルトンパターン

従来のシングルトンパターンは、実際には、すべてのコードが`class`内になければならないという事実を克服するために使用されるものです。

```ts
class Singleton {
    private static instance: Singleton;
    private constructor() {
        // do something construct...
    }
    static getInstance() {
        if (!Singleton.instance) {
            Singleton.instance = new Singleton();
            // ... any one time initialization goes here ...
        }
        return Singleton.instance;
    }
    someMethod() { }
}

let something = new Singleton() // Error: constructor of 'Singleton' is private.

let instance = Singleton.getInstance() // do something with the instance...
```

しかし、遅延初期化をしたくない場合は、単に`namespace`を使うことができます：

```ts
namespace Singleton {
    // ... any one time initialization goes here ...
    export function someMethod() { }
}
// Usage
Singleton.someMethod();
```

> 警告：シングルトンは単に [global](http://stackoverflow.com/a/142450/390330) をファンシーな名前にしたものです。

ほとんどのプロジェクトでは、`namespace`をさらにモジュールに置き換えることができます。

```ts
// someFile.ts
// ... any one time initialization goes here ...
export function someMethod() { }

// Usage
import {someMethod} from "./someFile";
```


