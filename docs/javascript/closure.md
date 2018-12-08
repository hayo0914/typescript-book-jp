## クロージャ(Closure)

JavaScriptで最高のものはクロージャでした。 JavaScriptの関数は、外部スコープで定義された変数にアクセスできます。クロージャは、例を見るのが一番わかり易いです。

```ts
function outerFunction(arg) {
    var variableInOuterFunction = arg;

    function bar() {
        console.log(variableInOuterFunction); // Access a variable from the outer scope
    }

    // Call the local function to demonstrate that it has access to arg
    bar();
}

outerFunction("hello closure"); // logs hello closure!
```

内側の関数は外側のスコープの変数(variableInOuterFunction)にアクセスできることがわかります。外側の関数の変数は、内側の関数に閉包されています(または束縛されています)。したがって、クロージャ(closure)という用語のコンセプト自体は簡単で直感的です。

クロージャの素晴らしい点：内側の関数は、外側の関数が`return`された後でも変数にアクセスできます。これは変数が内側の関数に束縛されており、外側の関数に依存していないからです。もう一度例を見てみましょう：

```ts
function outerFunction(arg) {
    var variableInOuterFunction = arg;
    return function() {
        console.log(variableInOuterFunction);
    }
}

var innerFunction = outerFunction("hello closure!");

// Note the outerFunction has returned
innerFunction(); // logs hello closure!
```

### なぜクロージャが素晴らしいか
オブジェクトを簡単に作成することができます。リビーリングモジュールパターン(revealing module pattern)：

```ts
function createCounter() {
    let val = 0;
    return {
        increment() { val++ },
        getVal() { return val }
    }
}

let counter = createCounter();
counter.increment();
console.log(counter.getVal()); // 1
counter.increment();
console.log(counter.getVal()); // 2
```

クロージャを使いこなせば、Node.jsのようなものを作ることもできます(今ピンとこなくても、心配しないでください。最終的には分かります🌹):

```ts
// Pseudo code to explain the concept
server.on(function handler(req, res) {
    loadData(req.id).then(function(data) {
        // the `res` has been closed over and is available
        res.send(data);
    })
});
```
