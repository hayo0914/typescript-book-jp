# クロージャ

JavaScriptで最も素晴らしいものは、クロージャでした。 JavaScript関数は、外部スコープで定義された変数にアクセスできます。クロージャを理解するには、例を見るのが一番です。

```typescript
function outerFunction(arg) {
    var variableInOuterFunction = arg;

    function bar() {
        console.log(variableInOuterFunction); // 外側のスコープにある変数にアクセスします
    }

    // argにアクセスできることを示すために、ローカル関数を呼び出します。
    bar();
}

outerFunction("hello closure"); // "hello closure"とログに出力されます
```

内側の関数は外側のスコープの変数\(variableInOuterFunction\)にアクセスできることがわかります。外側の関数の変数は、内側の関数に閉包されています\(または束縛されています\)。したがって、クロージャ\(closure\)という用語のコンセプト自体は簡単で直感的です。

クロージャの素晴らしい点：内側の関数は、外側の関数が`return`された後でも変数にアクセスできます。これは変数が内側の関数に束縛されており、外側の関数に依存していないからです。もう一度例を見てみましょう：

```typescript
function outerFunction(arg) {
    var variableInOuterFunction = arg;
    return function() {
        console.log(variableInOuterFunction);
    }
}

var innerFunction = outerFunction("hello closure!");

// outerFunctionが返しているものに注意してください
innerFunction(); // "hello closure" と出力されます
```

## なぜクロージャが素晴らしいか

オブジェクトを簡単に作成することができます。リヴィーリングモジュール\(revealing module pattern\)というコーディングパターンがあります：

```typescript
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

クロージャを使いこなせば、Node.jsのようなものを作ることもできます\(今はピンとこなくても、心配しないでください。最終的には分かります🌹\):

```typescript
// 概念を説明するための疑似コード
server.on(function handler(req, res) {
    loadData(req.id).then(function(data) {
        // `res`が閉じ込められており、ここで利用可能です
        res.send(data);
    })
});
```

