# TypeScriptの静的コンストラクタ

TypeScript `class`（JavaScriptの`class`のような）は静的なコンストラクタを持つことはできません。しかし、自分で呼び出すだけで、同じ効果を得ることができます。

```ts
class MyClass {
    static initialize() {
        // Initialization
    }
}
MyClass.initialize();
```
