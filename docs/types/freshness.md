## Freshness

TypeScriptは**Freshness**(厳密なオブジェクトリテラルチェックとも呼ばれます)という概念を提供します。それはオブジェクトリテラルや構造的にご完成がある型の型チェックを簡単にします。

構造型は非常に便利です。次のコードを考えてみましょう。これにより、型安全性のレベルを維持しながら、JavaScriptをTypeScriptに非常に便利にアップグレードすることができます：

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

しかし、構造型の入力は、実際よりも、余計なものを含むデータを受け入れると誤解してしまうという弱点があります。これは、次のコードで示されています。これは、TypeScriptが次のようにエラーになります。

```ts
function logName(something: { name: string }) {
    console.log(something.name);
}

logName({ name: 'matt' }); // okay
logName({ name: 'matt', job: 'being awesome' }); // Error: object literals must only specify known properties. `job` is excessive here.
```

このエラーはオブジェクトリテラルでのみ発生することに注意してください。このエラーがなければ、`logName({name： 'matt'、job： 'awesome'})`という呼び出しを見て、logNameが`job`を渡すと何かを便利なことを実行すると思うかもしれません。現実的には完全に無視されます。

もう1つの大きなユースケースは、オプションのメンバを持つインターフェイスで、このようなオブジェクトのリテラルチェックなしでは、型チェックはタイプミスを見逃します。これは以下のとおりです：

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

このようにしてオブジェクトリテラルを型チェックする理由は、実際には使用されないプロパティは、ほとんどの場合、タイプミスまたは誤解によるものだからです。

### 追加のプロパティを許可する

型には、過剰なプロパティが許可されていることを明示的に示すインデックスシグネチャを含めることができます。

```ts
var x: { foo: number, [x: string]: any };
x = { foo: 1, baz: 2 };  // Ok, `baz` matched by index signature
```

### ユースケース： Reactの状態

[Facebook ReactJS](https://facebook.github.io/react/) は、オブジェクトのFreshnessの良いユースケースを提供します。コンポーネント内では、通常、すべてのプロパティを渡すのではなく、少数のプロパティだけを使って`setState`を呼び出します。

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

Freshnessの概念を使用する場合は、すべてのメンバーをオプションとマークすれば、あなたはまだタイプミスに気づくことができます!：

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
