## 閉鎖

JavaScriptが得た最高のものはクロージャーでした。 JavaScriptの関数は、外部スコープで定義された変数にアクセスできます。クロージャは、例を用いて最もよく説明されます。

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

内部関数は外部スコープからの変数（variableInOuterFunction）へのアクセスを持っていることがわかります。外部関数の変数は、内部関数によって閉じられています（または束縛されています）。したがって、用語**クロージャ**。そのコンセプト自体は簡単で、かなり直感的です。

今すぐ素晴らしい部分：内部関数は外部関数が返された後でも外部スコープ*から変数にアクセスできます*。これは、変数が内部関数に依然としてバインドされており、外部関数に依存していないためです。もう一度例を見てみましょう：

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

### 理由は素晴らしいです
オブジェクトを簡単に作成することができます。明らかなモジュールパターン：

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

高いレベルでは、Node.jsのようなものを作ることもできます（今すぐあなたの脳をクリックしなければ心配しないでください。

```ts
// Pseudo code to explain the concept
server.on(function handler(req, res) {
    loadData(req.id).then(function(data) {
        // the `res` has been closed over and is available
        res.send(data);
    })
});
```
