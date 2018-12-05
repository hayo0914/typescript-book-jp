## JavaScriptからの移行

仮定：
* あなたはJavaScriptを知っています。
* プロジェクトで使用されているパターンや構築ツール(webpackなど)を知っている。

そのような前提を外して、一般に、プロセスは以下のステップからなる：

* `tsconfig.json`を追加します。
* ソースコードの拡張子を `.js`から`.ts`に変更してください。 *を使用してエラーを抑制*する。
* TypeScriptに新しいコードを記述し、できるだけ `any`をほとんど使わないようにしてください。
* 古いコードに戻り、型の注釈を追加し、識別されたバグを修正してください。
* サードパーティ製JavaScriptコードの環境定義を使用します。

これらの点のいくつかをさらに議論しましょう。

すべてのJavaScriptは*有効* TypeScriptであることに注意してください。つまり、TypeScriptコンパイラにJavaScriptをいくつか与えると、TypeScriptコンパイラによって生成されたJavaScriptは元のJavaScriptとまったく同じように動作します。つまり、拡張子を `.js`から`.ts`に変更しても、コードベースに悪影響はありません。

### エラーを抑制する
TypeScriptはすぐにTypeCheckingを開始し、元のJavaScriptコード*はあなたが思っていたほどきちんとしていない可能性があります。したがって、診断エラーが発生します。これらのエラーの多くは、「任意」を使用して抑制することができます。例：

```ts
var foo = 123;
var bar = 'hey';

bar = foo; // ERROR: cannot assign a number to a string
```

** エラーは有効です**(ほとんどの場合、推測される情報はコードベースの異なる部分の元の著者よりも優れています)、あなたの焦点はおそらくTypeScriptで新しいコードを書くことになります。古いコードベース。ここでは、以下のような型アサーションでこのエラーを抑制することができます：

```ts
var foo = 123;
var bar = 'hey';

bar = foo as any; // Okay!
```

他の場所では、何かに `any`と注釈を付けることができます。

```ts
function foo() {
    return 1;
}
var bar = 'hey';
bar = foo(); // ERROR: cannot assign a number to a string
```

抑制された：

```ts
function foo(): any { // Added `any`
    return 1;
}
var bar = 'hey';
bar = foo(); // Okay!
```

> 注意：エラーを抑止することは危険ですが、* new * TypeScriptコードでエラーを通知することができます。あなたは `/ TODO：`コメントを残しておきたいかもしれません。**

### 第三者のJavaScript
JavaScriptをTypeScriptに変更することはできますが、世界全体を変更してTypeScriptを使用することはできません。これは、TypeScriptの環境定義サポートがどこに来るかです。最初は `vendor.d.ts`(`.d.ts`拡張子が*これは*宣言ファイル*を指定しています)を作成し、ダーティそれに詰め込む。あるいは、ライブラリに固有のファイルを作成します。 jqueryの `jquery.d.ts`です。

> 注意：[DefinitelyTyped](https://github.com/borisyankov/DefinitelyTyped)と呼ばれるOSSリポジトリには、上位90％のJavaScriptライブラリのほぼ整った厳密な型定義が存在します。ここにあるように独自の定義を作成する前に、そこを見ることをお勧めします。それにもかかわらず、この素早く汚れた方法は、初期の摩擦をTypeScript **で減らすために不可欠な知識です。

`jquery`の場合を考えてください。あなたはそれを簡単に*簡単に定義することができます：

```ts
declare var $: any;
```

場合によっては、明示的な注釈を何か(例えば `JQuery`)に追加したいかもしれないし、*型宣言スペース*に何かが必要な場合もあります。 `type`キーワードを使って簡単に行うことができます：

```ts
declare type JQuery = any;
declare var $: JQuery;
```

これにより、将来の更新パスが簡単になります。

ここでも、[DefinitelyTyped](https://github.com/borisyankov/DefinitelyTyped)に高品質の「jquery.d.ts」が存在します。しかし、サードパーティ製のJavaScriptを使用している場合、JavaScript  - > TypeScriptのフリクション*をすばやく克服する方法を知っています。次に、環境宣言について詳しく説明します。


# 第三者NPMモジュール

グローバル変数宣言と同様に、グローバルモジュールを簡単に宣言できます。例えば。 `jquery`をモジュール(https://www.npmjs.com/package/jquery)として使用したい場合は、あなた自身で以下のように書くことができます：

```ts
declare module "jquery";
```

必要に応じてファイルにインポートすることができます：

```ts
import * as $ from "jquery";
```

> さらに、より高品質のjqueryモジュール宣言を提供する[DefinitelyTyped](https://github.com/borisyankov/DefinitelyTyped)に高品質の `jquery.d.ts`が存在します。しかし、あなたのライブラリには存在しないかもしれないので、今やあなたは移行を継続するための素早い低摩擦の方法を持っています🌹

# 外部の非jsリソース

たとえば、ファイルのインポートを許可することもできます。簡単な `*`スタイル宣言(理想的には ``globals.d.ts`ファイル(../ project / globals.md)の中にある `.css`ファイル(webpackスタイルのローダーやCSSモジュールのようなものを使用している場合) )))：

```ts
declare module "*.css";
```

今では `foo from as"をインポートすることができます./some/file.css ";`

同様に、htmlテンプレート(角度など)を使用している場合は、次の操作を実行できます。

```ts
declare module "*.html";
```
