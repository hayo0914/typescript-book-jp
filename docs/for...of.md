### for...of
JavaScriptの初心者がよく経験するエラーは、`for...in`が配列要素を反復しないということです。代わりに渡されたオブジェクトの*keys*を反復します。これを以下の例で示します。ここでは`9,2,5`の表示が期待されていますが、インデックス`0,1,2`が表示されます。

```ts
var someArray = [9, 2, 5];
for (var item in someArray) {
    console.log(item); // 0,1,2
}
```

これは、for...ofがTypeScript(およびES6)に存在する理由の1つです。次のように、配列を繰り返し処理して、期待どおりに要素をログに出力します。

```ts
var someArray = [9, 2, 5];
for (var item of someArray) {
    console.log(item); // 9,2,5
}
```

TypeScriptでは、同様に文字列に対して`for...of`を使っても問題ありません：

```ts
var hello = "is it me you're looking for?";
for (var char of hello) {
    console.log(char); // is it me you're looking for?
}
```

#### 生成されるJS
ES6未満をターゲットにした場合、TypeScriptは標準的な`for(var i = 0; i <list.length; i ++)`のループを生成します。たとえば、前の例で生成されるものを次に示します。
```ts
var someArray = [9, 2, 5];
for (var item of someArray) {
    console.log(item);
}

// becomes //

for (var _i = 0; _i < someArray.length; _i++) {
    var item = someArray[_i];
    console.log(item);
}
```
`for...of`を使うと、意図がより明確になりますし、書くべきコードの量が減ります(そして、ひねり出さないといけない変数名も)。

#### 制限事項
ES6以上をターゲットにしていない場合、生成されたコードはオブジェクトに`length`というプロパティが存在していることと、数値によってインデックスされていること(`obj[2]`など)を前提としています。したがって、これらのレガシーなJSエンジンでは、`string`と`array`のみサポートされています。

もしTypeScriptが配列や文字列を使用していないことを知った場合は、明確なエラーを出力します:"is not an array type or a string type"。

```ts
let articleParagraphs = document.querySelectorAll("article > p");
// Error: Nodelist is not an array type or a string type
for (let paragraph of articleParagraphs) {
    paragraph.classList.add("read");
}
```

配列や文字列であると知っているものにだけ `for ... of`を使ってください。この制限は、TypeScriptの将来のバージョンでは削除される可能性があることに注意してください。

#### 要約
配列の反復処理をどれだけの回数書くことになるかを知ったらあなたは驚くでしょう。次にそれを行うことになったら、`for...of`を使ってください。あなたのコードを次にレビューする人が嬉しくなるかもしれません。
