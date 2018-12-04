## 束縛は有害である

これは `lib.d.ts`の`bind`の定義です：

```ts
bind(thisArg: any, ...argArray: any[]): any;
```

あなたが見ることができるように、** any **を返します！つまり、関数の `bind`を呼び出すと、元の関数の署名の型の安全性が完全に失われます。

たとえば、次のようにコンパイルします。

```ts
function twoParams(a:number,b:number) {
    return a + b;
}
let curryOne = twoParams.bind(null,123);
curryOne(456); // Okay but is not type checked!
curryOne('456'); // Allowed because it wasn't type checked!
```

それを書くためのよりよい方法は、明示的な型の注釈を持つ単純な[arrow関数]（../ arrow-functions.md）です。
```ts
function twoParams(a:number,b:number) {
    return a + b;
}
let curryOne = (x:number)=>twoParams(123,x);
curryOne(456); // Okay and type checked!
curryOne('456'); // Error!
```

しかし、あなたがカレー化された機能を望むなら（それにはより良いパターンがあります）（./ currying.md）。

### クラスメンバー
別の一般的な使い方は、クラス関数を渡すときに `this`の正しい値を保証するために`bind`を使うことです。それをしないでください！

次の例は、 `bind`を使うとパラメータ型の安全性を失うという事実を示しています：

```ts
class Adder {
    constructor(public a: string) { }

    add(b: string): string {
        return this.a + b;
    }
}

function useAdd(add: (x: number) => number) {
    return add(456);
}

let adder = new Adder('mary had a little 🐑');
useAdd(adder.add.bind(adder)); // No compile error!
useAdd((x) => adder.add(x)); // Error: number is not assignable to string
```

あなたが**期待している** **クラスメンバー関数を持っているなら、[最初の矢印関数を使う]（../ arrow-functions.md）のように、同じ `Adder`クラスを書くでしょう：

```ts
class Adder {
    constructor(public a: string) { }

    // This function is now safe to pass around
    add = (b: string): string => {
        return this.a + b;
    }
}
```

もう1つの方法は、バインドする変数のタイプを手動で指定することです。

```ts
const add: typeof adder.add = adder.add.bind(adder);
```
