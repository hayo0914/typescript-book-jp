## NullおよびUndefined
JavaScript（拡張子はTypeScript）には、 `null`と`undefined`という2つのボトムの型があります。彼らは異なる意味を意図しています。

* 何かが初期化されていない： `undefined`。
* 何かが現在利用できません： `null`。


### どちらかを確認する

事実、あなたは両方を扱う必要があります。 `==`チェックだけでどちらかをチェックしてください。

```ts
/// 想像してください: `foo.bar == undefined` でbarはいずれかになり得ます:
console.log(undefined == undefined); // true
console.log(null == undefined); // true

// これらのチェックを行うことにより、偽となる値を心配せずに済みます
console.log(0 == undefined); // false
console.log('' == undefined); // false
console.log(false == undefined); // false
```

`== null`を使って`undefined`と `null`の両方をチェックすることをお勧めします。一般的に2つを区別したくありません。

```ts
function foo(arg: string | null | undefined) {
  if (arg != null) {
    // `!=` がnulllとundefinedを除外しているので、引数argは文字列です
  }
}
```

1つの例外は、global変数(root level)のundefinedの値です。

### global変数(root level)のundefinedのチェック

`== null`を使うべきだと言ったことを思い出してください。もちろん、あなたは覚えているでしょう（私はちょうどそれを言ったので^）。それは、root levelのものには使用しないでください。 strictモードで `foo`を使うとき、`foo`が定義されていないと、 `ReferenceError` **exception**が発生し、呼び出しスタック全体が巻き戻されます。

> strictモードを使うべきです...実際には、TSコンパイラはmoduleを使うとそれを挿入します...より詳細は、あとでこの本で解説するので、詳しく述べる必要はありません:)

したがって、変数が* global *レベルで定義されているかどうかを確認するには、通常は `typeof`を使用します：

```ts
if (typeof someglobal !== 'undefined') {
  // ここではsomeglobalは安全に使えます
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
型アノテーションを使用する必要があります。
```ts
function foo():{a:number,b?:number}{
  // if Something
  return {a:1,b:2};
  // else
  return {a:1};
}
```

### ノードスタイルコールバック
ノードスタイルのコールバック関数（ `（err, somethingElse）=> {/* something */}`）は、エラーがなければ `err`を`null`に設定して呼び出されます。あなたは一般的にerrが真であるかをチェックします：

```ts
fs.readFile('someFile', 'utf8', (err,data) => {
  if (err) {
    // do something
  } else {
    // no error
  }
});
```
独自のAPIを作成するときは、一貫性のために `null`を使用することは問題ありません。誠心誠意、あなたのAPIはpromiseを見るべきです。その場合、エラー値の存在を気にする必要はありません（`.then`と`.catch`を使って扱います）。

### *有効性*を示す手段として `undefined`を使用しないでください

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
TypeScriptチームは、nullを使用しません: [TypeScriptコーディングガイドライン]（https://github.com/Microsoft/TypeScript/wiki/Coding-guidelines#null-and-undefined） そして、問題は発生していません。 Douglas Crockfordは[null is a bad idea]（https://www.youtube.com/watch?v=PSGEjv3Tqo0&feature=youtu.be&t=9m21s） と考えてます。私たちはすべて`undefined`を使うべきです。

しかし、NodeJSスタイルのコードベースでは、Error引数に `null`が標準で使用されています。これは`何かが現在利用できません`ということを示しています。私は個人的には、ほとんどのプロジェクトにおいて、意見の異なるライブラリを使っていますが、 `== null`で除外するだけなので、2つを区別することを気にしません。
