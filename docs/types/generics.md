## ジェネリックス

ジェネリックの主な動機は、メンバー間で意味のある型制約を提供することです。メンバーには以下のものがあります：

* クラスインスタンスメンバ
* クラスメソッド
* 関数の引数
* 関数の戻り値

## 動機づけとサンプル

単純な `Queue`（先入れ先出し）データ構造の実装を考えてみましょう。 TypeScript / JavaScriptの単純なものは以下のようになります：

```ts
class Queue {
  private data = [];
  push = (item) => this.data.push(item);
  pop = () => this.data.shift();
}
```

この実装での1つの問題は、キューに*何かを追加できるようにすることです。キューをポップすると、*何でも*できます。これは以下に示されています。ここでは、 `string`をキューにプッシュすることができますが、実際に`numbers`だけがプッシュされていると仮定しています。

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

1つの解決策（実際にはジェネリックをサポートしていない言語の唯一の解決策）は、これらの制約のために*特別なクラスを作成することです。例えば。クイックで汚れた番号のキュー：

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

もちろん、これは急速に痛みを伴う可能性があります。文字列キューが必要な場合は、そのすべての作業をやり直す必要があります。あなたが本当に欲しいのは、タイプが*プッシュ*されているもののタイプが何であれ、*ポップされたものは何でも同じでなければならないと言う方法です。これは、*ジェネリック*パラメータ（この場合はクラスレベル）で簡単に行えます：

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

すでに見たもう一つの例は、* reverse *関数の例です。ここでは、関数に渡されるものと関数が返すものの間の制約があります。

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

このセクションでは、クラスレベル*と*関数レベル*で定義されているジェネリックの例を見てきました。言及する価値のあるマイナーな追加点は、メンバ関数のためだけにジェネリックを作成できるということです。おもちゃの例として、 `reverse`関数を`Utility`クラスに移したところで、次のことを考えてみましょう：

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

> ヒント：必要に応じてジェネリックパラメータを呼び出すことができます。単純なジェネリックスを持つときは `T`、`U`、 `V`を使うのが普通です。複数の汎用引数がある場合は、意味のある名前を使用してください。 `TKey`と`TValue`（一般に `T`を接頭辞として使用することは、他の言語、例えばC ++の*テンプレート*とも呼ばれます）です。

## 役に立たずのジェネリック

私は人々がジェネリック薬をちょうど使用しているのを見ました。尋ねる質問は、あなたが何を記述しようとしているのか*です。あなたが簡単にそれに答えることができない場合は、役に立たないジェネリックを持つかもしれません。例えば。次の関数

```ts
declare function foo<T>(arg: T): void;
```
ここでは、一般的な `T`は、* single *引数の位置でのみ使用されるので完全に無用です。次のようなこともあります。

```ts
declare function foo(arg: any): void;
```

### デザインパターン：便利な汎用

次の関数を考えてみましょう。

```ts
declare function parse<T>(name: string): T;
```

この場合、タイプ「T」は1つの場所でのみ使用されていることがわかります。したがって、メンバー間に制約はありません。これは、型の安全性に関する型宣言に相当します。

```ts
declare function parse(name: string): any;

const something = parse('something') as TypeOfSomething;
```

* 使用されているジェネリックは、型の安全性に関してアサーションよりも優れていません。それはあなたのAPIに*便利*を提供していると言いました。

より明白な例は、jsonレスポンスをロードする関数です。それは*あなたが渡したどんな型でも*の約束を返します：
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

`getJSON <T>`シグネチャ `（config）=> Promise <T>`は、いくつかのキーストロークを保存します（戻り値の型を注釈する必要はありません）。推測できるように `loadUsers`）：

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

戻り値として `Promise <T>`も `Promise <any>`のような選択肢よりも優れています。
