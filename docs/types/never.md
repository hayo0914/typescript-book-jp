# 決して

> [決してタイプしないビデオレッスン]（https://egghead.io/lessons/typescript-use-the-never-type-to-avoid-code-with-dead-ends-using-typescript）

プログラミング言語の設計には、コードフロー解析*を行うとすぐに**自然な結果である* bottom *型の概念があります。 TypeScriptは*フロー解析*（😎）を実行するので、決して起こりえないようなものを確実に表現する必要があります。

`never`型は、この* bottom型を表すためにTypeScriptで使用されます。自然発生した場合：

* 関数が返ることはありません（例えば、関数本体に `while（true）{}`がある場合）
* 関数は常に（例えば `function foo（）{throw new Error（ '実装されていません'）}` `foo`の戻り値の型は`never`です）

もちろん、この注釈を自分でも使用できます

```ts
let foo: never; // Okay
```

しかし、決して*決して*決して他の決して*割り当てることができません。例えば

```ts
let foo: never = 123; // Error: Type number is not assignable to never

// Okay as the function's return type is `never`
let bar: never = (() => { throw new Error('Throw my hands in the air like I just dont care') })();
```

すばらしいです。さあ、その主要な使用例に飛び乗りましょう:)

# ユースケース：完全なチェック

neverコンテキストで関数を決して呼び出すことはできません。

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

`never`は他の`never`にのみ割り当てられるので、* compile time *徹底的なチェックのためにも使うことができます。これは[* discriminated union *セクション]（./ discriminated-unions.md）で網羅されています。

# 「ボイド」との混乱

関数が正常に終了しないときには `never`が返されると直ちに直感的に`void`と同じように考えたいと思っていますが、 `void`はUnitです。 `決して`はうそつきです。

* 何も返さない関数はユニット `void`を返します。しかし、*を返すことのない関数（または常にスローする）*は `never`を返します。 `void`は（strictNullCheckingなしで）割り当てることができるものですが、`never`以外のものに `never`を割り当てることはできません。

<！ - 
PR：https://github.com/Microsoft/TypeScript/pull/8652
問題：https://github.com/Microsoft/TypeScript/issues/3076
コンセプト：https://en.wikipedia.org/wiki/Bottom_type
 - >
