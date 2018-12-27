### 列挙型(Enums)
列挙型は、関連する値の集合を編成する方法です。他の多くのプログラミング言語(C/C#/Java)は`enum`データ型を持っていますが、JavaScriptはありません。しかし、TypeScriptにはあります。TypeScript列挙型の定義例を次に示します。

```ts
enum CardSuit {
	Clubs,
	Diamonds,
	Hearts,
	Spades
}

// Sample usage
var card = CardSuit.Clubs;

// Safety
card = "not a member of card suit"; // Error : string is not assignable to type `CardSuit`
```

これらのenum値は`number`なので、私は数値列挙型(Number Enums)と呼んでいます。

#### 数値列挙数と数値(Number Enums and Numbers)
TypeScript列挙型は数値ベースです。これは、数値を列挙型のインスタンスに割り当てることができることを意味し、`number`と互換性のあるものもそうです。

```ts
enum Color {
    Red,
    Green,
    Blue
}
var col = Color.Red;
col = 0; // Effectively same as Color.Red
```

#### 数値列挙型と文字列(Number Enums and Strings)
列挙型をさらに詳しく調べる前に、生成するJavaScriptを見てみましょう。ここにはサンプルのTypeScriptがあります：

```ts
enum Tristate {
    False,
    True,
    Unknown
}
```
次のJavaScriptを生成します。

```js
var Tristate;
(function (Tristate) {
    Tristate[Tristate["False"] = 0] = "False";
    Tristate[Tristate["True"] = 1] = "True";
    Tristate[Tristate["Unknown"] = 2] = "Unknown";
})(Tristate || (Tristate = {}));
```

`Tristate[Tristate["False"] = 0] = "False";`という行に焦点を当てましょう。`Tristate["False"] = 0`は自己説明的でなければなりません。つまり、`Tristate`変数の`"False"`メンバを`0`に設定します。JavaScriptでは、代入演算子は割り当てられた値(この場合は`0`)を返します。したがって、JavaScriptランタイムによって次に実行されるのは、`Tristate [0] ="False"`です。これは、`Tristate`変数を使用して、列挙型の文字列バージョンを列挙型の数値または数値バージョンに変換することができることを意味します。これは以下のとおりです：

```ts
enum Tristate {
    False,
    True,
    Unknown
}
console.log(Tristate[0]); // "False"
console.log(Tristate["False"]); // 0
console.log(Tristate[Tristate.False]); // "False" because `Tristate.False == 0`
```

#### 数値列挙型に関連付けられた数値を変更する
デフォルトでは列挙型は「0」に基づいており、その後の各値は自動的に1ずつ増加します。例として、次の点を考慮してください。

```ts
enum Color {
    Red,     // 0
    Green,   // 1
    Blue     // 2
}
```

ただし、任意の列挙型メンバーに関連付けられた番号を、それに特に割り当てて変更することはできます。以下の例は3で始まりそこからインクリメントを開始します：

```ts
enum Color {
    DarkRed = 3,  // 3
    DarkGreen,    // 4
    DarkBlue      // 5
}
```

> ヒント：私はいつも最初の列挙型を`= 1`で初期化することによって、列挙型の値を安全にtruthyチェックできるようにします。

#### フラグとしての数値列挙型(Number Enums as flags)
列挙型の優れた使い方は、列挙型をフラグとして使用することです。フラグを使用すると、一連の条件から特定の条件が真であるかどうかを確認できます。動物に関する一連のプロパティがある次の例を考えてみましょう。

```ts
enum AnimalFlags {
    None           = 0,
    HasClaws       = 1 << 0,
    CanFly         = 1 << 1,
    EatsFish       = 1 << 2,
    Endangered     = 1 << 3
}
```

ここでは、左シフト演算子を使用して、特定のビットレベルに1を移動することにより、ビット単位の「0001」、「0010」、「0100」および「1000」になります(これらは10進数の1、2、4、8です。興味があれば)。ビット演算子`|`(or)/`&`(and)/`~`(not)は、ビットフラグを使って作業するときの友達です。

```ts

enum AnimalFlags {
    None           = 0,
    HasClaws       = 1 << 0,
    CanFly         = 1 << 1,
}

function printAnimalAbilities(animal) {
    var animalFlags = animal.flags;
    if (animalFlags & AnimalFlags.HasClaws) {
        console.log('animal has claws');
    }
    if (animalFlags & AnimalFlags.CanFly) {
        console.log('animal can fly');
    }
    if (animalFlags == AnimalFlags.None) {
        console.log('nothing');
    }
}

var animal = { flags: AnimalFlags.None };
printAnimalAbilities(animal); // nothing
animal.flags |= AnimalFlags.HasClaws;
printAnimalAbilities(animal); // animal has claws
animal.flags &= ~AnimalFlags.HasClaws;
printAnimalAbilities(animal); // nothing
animal.flags |= AnimalFlags.HasClaws | AnimalFlags.CanFly;
printAnimalAbilities(animal); // animal has claws, animal can fly
```

ここでやったこと：
* `|=`を使ってフラグを追加する
* `&=`と`~`の組み合わせを使ってフラグをクリアする
* `|`を使ってフラグを組み合わせる

> 注：フラグを組み合わせて、列挙型定義内の便利なショートカットを作成することができます。`EndangeredFlyingClawedFishEating`は以下のようになります：

```ts
enum AnimalFlags {
	None           = 0,
    HasClaws       = 1 << 0,
    CanFly         = 1 << 1,
    EatsFish       = 1 << 2,
    Endangered     = 1 << 3,

    EndangeredFlyingClawedFishEating = HasClaws | CanFly | EatsFish | Endangered,
}
```

#### 文字列列挙型(String Enums)
メンバの値が`number`のenumを見てきました。実際には文字列値を持つ列挙型メンバを持つこともできます。例えば

```ts
export enum EvidenceTypeEnum {
  UNKNOWN = '',
  PASSPORT_VISA = 'passport_visa',
  PASSPORT = 'passport',
  SIGHTED_STUDENT_CARD = 'sighted_tertiary_edu_id',
  SIGHTED_KEYPASS_CARD = 'sighted_keypass_card',
  SIGHTED_PROOF_OF_AGE_CARD = 'sighted_proof_of_age_card',
}
```

これらは意味を持ち/デバッグ可能な文字列値を提供するので、デバッグしやすくなります。

これらの値を使用して簡単な文字列の比較を行うことができます。例えば

```ts
// Where `someStringFromBackend` will be '' | 'passport_visa' | 'passport' ... etc.
const value = someStringFromBackend as EvidenceTypeEnum; 

// Sample use in code
if (value === EvidenceTypeEnum.PASSPORT){
    console.log('You provided a passport');
    console.log(value); // `passport`
}
```

#### 定数列挙型(Const Enums)

次のような列挙型定義がある場合：

```ts
enum Tristate {
    False,
    True,
    Unknown
}

var lie = Tristate.False;
```

`var lie = Tristate.False`という行はJavaScriptの`var lie = Tristate.False`にコンパイルされます(出力は入力と同じです)。つまり、実行時にランタイムは `Tristate`と`Tristate.False`を検索する必要があります。ここでパフォーマンスを向上させるには、`enum`を`const enum`としてマークできます。これは以下のとおりです：

```ts
const enum Tristate {
    False,
    True,
    Unknown
}

var lie = Tristate.False;
```

JavaScriptを生成する：

```js
var lie = 0;
```

コンパイラが行うこと：

1. 列挙型のあらゆる用途をインライン化する(`Tristate.False`ではなく`0`)
1. enum定義用のJavaScriptを生成しない(実行時に`Tristate`変数はありません)。使用箇所はインライン展開される

##### 定数列挙型に対する`--preserveConstEnums`(Const enum preserveConstEnums)
インライン化には明らかなパフォーマンス上の利点があります。実行時に`Tristate`変数がないという事実は、実行時に実際には使用されないJavaScriptを生成しないことによって、コンパイラを助けることです。しかし、それでも先程のように数値型と文字列型を相互に検索できる列挙型を生成したい場合があるかもしれません。この場合、コンパイラフラグ`--preserveConstEnums`を使用することができます。また`var Tristate`定義を生成するので、実行時に`Tristate [" False "]`や `Tristate [0]`をランタイムで手動で使用することができます。これはインライン展開には決して影響しません。

### 静的関数を持つ列挙型(Enum with static functions)
宣言`enum`と`namespace`を合体させて、静的メソッドを列挙型に追加することができます。以下は、静的メンバー`isBusinessDay`を列挙型`Weekday`に追加する例を示しています：

```ts
enum Weekday {
	Monday,
	Tuesday,
	Wednesday,
	Thursday,
	Friday,
	Saturday,
	Sunday
}
namespace Weekday {
	export function isBusinessDay(day: Weekday) {
		switch (day) {
			case Weekday.Saturday:
			case Weekday.Sunday:
				return false;
			default:
				return true;
		}
	}
}

const mon = Weekday.Monday;
const sun = Weekday.Sunday;
console.log(Weekday.isBusinessDay(mon)); // true
console.log(Weekday.isBusinessDay(sun)); // false
```

#### 列挙型はオープンエンド

> 注：オープンエンドの列挙型は、モジュールを使用していない場合にのみ関係します。モジュールを使用するべきです。したがって、このセクションで触れるだけに留めます。

ここに再び表示される列挙型のJavaScriptが生成されます：

```js
var Tristate;
(function (Tristate) {
    Tristate[Tristate["False"] = 0] = "False";
    Tristate[Tristate["True"] = 1] = "True";
    Tristate[Tristate["Unknown"] = 2] = "Unknown";
})(Tristate || (Tristate = {}));
```

`Tristate[Tristate["False"] = 0] = "False";`部分については、すでに説明しました。今は、`(function (Tristate) { /*code here */ })(Tristate || (Tristate = {}));`部分を見ましょう。特に`(Tristate || (Tristate = {}));`。これは、基本的に既に捕捉されたローカル変数`Tristate`を指し示すか、新しい空のオブジェクト`{}`で初期化するローカル変数`TriState`を取得します。

つまり、列挙型定義を複数のファイルに分割(および拡張)することができます。たとえば、以下の例では、`Color`の定義を2つのブロックに分割しています

```ts
enum Color {
    Red,
    Green,
    Blue
}

enum Color {
    DarkRed = 3,
    DarkGreen,
    DarkBlue
}
```

注意しなければならないのは、前の定義(つまり、`0`、`1`、...)を除外するために、列挙の最初のメンバ(ここでは`DarkRed = 3`)を再初期化しないといけないことです。それを行わない場合は、TypeScriptは警告します(エラーメッセージ:`In an enum with multiple declarations, only one declaration can omit an initializer for its first enum element`)。
