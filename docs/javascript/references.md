## 参照(Refences)

リテラル以外にも、JavaScriptのあらゆるオブジェクト(関数、配列、正規表現など)は参照(reference)です。これは、次のことを意味します。

### 変更(Mutation)はすべての参照に影響する

```js
var foo = {};
var bar = foo; // bar is a reference to the same object

foo.baz = 123;
console.log(bar.baz); // 123
```

### 比較は、参照に対して行われる

```js
var foo = {};
var bar = foo; // bar is a reference
var baz = {}; // baz is a *new object* distinct from `foo`

console.log(foo === bar); // true
console.log(foo === baz); // false
```
