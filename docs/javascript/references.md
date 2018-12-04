## 参考文献

リテラル以外にも、JavaScriptのあらゆるオブジェクト（関数、配列、正規表現など）は参照です。これは、次のことを意味します

### 突然変異はすべての参照に渡っている

```js
var foo = {};
var bar = foo; // bar is a reference to the same object

foo.baz = 123;
console.log(bar.baz); // 123
```

### 平等は参照用です

```js
var foo = {};
var bar = foo; // bar is a reference
var baz = {}; // baz is a *new object* distinct from `foo`

console.log(foo === bar); // true
console.log(foo === baz); // false
```
