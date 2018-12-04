### 差別化された組合

[* literalメンバー*]（./ literal-types.md）を持つクラスがある場合、そのプロパティを使用して、共用体メンバーを区別することができます。

例として、 `Square`と`Rectangle`の和集合を考えてみましょう。ここでは、両方の共用体メンバに存在し、特定の*リテラル型のメンバ `kind`があります*：

```ts
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

* discriminantプロパティ（ここで `kind`）にタイプガードスタイルチェック（`== `、`=== `、`！= `、`！== `）または`switch`を使用すると、TypeScriptはそのオブジェクトは、その特定のリテラルを持つタイプのものでなければならず、あなたのためにタイプを狭くする必要があります:)

```ts
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

### 完全なチェック
かなり一般的には、組合のすべてのメンバーがそれらに対していくつかのコード（行動）を持っていることを確認したいと思います。

```ts
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

物が悪くなる場所の例として：

```ts
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

これを行うには、フォールスルーを追加し、そのブロックの推論された型が `never`型と互換性があることを確認するだけです。たとえば、徹底的なチェックを追加すると、すばらしいエラーが発生します。

```ts
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

それはこの新しいケースを扱うことを強いられます：

```ts
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


### スイッチ
ヒント：もちろん、あなたは `switch`ステートメントでそれを行うこともできます：

```ts
function area(s: Shape) {
    switch (s.kind) {
        case "square": return s.size * s.size;
        case "rectangle": return s.width * s.height;
        case "circle": return Math.PI * s.radius * s.radius;
        default: const _exhaustiveCheck: never = s;
    }
}
```

[references-discriminated-union]：https：//github.com/Microsoft/TypeScript/pull/9163

### strictNullChecks

strictNullChecksを使用して網羅的なチェックを行っている場合、 `_exhaustiveCheck`変数（`never`型）も返さなければなりません。そうでなければ、TypeScriptは `undefined`の可能な戻り値を推論します。そう：

```ts
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

### Redux

これを利用する普及した図書館は、還元的です。

ここに、TypeScript型アノテーションを追加した[* gist of redux *]（https://github.com/reactjs/redux#the-gist）があります：

```ts
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
// However it can also be handy to persist the current state in the localStorage.

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

TypeScriptで使用すると、誤植、リファクタリング能力の向上、および自己文書化コードに対する安全性が確保されます。
