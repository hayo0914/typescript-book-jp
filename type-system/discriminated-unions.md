# 判別可能なUnion型

## Union型の判別\(Discriminated Union\)

[_literal型のメンバ_](literal-types.md)を持つクラスがある場合、そのプロパティを使用して、Union型のメンバを判別することができます。

例として、`Square`と`Rectangle`のUnionを考えてみましょう。ここでは`kind`（特定のリテラル型）は両方のUnion型のメンバに存在しています:

```typescript
interface Square {
    kind: "square";
    size: number;
}

interface Rectangle {
    kind: "rectangle";
    width: number;
    height: number;
}
type Shape = Square | Rectangle;
```

判別用のプロパティ\(ここでは`kind`\)に対して、型安全なチェック\(`==`、`===`、`!=`、`!==`\)または`switch`を使用すると、TypeScriptはあなたのために、そのリテラル型を持つオブジェクトの型を特定し、型の絞り込みを行います :\)

```typescript
function area(s: Shape) {
    if (s.kind === "square") {
        // Now TypeScript *knows* that `s` must be a square ;)
        // So you can use its members safely :)
        return s.size * s.size;
    }
    else {
        // Wasn't a square? So TypeScript will figure out that it must be a Rectangle ;)
        // So you can use its members safely :)
        return s.width * s.height;
    }
}
```

## 網羅チェック\(Exhaustive Checks\)

一般論として、あなたはユニオンのすべてのメンバに対して漏れなくコード\(またはアクション\)が存在していることを確認したいでしょう。

```typescript
interface Square {
    kind: "square";
    size: number;
}

interface Rectangle {
    kind: "rectangle";
    width: number;
    height: number;
}

// Someone just added this new `Circle` Type
// We would like to let TypeScript give an error at any place that *needs* to cater for this
interface Circle {
    kind: "circle";
    radius: number;
}

type Shape = Square | Rectangle | Circle;
```

`Circle`のインスタンスが渡された場合に悪いことが起きる例：

```typescript
function area(s: Shape) {
    if (s.kind === "square") {
        return s.size * s.size;
    }
    else if (s.kind === "rectangle") {
        return s.width * s.height;
    }
    // Would it be great if you could get TypeScript to give you an error?
}
```

これをチェックするには、フォールスルー\(else\)を追加し、そのブロックの推論された型が`never`型と互換性があるかを確認するだけです。たとえば、その網羅チェックを追加すると、ナイスなエラーが発生します:

```typescript
function area(s: Shape) {
    if (s.kind === "square") {
        return s.size * s.size;
    }
    else if (s.kind === "rectangle") {
        return s.width * s.height;
    }
    else {
        // ERROR : `Circle` is not assignable to `never`
        const _exhaustiveCheck: never = s;
    }
}
```

これによって、あなたは新しいケースに対応することを強制されます：

```typescript
function area(s: Shape) {
    if (s.kind === "square") {
        return s.size * s.size;
    }
    else if (s.kind === "rectangle") {
        return s.width * s.height;
    }
    else if (s.kind === "circle") {
        return Math.PI * (s.radius **2);
    }
    else {
        // Okay once more
        const _exhaustiveCheck: never = s;
    }
}
```

## スイッチ\(Switch\)

ヒント：もちろん、`switch`ステートメントでも同じことが可能です：

```typescript
function area(s: Shape) {
    switch (s.kind) {
        case "square": return s.size * s.size;
        case "rectangle": return s.width * s.height;
        case "circle": return Math.PI * s.radius * s.radius;
        default: const _exhaustiveCheck: never = s;
    }
}
```

## strictNullChecks

strictNullChecksを使用して網羅チェックを行っている場合、TypeScriptは"not all code paths return a value"というエラーを出すかもしれません。そのエラーを黙らせるには、シンプルに`_exhaustiveCheck`変数\(never型\)を返すだけです:

```typescript
function area(s: Shape) {
    switch (s.kind) {
        case "square": return s.size * s.size;
        case "rectangle": return s.width * s.height;
        case "circle": return Math.PI * s.radius * s.radius;
        default:
          const _exhaustiveCheck: never = s;
          return _exhaustiveCheck;
    }
}
```

## 網羅チェックの中で例外を投げる

引数として`never`を取る関数を書くことができます\(したがって、この関数は`never`として推論された変数で呼ばれた場合にのみ呼ばれます\)。そして、次のように、関数の本体が実行された場合に例外を投げるように書きます。

```typescript
function assertNever(x:never): never {
    throw new Error('Unexpected value. Should have been never.');
}
```

以下に、`area`関数とともに使用する例を示します。

```typescript
interface Square {
    kind: "square";
    size: number;
}
interface Rectangle {
    kind: "rectangle";
    width: number;
    height: number;
}
type Shape = Square | Rectangle;

function area(s: Shape) {
    switch (s.kind) {
        case "square": return s.size * s.size;
        case "rectangle": return s.width * s.height;
        // If a new case is added at compile time you will get a compile error
        // If a new value appears at runtime you will get a runtime error
        default: return assertNever(s);
    }
}
```

## Retrospective Versioning

次のような形のデータ構造があるとします。

```typescript
type DTO = {
  name: string
}
```

そして、`DTO`をさまざまな場所で使用した後に、`name`という名前は良くない選択だったことに気が付いたとします。このような場合には、_リテラルの数値_\(または望むなら文字列\)を追加したDTOの新しい_ユニオン型_を定義することで、後から型にバージョニングを追加することができます。_strictNullChecks_を有効にしていれば、バージョン0を`undefined`とマークするだけで、そのバージョンの型が使われているかどうかのチェックを自動的に行えます。

```typescript
type DTO = 
| { 
   version: undefined, // version 0
   name: string,
 }
| {
   version: 1,
   firstName: string,
   lastName: string, 
}
// Even later 
| {
    version: 2,
    firstName: string,
    middleName: string,
    lastName: string, 
} 
// So on
```

このように定義したDTOは、次のように利用します。

```typescript
function printDTO(dto:DTO) {
  if (dto.version == null) {
      console.log(dto.name);
  } else if (dto.version == 1) {
      console.log(dto.firstName,dto.lastName);
  } else if (dto.version == 2) {
      console.log(dto.firstName, dto.middleName, dto.lastName);
  } else {
      const _exhaustiveCheck: never = dto;
  }
}
```

## Redux

ユニオン判別を活用しているポピュラーなライブラリはreduxです。

ここに、TypeScript型アノテーションを追加した [_gist of redux_](https://github.com/reactjs/redux#the-gist) があります：

```typescript
import { createStore } from 'redux'

type Action
  = {
    type: 'INCREMENT'
  }
  | {
    type: 'DECREMENT'
  }

/**
 * This is a reducer, a pure function with (state, action) => state signature.
 * It describes how an action transforms the state into the next state.
 *
 * The shape of the state is up to you: it can be a primitive, an array, an object,
 * or even an Immutable.js data structure. The only important part is that you should
 * not mutate the state object, but return a new object if the state changes.
 *
 * In this example, we use a `switch` statement and strings, but you can use a helper that
 * follows a different convention (such as function maps) if it makes sense for your
 * project.
 */
function counter(state = 0, action: Action) {
  switch (action.type) {
  case 'INCREMENT':
    return state + 1
  case 'DECREMENT':
    return state - 1
  default:
    return state
  }
}

// Create a Redux store holding the state of your app.
// Its API is { subscribe, dispatch, getState }.
let store = createStore(counter)

// You can use subscribe() to update the UI in response to state changes.
// Normally you'd use a view binding library (e.g. React Redux) rather than subscribe() directly.
// However, it can also be handy to persist the current state in the localStorage.

store.subscribe(() =>
  console.log(store.getState())
)

// The only way to mutate the internal state is to dispatch an action.
// The actions can be serialized, logged or stored and later replayed.
store.dispatch({ type: 'INCREMENT' })
// 1
store.dispatch({ type: 'INCREMENT' })
// 2
store.dispatch({ type: 'DECREMENT' })
// 1
```

これをTypeScriptで使うことにより、型安全性とリファクタ容易性、そしてコードの自己文書化を図ることができます。

