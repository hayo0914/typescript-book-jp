### の
JavaScriptの開発者が経験するよくあるエラーは、配列の `for ... in`が配列項目を反復処理しないということです。代わりに渡されたオブジェクトの* keys *を反復処理します。これは、以下の例で実証されています。ここで `9,2,5`が期待されますが、インデックスは`0,1,2`です。

```ts
var someArray = [9, 2, 5];
for (var item in someArray) {
    console.log(item); // 0,1,2
}
```

これは、for ... ofがTypeScript(およびES6)に存在する理由の1つです。次のように、配列を繰り返し処理して、期待どおりにメンバーを正しくログアウトします。

```ts
var someArray = [9, 2, 5];
for (var item of someArray) {
    console.log(item); // 9,2,5
}
```

同様に、TypeScriptは文字列ごとに `for ... of`を使っても問題はありません：

```ts
var hello = "is it me you're looking for?";
for (var char of hello) {
    console.log(char); // is it me you're looking for?
}
```

#### JS Generation
プレES6ターゲットの場合、TypeScriptは標準の `for(var i = 0; i <list.length; i ++)`種類のループを生成します。たとえば、前の例で生成されるものを次に示します。
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
`for ... of`を使うと、* intent *がより明確になることがわかりますし、書くべきコードの量も増えます(そして、あなたが思いつくべき変数名)。

#### 制限事項
ES6以上をターゲットにしていない場合、生成されたコードはオブジェクトに「長さ」というプロパティが存在することを前提としています。 `obj [2]`。したがって、これらのレガシーJSエンジンの `string`と`array`でのみサポートされています。

TypeScriptが配列や文字列を使用していないことがわかった場合は、「配列型でも文字列型でもない」*
```ts
let articleParagraphs = document.querySelectorAll("article > p");
// Error: Nodelist is not an array type or a string type
for (let paragraph of articleParagraphs) {
    paragraph.classList.add("read");
}
```

あなたが知っている*配列や文字列であるものだけ `for ... of`を使います。この制限は、TypeScriptの将来のバージョンでは削除される可能性があることに注意してください。

#### 要約
配列の要素を何回反復するかは驚くでしょう。次回あなたがそれをしているのを見て、「〜のために〜を」与えてください。自分のコードを見直す次の人を幸せにするだけかもしれません。
