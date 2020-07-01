# for...of

JavaScript初心者がよく経験するエラーは、`for...in`が配列の要素を反復しないということです。代わりに渡されたオブジェクトの_keys_を反復します。これを以下の例で示します。ここでは`9,2,5`の表示が期待されていますが、インデックス`0,1,2`が表示されます。

```typescript
var someArray = [9, 2, 5];
for (var item in someArray) {
    console.log(item); // 0,1,2
}
```

これは、for...ofがTypeScript\(およびES6\)に存在する理由の1つです。次のように、配列を繰り返し処理して、期待どおりに要素をログに出力します。

```typescript
var someArray = [9, 2, 5];
for (var item of someArray) {
    console.log(item); // 9,2,5
}
```

TypeScriptでは、同様に文字列に対して`for...of`を使っても問題ありません：

```typescript
var hello = "is it me you're looking for?";
for (var char of hello) {
    console.log(char); // 次のものが出力されます: is it me you're looking for?
}
```

## 生成されるJavaScript

ES6未満をターゲットにコンパイルした場合、TypeScriptは標準的な`for(var i = 0; i < list.length; i++)`のループを生成します。たとえば、前の例で生成されるものを次に示します。

```typescript
var someArray = [9, 2, 5];
for (var item of someArray) {
    console.log(item);
}

// このようになります //

for (var _i = 0; _i < someArray.length; _i++) {
    var item = someArray[_i];
    console.log(item);
}
```

`for...of`を使うと、開発者の意図がより明確になりますし、コードの量が減ります\(そして、頭からひねり出さないといけない変数名も減ります\)。

## 制限事項

ES6未満をターゲットにしている場合、コンパイルによって生成されるコードは、オブジェクトに`length`というプロパティが存在していること、数値のインデックス\(`obj[2]`など\)が使えることを前提にしています。なので、これらの古いJavaScriptエンジンでは、`string`と`array`のみがサポートされています。

もし`string`や`array`以外で`for...of`を使用している場合は、TypeScriptはわかりやすいエラーを出力します: "array型またはstring型ではありません"。

```typescript
let articleParagraphs = document.querySelectorAll("article > p");
// Error: これはarray型まはたstring型ではありません
for (let paragraph of articleParagraphs) {
    paragraph.classList.add("read");
}
```

`string`や`array`であることが確実である場合だけ `for ... of`を使ってください。この制限は、TypeScriptの将来のバージョンでは削除される可能性がありますので、注意してください。

## まとめ

配列の反復処理をどれだけ多く書くことになるかを知ったら、あなたは驚くでしょう。その時には、`for...of`を使ってください。あなたのコードのレビュアーが喜ぶかもしれません。

