# Never

> [never型のビデオレッスン](https://egghead.io/lessons/typescript-use-the-never-type-to-avoid-code-with-dead-ends-using-typescript)

プログラミング言語の設計には、bottom型の概念があります。それは、データフロー解析を行うと現れるものです。TypeScriptはデータフロー解析(😎)を実行するので、決して起こりえないようなものを確実に表現する必要があります。

`never`型は、このbottom型を表すためにTypeScriptで使用されます。自然発生するケース：

* 絶対にreturnされない関数(例えば、関数本体に `while(true){}`がある場合)
* 常にthrowする関数(例えば `function foo(){throw new Error('Not Implemented')}`の場合、`foo`の戻り値の型は`never`です)

もちろん、このアノテーションを自分でも使用できます

```ts
let foo: never; // Okay
```

しかし、neverは、neverだけを代入することができます。例:

```ts
let foo: never = 123; // Error: Type number is not assignable to never

// Okay as the function's return type is `never`
let bar: never = (() => { throw new Error('Throw my hands in the air like I just dont care') })();
```

すばらしい。さあ、主な使用例を見てみましょう:)

# ユースケース： 網羅チェック(Exhaustive Checks)

たどり着けないコンテキストで関数を呼び出すことはできません。

```ts
function foo(x: string | number): boolean {
  if (typeof x === "string") {
    return true;
  } else if (typeof x === "number") {
    return false;
  }

  // Without a never type we would error :
  // - Not all code paths return a value (strict null checks)
  // - Or Unreachable code detected
  // But because typescript understands that `fail` function returns `never`
  // It can allow you to call it as you might be using it for runtime safety / exhaustive checks.
  return fail("Unexhaustive!");
}

function fail(message: string): never { throw new Error(message); }
```

`never`は他の`never`にのみ割り当てられるので、コンパイル時の網羅チェックのためにも使うことができます。これは[ユニオン判別のセクション](./discriminated-unions.md)で説明します。

# `void`との混乱

関数が正常に終了することがないとき、`never`が返されると知ると、直感的に`void`と同じように考えたくなるでしょう。しかし、`void`は部品です。`never`はうそつきです。

何も返さない関数は`void`を返します。しかし、returnを返すことのない関数(または常にスローする)は`never`を返します。`void`は(strictNullCheckingなしで)代入することができるものですが、`never`は`never`以外のものに代入することはできません。
