## NullとUndefined
JavaScript(と、TypeScript)は、`null`と`undefined`という2つのボトム型(bottom type)があります。これらは異なる意味を持っています。

* 初期化されていない： `undefined`。
* 現在利用できない： `null`。


### どちらであるかをチェックする

現実としては、あなたは両方とも対応する必要があります。`==`でチェックしましょう:

```ts
/// Imagine you are doing `foo.bar == undefined` where bar can be one of:
console.log(undefined == undefined); // true
console.log(null == undefined); // true

// You don't have to worry about falsy values making through this check
console.log(0 == undefined); // false
console.log('' == undefined); // false
console.log(false == undefined); // false
```

`== null`を使って`undefined`と `null`を両方ともチェックすることを推奨します。一般的に２つを区別する必要はありません。

```ts
function foo(arg: string | null | undefined) {
  if (arg != null) {
    // `!=` がnullとundefinedを除外しているので、引数argは文字列です
  }
}
```

１つだけ例外があります。次に説明するルートレベル(root level)のundefinedの値です。

### ルートレベル(root level)のundefinedのチェック

`== null`を使うべきだと言ったことを思い出してください。もちろん、覚えているでしょう(今、言ったばかりなので)。それは、ルートレベルのものには使用しないでください。 strictモード(strict mode)で`foo`を使うとき、`foo`が定義されていないと、`ReferenceError` **exception**が発生し、コールスタック全体がアンワインド(unwind)されます。

> strictモードを使うべきです...現実としては、TSコンパイラはモジュール(modules)を使うときに、自動的に`"use strict";`を挿入します...後で解説を行うので、詳細は省略します:)

変数が*global*レベルで定義されているかどうかを確認するには、通常、`typeof`を使用します：

```ts
if (typeof someglobal !== 'undefined') {
  // someglobal is now safe to use
  console.log(someglobal);
}
```

### `undefined`を使わないようにする
TypeScriptにおいて、あなたは、変数と構造を分離して型を記述することができます。下記のように書く代わりに:
```ts
function foo(){
  // if Something
  return {a:1,b:2};
  // else
  return {a:1,b:undefined};
}
```
型アノテーションを使用すべきです。
```ts
function foo():{a:number,b?:number}{
  // if Something
  return {a:1,b:2};
  // else
  return {a:1};
}
```

### Nodeスタイルのコールバック
Nodeスタイルのコールバック関数(例: `(err, somethingElse)=> {/* something */}`)は、エラーがなければ `err`に`null`を設定して呼び出されます。開発者は一般的にtruthyチェックを行います：

```ts
fs.readFile('someFile', 'utf8', (err,data) => {
  if (err) {
    // do something
  } else {
    // no error
  }
});
```
独自のAPIを作成するときは、一貫性のために`null`を使用することは、良くはありませんが、問題ありません。とはいえ、できればPromiseを返すようにするべきです。そうすれば、`err`が`null`かどうかを気にかける必要はなくなります(`.then`と`.catch`を使います)。

### 有効性(validity)の意味で`undefined`を使用しない

ひどい関数の例:

```ts
function toInt(str:string) {
  return str ? parseInt(str) : undefined;
}
```
このほうがはるかに良い：
```ts
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

### JSONとシリアライズ

JSON標準では、`null`のエンコードはサポートしていますが、`undefined`のエンコードはサポートしていません。値が`null`である属性を持つオブジェクトをJSONにエンコードするとき、その属性は`null`値とともにJSONに含まれますが、値が`undefined`である属性は完全に除外されます。

```ts
JSON.stringify({willStay: null, willBeGone: undefined}); // {"willStay":null}
```

結果として、JSONベースのデータベースは、`null`はサポートしますが`undefined`はサポートしないことがあります。`null`値を持つ属性はエンコードされるため、オブジェクトをエンコードしてリモートのデータストアに送る前に、ある属性値を`null`にすることで、その属性を削除したいという意図を伝えることができます。

属性値を`undefined`にすると、その属性名はエンコードされないため、データの保存と転送のコストを節約することができます。しかし、これによって値を削除することと値が存在しないことの意味づけが複雑になってしまいます。

### 結論
TypeScriptチームは、`null`を使いません: [TypeScriptコーディングガイドライン](https://github.com/Microsoft/TypeScript/wiki/Coding-guidelines#null-and-undefined)。 そして、問題は起きていません。 Douglas Crockfordは[nullはbad idea](https://www.youtube.com/watch?v=PSGEjv3Tqo0&feature=youtu.be&t=9m21s)であり、誰もが`undefined`だけを使うべきだと考えています。

しかし、Nodeスタイルのコードでは、Error引数に`null`が標準で使われています。これは`現在利用できません`という意味です。私は個人的に、ほとんどのプロジェクトにおいて、意見がバラバラのライブラリを使っていますが、`== null`で除外するだけなので、2つを区別しません。
