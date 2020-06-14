# 残余引数（Restパラメータ）

可変長引数\(引数の最後に`...argumentName`と書く\)を受け取る場合、以下のように関数に渡された複数の引数をすぐに配列として取得できます:

```typescript
function iTakeItAll(first, second, ...allOthers) {
    console.log(allOthers);
}
iTakeItAll('foo', 'bar'); // []
iTakeItAll('foo', 'bar', 'bas', 'qux'); // ['bas','qux']
```

可変長引数は、`function`/`()=>`/`class member`の関数で使うことができます。なお、可変長引数でなくてもRestパラメータを利用できることに注意してください。





