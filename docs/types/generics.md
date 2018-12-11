## ジェネリック(Generics)

ジェネリックの役立つ主な理由は、メンバ間で意味のある型制約を提供することです。メンバには以下のものがあります：

* クラスのインスタンスメンバ
* クラスメソッド
* 関数の引数
* 関数の戻り値

## ジェネリックのモチベーションとサンプル

単純な`Queue`(先入れ先出し)データ構造の実装を考えてみましょう。TypeScript/JavaScriptの単純なものは以下のようになります：

```ts
class Queue {
  private data = [];
  push = (item) => this.data.push(item);
  pop = () => this.data.shift();
}
```

この実装での1つの問題は、キューに何でも追加できることです。また、キューから要素を取り出すと、何が出てくるかわかりません。これを以下に示します。ここでは誰かが`string`をキューにプッシュしていますが、実際には`numbers`だけがプッシュされることを想定しています。

```ts
class Queue {
  private data = [];
  push = (item) => this.data.push(item);
  pop = () => this.data.shift();
}

const queue = new Queue();
queue.push(0);
queue.push("1"); // Oops a mistake

// a developer walks into a bar
console.log(queue.pop().toPrecision(1));
console.log(queue.pop().toPrecision(1)); // RUNTIME ERROR
```

1つの解決策(実際にはジェネリックをサポートしていない言語での唯一の解決策)は、これらの制約のために特別なクラスを作成することです。例えば素早くダーティに数値型のキューを作ります：

```ts
class QueueNumber {
  private data = [];
  push = (item: number) => this.data.push(item);
  pop = (): number => this.data.shift();
}

const queue = new QueueNumber();
queue.push(0);
queue.push("1"); // ERROR : cannot push a string. Only numbers allowed

// ^ if that error is fixed the rest would be fine too
```

もちろん、これはすぐに苦痛になる可能性があります。文字列キューが必要な場合は、そのすべての作業をもう一度行う必要があります。あなたが本当に必要とすることは、型が何であれ、プッシュされているもの型とポップされたものの型は同じでなければならないということです。これは、ジェネリックパラメータ(この場合はクラスレベル)で簡単に行えます：

```ts
/** A class definition with a generic parameter */
class Queue<T> {
  private data = [];
  push = (item: T) => this.data.push(item);
  pop = (): T => this.data.shift();
}

/** Again sample usage */
const queue = new Queue<number>();
queue.push(0);
queue.push("1"); // ERROR : cannot push a string. Only numbers allowed

// ^ if that error is fixed the rest would be fine too
```

すでに見たもう一つの例は、*reverse*関数の例です。ここでは、関数に渡されるものと関数が返すものの間の制約があります。

```ts
function reverse<T>(items: T[]): T[] {
    var toreturn = [];
    for (let i = items.length - 1; i >= 0; i--) {
        toreturn.push(items[i]);
    }
    return toreturn;
}

var sample = [1, 2, 3];
var reversed = reverse(sample);
console.log(reversed); // 3,2,1

// Safety!
reversed[0] = '1';     // Error!
reversed = ['1', '2']; // Error!

reversed[0] = 1;       // Okay
reversed = [1, 2];     // Okay
```

このセクションでは、クラスレベルと関数レベルで定義されているジェネリックの例を見てきました。多少付け加えたいことは、メンバ関数のためだけにジェネリックを作成できるということです。おもちゃの例として、`reverse`関数を`Utility`クラスに移したところで、次のことを考えてみましょう：

```ts
class Utility {
  reverse<T>(items: T[]): T[] {
      var toreturn = [];
      for (let i = items.length - 1; i >= 0; i--) {
          toreturn.push(items[i]);
      }
      return toreturn;
  }
}
```

> ヒント：必要に応じてジェネリックパラメータを呼び出すことができます。単純なジェネリックを使うときは `T`、`U`、`V`を使うのが普通です。複数のジェネリック引数がある場合は、意味のある名前を使用してください。例えば`TKey`と`TValue`です(一般に`T`を接頭辞として使用する規約は、他の言語(例えばC++)ではテンプレートと呼ばれることもあります)。

## 役に立たずのジェネリック

私は人々が興味本位でジェネリックを使用しているのを見ました。考えるべき質問は、何を表現しようとしているのか？です。あなたが簡単にそれに答えることができない場合は、役に立たないジェネリックかもしれません。例えば次の関数です:

```ts
declare function foo<T>(arg: T): void;
```
ここでは、ジェネリック`T`は、一箇所の引数の位置でのみ使用されるので完全に不要です。これは次のコードと同じです:

```ts
declare function foo(arg: any): void;
```

### デザインパターン：便利なジェネリック

次の関数を考えてみましょう。

```ts
declare function parse<T>(name: string): T;
```

この場合、タイプ`T`は1つの場所でのみ使用されていることがわかります。したがって、メンバー間に制約はありません。これは、型安全性における型アサーションに相当します。

```ts
declare function parse(name: string): any;

const something = parse('something') as TypeOfSomething;
```

一回だけ使用されるジェネリックは、型安全性に関してはアサーションよりも劣っています。それは、既に述べたように、あなたのAPIに利便性を提供するものです。

より明らかな例は、jsonレスポンスをロードする関数です。それは、あなたが渡した任意の型のPromiseを返します：
```ts
const getJSON = <T>(config: {
    url: string,
    headers?: { [key: string]: string },
  }): Promise<T> => {
    const fetchConfig = ({
      method: 'GET',
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      ...(config.headers || {})
    });
    return fetch(config.url, fetchConfig)
      .then<T>(response => response.json());
  }
```

あなたは依然としてアノテーションを明示しなければならないことに注意してください。しかし、`getJSON<T>`のシグネチャ`(config)=> Promise <T>`は、キータイプを減らすことができます(`loadUsers`の戻り値の型は、TypeScriptが推論可能なのでアノテーションする必要はありません):

```ts
type LoadUsersResponse = {
  users: {
    name: string;
    email: string;
  }[];  // array of user objects
}
function loadUsers() {
  return getJSON<LoadUsersResponse>({ url: 'https://example.com/users' });
}
```

戻り値としての`Promise<T>`は、`Promise<any>`よりも断然優れています。
