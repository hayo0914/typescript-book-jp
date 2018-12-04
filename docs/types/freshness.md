
* [鮮度]（新鮮度）
* [追加のプロパティを許可する]（#allow-extra-properties）
* [ユースケース：反応]（#ユースケース反応状態）

## フレッシュネス

TypeScriptは、構造的に型互換性のあるオブジェクトリテラルのチェックを簡単に入力できるように、** Freshness **（*厳密なオブジェクトリテラルチェック*とも呼ばれます）のコンセプトを提供します。

構造タイピングは非常に便利です*。次のコードを考えてみましょう。これにより、タイプセーフティのレベルを維持しながら、JavaScriptをTypeScriptに非常に便利に*アップグレードすることができます：

```ts
function logName(something: { name: string }) {
    console.log(something.name);
}

var person = { name: 'matt', job: 'being awesome' };
var animal = { name: 'cow', diet: 'vegan, but has milk of own species' };
var random = { note: `I don't have a name property` };

logName(person); // okay
logName(animal); // okay
logName(random); // Error: property `name` is missing
```

しかし、*構造型の入力は、実際に比べて何かがより多くのデータを受け入れると誤解して考えることができるという弱点があります。これは、次のコードで示されています。これは、TypeScriptが次のようにエラーになります。

```ts
function logName(something: { name: string }) {
    console.log(something.name);
}

logName({ name: 'matt' }); // okay
logName({ name: 'matt', job: 'being awesome' }); // Error: object literals must only specify known properties. `job` is excessive here.
```

このエラー*はオブジェクトリテラル*でのみ発生することに注意してください。このエラーがなければ、 `logName（{name： 'matt'、job： 'awesome'}）`という呼び出しを見て、* logName *が `job`で有用な何かを実行すると思うかもしれません。それ。

もう1つの大きなユースケースは、オプションのメンバを持つインターフェイスで、このようなオブジェクトのリテラルチェックなしでは、タイプミスはちょうど良いとタイプされます。これは以下のとおりです：

```ts
function logIfHasName(something: { name?: string }) {
    if (something.name) {
        console.log(something.name);
    }
}
var person = { name: 'matt', job: 'being awesome' };
var animal = { name: 'cow', diet: 'vegan, but has milk of own species' };

logIfHasName(person); // okay
logIfHasName(animal); // okay
logIfHasName({neme: 'I just misspelled name to neme'}); // Error: object literals must only specify known properties. `neme` is excessive here.
```

このようにしてオブジェクトリテラルだけを型チェックする理由は、実際には使用されない追加のプロパティ*は、ほとんどの場合、APIのタイプミスまたは誤解のためです。

### 追加のプロパティを許可する

型には、過剰なプロパティが許可されていることを明示的に示すインデックスシグネチャを含めることができます。

```ts
var x: { foo: number, [x: string]: any };
x = { foo: 1, baz: 2 };  // Ok, `baz` matched by index signature
```

### ユースケース：反応状態

[Facebook ReactJS]（https://facebook.github.io/react/）は、オブジェクトの新鮮さの良いユースケースを提供します。コンポーネント内では、通常、すべてのプロパティを渡すのではなく、少数のプロパティだけを使って `setState`を呼び出します。

```ts
// Assuming
interface State {
  foo: string;
  bar: string;
}

// You want to do: 
this.setState({foo: "Hello"}); // Error: missing property bar

// But because state contains both `foo` and `bar` TypeScript would force you to do: 
this.setState({foo: "Hello", bar: this.state.bar}};
```

フレッシュさのアイデアを使用すると、すべてのメンバーをオプションとマークします*あなたはまだタイプミスをキャッチする*！：

```ts
// Assuming
interface State {
  foo?: string;
  bar?: string;
}

// You want to do: 
this.setState({foo: "Hello"}); // Yay works fine!

// Because of freshness it's protected against typos as well!
this.setState({foos: "Hello"}}; // Error: Objects may only specify known properties

// And still type checked
this.setState({foo: 123}}; // Error: Cannot assign number to a string
```
