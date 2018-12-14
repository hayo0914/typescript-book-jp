## バインドは有害である

これは`lib.d.ts`の`bind`の定義です：

```ts
bind(thisArg: any, ...argArray: any[]): any;
```

見ての通り、**any**を返します!つまり、関数の`bind`を呼び出すと、元の関数のシグネチャの型安全性が完全に失われます。

たとえば、次のようにコンパイルします:

```ts
function twoParams(a:number,b:number) {
    return a + b;
}
let curryOne = twoParams.bind(null,123);
curryOne(456); // Okay but is not type checked!
curryOne('456'); // Allowed because it wasn't type checked!
```

それを書くためのよりよい方法は、明示的な型アノテーションを持つ単純な[アロー関数](../arrow-functions.md)です。
```ts
function twoParams(a:number,b:number) {
    return a + b;
}
let curryOne = (x:number)=>twoParams(123,x);
curryOne(456); // Okay and type checked!
curryOne('456'); // Error!
```

しかし、あなたがカリー化された関数を必要とする場合は、[それにはより良いパターンがあります](./currying.md)。

### クラスメンバー
`bind`の別の一般的な使い方は、クラス関数を渡すときに`this`の正しい値を保証するために`bind`を使うことです。それはやらないでください!

次の例は、`bind`を使うとパラメータの型安全性を失うことを示しています：

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

もしあなたが他に渡すことを期待しているクラスメンバ関数を持つ場合は、そもそも[アロー関数](../arrow-functions.md)を使います。例えば、上記と同じ`Adder`クラスを以下に示します:

```ts
class Adder {
    constructor(public a: string) { }

    // This function is now safe to pass around
    add = (b: string): string => {
        return this.a + b;
    }
}
```

もう1つの方法は、バインドする変数の型を手動で指定することです。

```ts
const add: typeof adder.add = adder.add.bind(adder);
```
