* [Enums]（#enums）
* [Number Enums and numbers]（#number-enums-and-numbers）
* [Number Enums and strings]（#number-enums-and-strings）
* [数値列挙型に関連付けられた番号の変更]（#番号付き列挙型変更）
* [Enums are open ended]（#enums-are-open-ended）
* [Number Enums as flags]（#number enums-as-flags）
* [String Enums]（#string-enums）
* [Const enums]（#const-enums）
* [静的関数を持つ列挙型]（#列挙型静的関数）

### Enums
列挙型は、関連する値の集合を編成する方法です。他の多くのプログラミング言語（C / C#/ Java）は `enum`データ型を持っていますが、JavaScriptはありません。しかし、TypeScriptはそうです。 TypeScript列挙型の定義例を次に示します。

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

これらのenum値は `number`sなので、私はNumber Enumsと呼んでいます。

#### 列挙数と数値
TypeScript列挙型は数値ベースです。これは、数値を列挙型のインスタンスに割り当てることができることを意味し、 `number`と互換性のあるものもそうです。

```ts
enum Color {
    Red,
    Green,
    Blue
}
var col = Color.Red;
col = 0; // Effectively same as Color.Red
```

#### 数値列挙と文字列
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

`Tristate [Talseate [" False "] = 0] =" False ";という行に焦点を当てましょう。 `Tristate [" False "] = 0`は自己説明的でなければなりません。つまり、`Tristate`変数の ``False``メンバを ``0 ''に設定します。 JavaScriptでは、代入演算子は割り当てられた値（この場合は `0`）を返します。したがって、JavaScriptランタイムによって次に実行されるのは、 `Tristate [0] =" False "`です。これは、 `Tristate`変数を使用して、列挙型の文字列バージョンを列挙型の数値または数値バージョンに変換することができることを意味します。これは以下のとおりです：

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

#### Number Enumに関連付けられた番号を変更する
デフォルトでは列挙型は「0」に基づいており、その後の各値は自動的に1ずつ増加します。例として、次の点を考慮してください。

```ts
enum Color {
    Red,     // 0
    Green,   // 1
    Blue     // 2
}
```

ただし、任意の列挙型メンバーに関連付けられた番号を、それに特に割り当てて変更することはできます。これは、3で始まりそこからインクリメントを開始するところで以下に説明されています：

```ts
enum Color {
    DarkRed = 3,  // 3
    DarkGreen,    // 4
    DarkBlue      // 5
}
```

> ヒント：最初の列挙型を `= 1`で初期化するのは、列挙型の値を安全に真理チェックするためです。

#### フラグとしての数値列挙型
列挙型の優れた使い方は、列挙型を `Flags`として使用することです。フラグを使用すると、一連の条件から特定の条件が真であるかどうかを確認できます。動物に関する一連のプロパティがある次の例を考えてみましょう。

```ts
enum AnimalFlags {
    None           = 0,
    HasClaws       = 1 << 0,
    CanFly         = 1 << 1,
    EatsFish       = 1 << 2,
    Endangered     = 1 << 3
}
```

ここでは、左シフト演算子を使用して、特定のビットレベルの周りに「1」を移動して、ビット単位の「0001」、「0010」、「0100」および「1000」（これらは小数点「1」、好奇心が強い場合は2、4、8）。ビット演算子 `|`（または）/ `＆`（と）/ `〜`（そうでない）は、フラグを使って作業するときの親友です。

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

ここに：
* `| =`を使ってフラグを追加しました
* フラグをクリアするための `＆=`と `〜`の組み合わせ
* フラグを結合する ``| `

> 注：フラグを組み合わせて、列挙型定義内の便利なショートカットを作成することができます。 `EndangeredFlyingClawedFishEating`以下のようになります：

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

#### 文字列列挙型
メンバーの値が `number`のenumを見てきました。実際には文字列値を持つ列挙型メンバを持つこともできます。例えば

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

これらは、有意義な/デバッグ可能な文字列値を提供するので、対処しやすく、デバッグすることができます。

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

#### Const Enums

次のような列挙型定義がある場合：

```ts
enum Tristate {
    False,
    True,
    Unknown
}

var lie = Tristate.False;
```

`var lie = Tristate.False`という行はJavaScriptの`var lie = Tristate.False`にコンパイルされます（出力は入力と同じです）。つまり、実行時にランタイムは `Tristate`と`Tristate.False`をルックアップする必要があります。ここでパフォーマンスを向上させるには、 `enum`を`const enum`としてマークできます。これは以下のとおりです：

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

コンパイラ：
1. * Inlines *列挙型のあらゆる用途（ 'Tristate.False`ではなく' 0`）。
1. enum定義用のJavaScriptを生成しません（実行時に `Tristate`変数はありません）。その用途はインライン展開されています。

##### Const enum preserveConstEnums
インライン化には明らかなパフォーマンス上の利点があります。実行時に `Tristate`変数がないという事実は、実行時に実際には使用されないJavaScriptを生成しないことによって、コンパイラを助けることです。しかし、コンパイラが* number to string *や* string to number *ルックアップのようなものの列挙型定義のJavaScriptバージョンを引き続き生成することをお勧めします。この場合、コンパイラフラグ `--preserveConstEnums`を使用することができます。また`var Tristate`定義を生成するので、実行時に `Tristate [" False "]`や `Tristate [0]`を手動で使用することができます欲しいです。これは決してインライン展開*には影響しません。

### 静的関数を持つ列挙型
宣言 `enum`+` namespace`マージを使用して、静的メソッドを列挙型に追加することができます。以下は、静的メンバー `isBusinessDay`を列挙型`Weekday`に追加する例を示しています：

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

#### 列挙は開いたままです

> 注：開いている列挙型は、モジュールを使用していない場合にのみ関係します。モジュールを使用する必要があります。したがって、このセクションは最後です。

ここに再び表示される列挙型のJavaScriptが生成されます：

```js
var Tristate;
(function (Tristate) {
    Tristate[Tristate["False"] = 0] = "False";
    Tristate[Tristate["True"] = 1] = "True";
    Tristate[Tristate["Unknown"] = 2] = "Unknown";
})(Tristate || (Tristate = {}));
```

`Tristate [Talseate [" False "] = 0] =" False ";部分についてすでに説明しました。 Tristate ||（Tristate = {}））; `具体的に`（Tristate ||（Tristate = {}））; `部分。これは、基本的に既に定義された `Tristate`値を指し示すか、新しい空の`{} `オブジェクトで初期化するローカル変数`TriState`を取得します。

つまり、列挙型定義を複数のファイルに分割（および拡張）することができます。たとえば、以下の例では、 `Color`の定義を2つのブロックに分割しています

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

注意しなければならないのは、生成されたコードを以前の定義（つまり、 `0`、`1`、...）から取り除くために、列挙の継続中の最初のメンバ（ここでは `DarkRed = 3`）を再初期化すべきです。値についても同様）。とにかくしないと、TypeScriptは警告します（エラーメッセージ `複数の宣言を含む列挙型では、1つの宣言だけが最初の列挙型要素の初期化子を省略できます）。
