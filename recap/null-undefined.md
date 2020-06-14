# nullとundefined

JavaScript\(と、TypeScript\)は、`null`と`undefined`という2つのボトム型\(bottom type\)があります。これらは異なる意味を持っています。

* 初期化されていない： `undefined`。
* 現在利用できない： `null`。

## どちらであるかをチェックする

現実としては、あなたは両方とも対応する必要があります。`==`でチェックしましょう:

```typescript
/// `foo.bar == undefined` のようなコードを書いたときに、何が起きるか想像してみてください:
console.log(undefined == undefined); // true
console.log(null == undefined); // true

// このようなチェックをすれば、falsyな値について心配する必要はありません
console.log(0 == undefined); // false
console.log('' == undefined); // false
console.log(false == undefined); // false
```

`== null`を使って`undefined`と `null`を両方ともチェックすることを推奨します。一般的に2つを区別する必要はありません。

```typescript
function foo(arg: string | null | undefined) {
  if (arg != null) {
    // `!=` がnullとundefinedを除外しているので、引数argは文字列です
  }
}
```

1つだけ例外があります。次に説明するルートレベル\(root level\)のundefinedの値です。

## ルートレベル\(root level\)のundefinedのチェック

`== null`を使うべきだと言ったことを思い出してください。もちろん、覚えているでしょう\(今、言ったばかりなので\)。それは、ルートレベルのものには使用しないでください。 strictモード\(strict mode\)で`foo`を使うとき、`foo`が定義されていないと、`ReferenceError` **exception**が発生し、コールスタック全体がアンワインド\(unwind\)されます。

> strictモードを使うべきです...現実としては、TSコンパイラはモジュール\(modules\)を使うときに、自動的に`"use strict";`を挿入します...後で解説を行うので、詳細は省略します:\)

変数が_global_レベルで定義されているかどうかを確認するには、通常、`typeof`を使用します：

```typescript
if (typeof someglobal !== 'undefined') {
  // これでsomeglobalは安全に利用できます
  console.log(someglobal);
}
```

## `undefined` の明示的な利用を制限する

TypeScriptでは値と構造を分離してドキュメントのようにわかりやすくすることができます。下記のようなコードを想像してください:

```typescript
function foo(){
  // if 何らかの場合に返す値
  return {a:1,b:2};
  // else それ以外の場合に返す値
  return {a:1,b:undefined};
}
```

これは、次のように型アノテーションを使用すべきです。

```typescript
function foo():{a:number,b?:number}{
  // if 何らかの場合に返す値
  return {a:1,b:2};
  // else それ以外の場合に返す値
  return {a:1};
}
```

## Nodeスタイルのコールバック

Nodeスタイルのコールバック関数\(例: `(err, somethingElse)=> {/* something */}`\)は、エラーがなければ `err`に`null`を設定して呼び出されます。開発者は一般的にtruthyチェックを行います：

```typescript
fs.readFile('someFile', 'utf8', (err,data) => {
  if (err) {
    // 何らかのエラー処理をする
  } else {
    // エラーなし
  }
});
```

独自のAPIを作成するときは、一貫性のために`null`を使用することは、良くはありませんが、問題ありません。とはいえ、できればPromiseを返すようにするべきです。そうすれば、`err`が`null`かどうかを気にかける必要はなくなります\(`.then`と`.catch`を使います\)。

## 値の有効性を表す意味で`undefined`を使用しない

下記は、ひどい関数の例です:

```typescript
function toInt(str:string) {
  return str ? parseInt(str) : undefined;
}
```

下記のようにする方が、はるかに良いでしょう：

```typescript
function toInt(str: string): { valid: boolean, int?: number } {
  const int = parseInt(str);
  if (isNaN(int)) {
    return { valid: false };
  }
  else {
    return { valid: true, int };
  }
}
```

## JSONとシリアライズ

JSON標準では、`null`のエンコードはサポートしていますが、`undefined`のエンコードはサポートしていません。値が`null`である属性を持つオブジェクトをJSONにエンコードするとき、その属性は`null`値とともにJSONに含まれますが、値が`undefined`である属性は完全に除外されます。

```typescript
JSON.stringify({willStay: null, willBeGone: undefined}); // {"willStay":null}
```

結果として、JSONベースのデータベースは、`null`はサポートしますが`undefined`はサポートしないことがあります。`null`値を持つ属性はエンコードされるため、オブジェクトをエンコードしてリモートのデータストアに送る前に、ある属性値を`null`にすることで、その属性をクリアしたいという意図を明確に伝えることができます。

属性値を`undefined`にすると、その属性はJSONにエンコードされないため、データのストレージと転送のコストを節約することができます。しかし、これによって、値をクリアすることと、値が存在しないことの文脈を曖昧にしてしまいます。

## 結論

TypeScriptチームは、`null`を使いません: [TypeScriptコーディングガイドライン](https://github.com/Microsoft/TypeScript/wiki/Coding-guidelines#null-and-undefined)。 そして、問題は起きていません。 Douglas Crockfordは[nullは良くない考え](https://www.youtube.com/watch?v=PSGEjv3Tqo0&feature=youtu.be&t=9m21s)であり、誰もが`undefined`だけを使うべきだと考えています。

しかし、Nodeスタイルのコードでは、Error引数に`null`が標準で使われています。これは`何かがおかしいです`という意味です。私は個人的に、ほとんどのプロジェクトにおいて、意見がバラバラのライブラリを使っていますが、`== null`で除外するだけなので、2つの区別について気にすることはありません。

