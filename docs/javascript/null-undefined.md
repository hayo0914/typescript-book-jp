## NullおよびUndefined
JavaScript（拡張子はTypeScript）には、 `null`と`undefined`という2つのボトムタイプがあります。彼らは異なることを意味することを意図しています*

* 何かが初期化されていない： `undefined`。
* 何か現在利用できません： `null`。


### どちらかを確認する

事実、あなたは両方を扱う必要があります。 `==`チェックだけでどちらかをチェックしてください。

```ts
/// Imagine you are doing `foo.bar == undefined` where bar can be one of:
console.log(undefined == undefined); // true
console.log(null == undefined); // true

// You don't have to worry about falsy values making through this check
console.log(0 == undefined); // false
console.log('' == undefined); // false
console.log(false == undefined); // false
```
`== null`を使って`undefined`と `null`の両方をチェックすることをお勧めします。あなたは一般的に2つを区別したくありません。

```ts
function foo(arg: string | null | undefined) {
  if (arg != null) {
    // arg must be a string as `!=` rules out both null and undefined. 
  }
}
```

1つの例外は、ルートレベル未定義の値です。

### 未定義のルートレベルのチェック

`== null`を使うべきだと言ったことを思い出してください。もちろん、あなたは（私はちょうどそれを言ったので^）。ルートレベルのものには使用しないでください。 strictモードで `foo`を使うと`foo`が定義されていないと、 `ReferenceError` **例外**が発生し、呼び出しスタック全体が巻き戻されます。

> 厳密なモードを使うべきです...実際には、TSコンパイラはモジュールを使うとそれを挿入します...もっと後のものについては、もっと詳しく述べる必要はありません:)

したがって、変数が* global *レベルで定義されているかどうかを確認するには、通常は `typeof`を使用します：

```ts
if (typeof someglobal !== 'undefined') {
  // someglobal is now safe to use
  console.log(someglobal);
}
```

### 明示的に `undefined`を使うことを制限する
TypeScriptは以下のようなものではなく、値とは別にあなたの構造体を文書化する機会を与えるからです：
```ts
function foo(){
  // if Something
  return {a:1,b:2};
  // else
  return {a:1,b:undefined};
}
```
型の注釈を使用する必要があります。
```ts
function foo():{a:number,b?:number}{
  // if Something
  return {a:1,b:2};
  // else
  return {a:1};
}
```

### ノードスタイルコールバック
ノードスタイルのコールバック関数（ `（err、somethingElse）=> {/ *何か* /}`）は、エラーがなければ `err`を`null`に設定して呼び出されます。あなたは一般的にちょうどこれのために本当にチェックを使用します：

```ts
fs.readFile('someFile', 'utf8', (err,data) => {
  if (err) {
    // do something
  } else {
    // no error
  }
});
```
独自のAPIを作成するときは、一貫性のために `null`を使用してください。あなた自身のAPIの全ての誠実さにおいて、約束を見てください。その場合、実際にはエラー値（ `.then`と`.catch`を使って扱います）を気にする必要はありません。

### *有効性を示す手段として `undefined`を使用しないでください*

たとえば、次のようなひどい関数です。

```ts
function toInt(str:string) {
  return str ? parseInt(str) : undefined;
}
```
次のように書くのがはるかに優れています：
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


### 最終的な考え
TypeScriptチームは、[TypeScriptコーディングガイドライン]（https://github.com/Microsoft/TypeScript/wiki/Coding-guidelines#null-and-undefined）を使用せず、問題は発生していません。 Douglas Crockfordは[`null`は悪い考えだと思う]（https://www.youtube.com/watch?v=PSGEjv3Tqo0&feature=youtu.be&t=9m21s）、私たちはすべて`undefined`を使うべきです。

しかし、NodeJSスタイルのコードベースでは、Error引数に `null`が標準で使用されています。これは`何か現在利用できません 'を示しています。私は個人的には、ほとんどのプロジェクトが意見の異なるライブラリを使い、 `== null`で除外するだけなので、2つを区別するのに気にしません。
