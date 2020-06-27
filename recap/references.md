# リファレンス

リテラル以外にも、JavaScriptにおけるすべてのオブジェクト\(関数、配列、正規表現 etc\)は参照\(references\)です。これは、以下のことを意味します。

## 変更\(Mutation\)はすべての参照\(references\)に影響する

```javascript
var foo = {};
var bar = foo; // bar is a reference to the same object

foo.baz = 123;
console.log(bar.baz); // 123
```

## 比較は、参照\(references\)に対して行われる

```javascript
var foo = {};
var bar = foo; // bar is a reference
var baz = {}; // baz is a *new object* distinct from `foo`

console.log(foo === bar); // true
console.log(foo === baz); // false
```

