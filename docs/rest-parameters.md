### 残りのパラメータ
残りの引数(最後の引数に `... argumentName`と表示されます)を使うと、関数内の複数の引数を素早く受け入れ、配列として取得できます。これは以下の例で実証されています。

```ts
function iTakeItAll(first, second, ...allOthers) {
    console.log(allOthers);
}
iTakeItAll('foo', 'bar'); // []
iTakeItAll('foo', 'bar', 'bas', 'qux'); // ['bas','qux']
```

restパラメータは、 `function`/`()=> `/`class member`のような関数で使うことができます。
