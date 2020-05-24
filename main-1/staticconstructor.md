# static constructors

TypeScriptの`class`は\(JavaScriptの`class`のような\)静的なコンストラクタを持つことはできません。しかし、自分で呼び出すだけで、同じ効果を得ることができます。

```typescript
class MyClass {
    static initialize() {
        // Initialization
    }
}
MyClass.initialize();
```

