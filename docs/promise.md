## 約束する

`Promise`クラスは、多くの最新のJavaScriptエンジンに存在し、簡単に[polyfill] [polyfill]することができます。約束の主な動機は、同期スタイルエラー処理をAsync / Callbackスタイルコードに持たせることです。

### コールバックスタイルコード

約束を完全に理解するために、コールバックだけで信頼性の高い非同期コードを作成することの難しさを証明する簡単なサンプルを提示しましょう。ファイルからJSONをロードする非同期バージョンをオーサリングする単純なケースを考えてみましょう。この同期バージョンは非常に簡単です。

```ts
import fs = require('fs');

function loadJSONSync(filename: string) {
    return JSON.parse(fs.readFileSync(filename));
}

// good json file
console.log(loadJSONSync('good.json'));

// non-existent file, so fs.readFileSync fails
try {
    console.log(loadJSONSync('absent.json'));
}
catch (err) {
    console.log('absent.json error', err.message);
}

// invalid json file i.e. the file exists but contains invalid JSON so JSON.parse fails
try {
    console.log(loadJSONSync('invalid.json'));
}
catch (err) {
    console.log('invalid.json error', err.message);
}
```

この単純な `loadJSONSync`関数、有効な戻り値、ファイルシステムエラー、またはJSON.parseエラーの3つの動作があります。私たちは、他の言語で同期プログラミングを行う際に慣れていたように、単純なtry / catchでエラーを処理します。このような関数の良い非同期バージョンを作ってみましょう。些細なエラーチェックロジックでまともな試みは次のようになります：

```ts
import fs = require('fs');

// A decent initial attempt .... but not correct. We explain the reasons below
function loadJSON(filename: string, cb: (error: Error, data: any) => void) {
    fs.readFile(filename, function (err, data) {
        if (err) cb(err);
        else cb(null, JSON.parse(data));
    });
}
```

十分単純で、コールバックをとり、ファイルシステムエラーをコールバックに渡します。ファイルシステムエラーがなければ、 `JSON.parse`の結果を返します。コールバックに基づいて非同期関数を操作するときに留意すべき点は次のとおりです。

1. 決してコールバックを2回コールしないでください。
1. 決してエラーを投げないでください。

しかしながら、この単純な関数は点2に対応できない。実際にJSON.parseはJSONが渡され、コールバックが呼び出されず、アプリケーションがクラッシュするとエラーをスローします。これは以下の例で示されます：

```ts
import fs = require('fs');

// A decent initial attempt .... but not correct
function loadJSON(filename: string, cb: (error: Error, data: any) => void) {
    fs.readFile(filename, function (err, data) {
        if (err) cb(err);
        else cb(null, JSON.parse(data));
    });
}

// load invalid json
loadJSON('invalid.json', function (err, data) {
    // This code never executes
    if (err) console.log('bad.json error', err.message);
    else console.log(data);
});
```

これを修正する単純な試みは、次の例に示すように `JSON.parse`をtry catchにラップすることです。

```ts
import fs = require('fs');

// A better attempt ... but still not correct
function loadJSON(filename: string, cb: (error: Error) => void) {
    fs.readFile(filename, function (err, data) {
        if (err) {
            cb(err);
        }
        else {
            try {
                cb(null, JSON.parse(data));
            }
            catch (err) {
                cb(err);
            }
        }
    });
}

// load invalid json
loadJSON('invalid.json', function (err, data) {
    if (err) console.log('bad.json error', err.message);
    else console.log(data);
});
```

しかし、このコードには微妙なバグがあります。 `JSON.parse`ではなく、コールバック(`cb`)がエラーをスローすると、 `try`/` catch`でラップしたので、 `catch`が実行され、コールバックを再度コールします。二度呼ばれる!これは以下の例で実証されています：

```ts
import fs = require('fs');

function loadJSON(filename: string, cb: (error: Error) => void) {
    fs.readFile(filename, function (err, data) {
        if (err) {
            cb(err);
        }
        else {
            try {
                cb(null, JSON.parse(data));
            }
            catch (err) {
                cb(err);
            }
        }
    });
}

// a good file but a bad callback ... gets called again!
loadJSON('good.json', function (err, data) {
    console.log('our callback called');

    if (err) console.log('Error:', err.message);
    else {
        // let's simulate an error by trying to access a property on an undefined variable
        var foo;
        // The following code throws `Error: Cannot read property 'bar' of undefined`
        console.log(foo.bar);
    }
});
```

```bash
$ node asyncbadcatchdemo.js
our callback called
our callback called
Error: Cannot read property 'bar' of undefined
```

これは、 `loadJSON`関数が`try`ブロックでコールバックを間違ってラップしたためです。ここで覚えておくべき簡単な教訓があります。

> シンプルなレッスン：コールバックを呼び出すときを除いて、すべてのシンクコードをtryキャッチに入れます。

この簡単なレッスンの後で、以下に示すように完全に機能する非同期バージョンの `loadJSON`があります：

```ts
import fs = require('fs');

function loadJSON(filename: string, cb: (error: Error) => void) {
    fs.readFile(filename, function (err, data) {
        if (err) return cb(err);
        // Contain all your sync code in a try catch
        try {
            var parsed = JSON.parse(data);
        }
        catch (err) {
            return cb(err);
        }
        // except when you call the callback
        return cb(null, parsed);
    });
}
```
確かに、これを数回やった後はこれを実行するのは難しいことではありませんが、エラー処理を簡単に行うためのボイラープレートコードがたくさんあります。では、約束を使って非同期JavaScriptに取り組むより良い方法を見てみましょう。

## 約束をする

約束は、「保留中」または「履行済み」または「拒否」のいずれかになります。

![約束の州と運命](https://raw.githubusercontent.com/basarat/typescript-book/master/images/promise%20states%20and%20fates.png)

約束を作るのを見てみましょう。 Promise(promiseコンストラクタ)で `new`を呼び出すのは簡単なことです。 promiseコンストラクタには、約束状態を解決するために `resolve`と`reject`関数が渡されます。

```ts
const promise = new Promise((resolve, reject) => {
    // the resolve / reject functions control the fate of the promise
});
```

### 約束の運命に加入する

約束運命は、 `.then`(解決された場合)または`.catch`(拒絶された場合)を使用して購読することができます。

```ts
const promise = new Promise((resolve, reject) => {
    resolve(123);
});
promise.then((res) => {
    console.log('I get called:', res === 123); // I get called: true
});
promise.catch((err) => {
    // This is never called
});
```

```ts
const promise = new Promise((resolve, reject) => {
    reject(new Error("Something awful happened"));
});
promise.then((res) => {
    // This is never called
});
promise.catch((err) => {
    console.log('I get called:', err.message); // I get called: 'Something awful happened'
});
```

> ヒント：約束のショートカット
* すでに約束されている約束をすばやく作成する： `Promise.resolve(result)`
* 既に拒否されている約束をすばやく作成する： `Promise.reject(error)`

### 約束の連鎖性
約束**の連鎖能力は、約束**が提供するメリットの中心です。その時点から約束が得られれば、 `then`関数を使って約束を作ることができます。

* チェーン内の関数から約束を返すと、値が解決されたときにのみ `.then`が呼び出されます：

```ts
Promise.resolve(123)
    .then((res) => {
        console.log(res); // 123
        return 456;
    })
    .then((res) => {
        console.log(res); // 456
        return Promise.resolve(123); // Notice that we are returning a Promise
    })
    .then((res) => {
        console.log(res); // 123 : Notice that this `then` is called with the resolved value
        return 123;
    })
```

* チェーンの前の部分のエラー処理を単一の `catch`で集約することができます：

```ts
// Create a rejected promise
Promise.reject(new Error('something bad happened'))
    .then((res) => {
        console.log(res); // not called
        return 456;
    })
    .then((res) => {
        console.log(res); // not called
        return 123;
    })
    .then((res) => {
        console.log(res); // not called
        return 123;
    })
    .catch((err) => {
        console.log(err.message); // something bad happened
    });
```

* `catch 'は実際に新しい約束を返します(効果的に新しい約束を作り出します)：

```ts
// Create a rejected promise
Promise.reject(new Error('something bad happened'))
    .then((res) => {
        console.log(res); // not called
        return 456;
    })
    .catch((err) => {
        console.log(err.message); // something bad happened
        return 123;
    })
    .then((res) => {
        console.log(res); // 123
    })
```

* `then`(または`catch`)でスローされた同期エラーは、返された約束が失敗する結果になります：

```ts
Promise.resolve(123)
    .then((res) => {
        throw new Error('something bad happened'); // throw a synchronous error
        return 456;
    })
    .then((res) => {
        console.log(res); // never called
        return Promise.resolve(789);
    })
    .catch((err) => {
        console.log(err.message); // something bad happened
    })
```

* 関連する(最も近いテーリング) `catch`だけが与えられたエラーに対して呼び出されます(catchが新しい約束を開始するとき)。

```ts
Promise.resolve(123)
    .then((res) => {
        throw new Error('something bad happened'); // throw a synchronous error
        return 456;
    })
    .catch((err) => {
        console.log('first catch: ' + err.message); // something bad happened
        return 123;
    })
    .then((res) => {
        console.log(res); // 123
        return Promise.resolve(789);
    })
    .catch((err) => {
        console.log('second catch: ' + err.message); // never called
    })
```

* `catch`は前のチェーンのエラーの場合にのみ呼び出されます：

```ts
Promise.resolve(123)
    .then((res) => {
        return 456;
    })
    .catch((err) => {
        console.log("HERE"); // never called
    })
```

事実：

* エラーはtailingの `catch`にジャンプします(そして`then`コールは途中でスキップします)。
* 同期エラーはまた、どんなテーリング `catch`でも捕捉されます。

実際には生のコールバックよりも優れたエラー処理を可能にする非同期プログラミングのパラダイムを効果的に提供します。もっと詳しくはこちら。


### TypeScriptと約束
TypeScriptの大きな点は、約束を通した価値の流れを理解することです。

```ts
Promise.resolve(123)
    .then((res) => {
         // res is inferred to be of type `number`
         return true;
    })
    .then((res) => {
        // res is inferred to be of type `boolean`

    });
```

もちろん、約束を返す可能性のある関数呼び出しのアンラッピングも理解しています。

```ts
function iReturnPromiseAfter1Second(): Promise<string> {
    return new Promise((resolve) => {
        setTimeout(() => resolve("Hello world!"), 1000);
    });
}

Promise.resolve(123)
    .then((res) => {
        // res is inferred to be of type `number`
        return iReturnPromiseAfter1Second(); // We are returning `Promise<string>`
    })
    .then((res) => {
        // res is inferred to be of type `string`
        console.log(res); // Hello world!
    });
```


### コールバックスタイル関数を約束を返すように変換する

関数呼び出しを約束して
 - エラーが発生した場合は `reject`を、
 - それがすべて良ければ `解決する`。

例えば。 `fs.readFile`をラップしましょう：

```ts
import fs = require('fs');
function readFileAsync(filename: string): Promise<any> {
    return new Promise((resolve,reject) => {
        fs.readFile(filename,(err,result) => {
            if (err) reject(err);
            else resolve(result);
        });
    });
}
```


### JSONの例を見直す

次に、 `loadJSON`の例を見直して、約束を使う非同期バージョンを書き直しましょう。私たちがする必要があるのは、ファイルの内容を約束として読み、それをJSONとして解析して完了したことだけです。これは以下の例に示されています。

```ts
function loadJSONAsync(filename: string): Promise<any> {
    return readFileAsync(filename) // Use the function we just wrote
                .then(function (res) {
                    return JSON.parse(res);
                });
}
```

使用法(このセクションの始めに導入された元の `sync`バージョンとどれほど似ているか注意してください。)：
```ts
// good json file
loadJSONAsync('good.json')
    .then(function (val) { console.log(val); })
    .catch(function (err) {
        console.log('good.json error', err.message); // never called
    })

// non-existent json file
    .then(function () {
        return loadJSONAsync('absent.json');
    })
    .then(function (val) { console.log(val); }) // never called
    .catch(function (err) {
        console.log('absent.json error', err.message);
    })

// invalid json file
    .then(function () {
        return loadJSONAsync('invalid.json');
    })
    .then(function (val) { console.log(val); }) // never called
    .catch(function (err) {
        console.log('bad.json error', err.message);
    });
```

この関数がより簡単だった理由は、 "loadFile`(async)+`JSON.parse`(sync)=> `catch`"の連結が約束チェーンによって行われたためです。また、コールバックは* us *によって呼び出されませんでしたが、約束チェーンによって呼び出されたので、 `try / catch`でラップする間違いの可能性はありませんでした。

### 並列制御フロー
私たちは、非同期タスクのシリアルシーケンスを行うことが約束どおりにいかに簡単であるかを見てきました。それは単に `then`呼び出しを連鎖させることの問題です。

しかし、一連の非同期タスクを実行し、これらのタスクのすべての結果を使用して何かを実行する可能性があります。 `Promise`は静的な`Promise.all`関数を提供します。この関数は、 `n`回の約束が完了するまで待つことができます。あなたは `n`約束の配列を提供し、`n`個の解決された値の配列を返します。以下では、連鎖と同様に連鎖を示します。

```ts
// an async function to simulate loading an item from some server
function loadItem(id: number): Promise<{ id: number }> {
    return new Promise((resolve) => {
        console.log('loading item', id);
        setTimeout(() => { // simulate a server delay
            resolve({ id: id });
        }, 1000);
    });
}

// Chaining
let item1, item2;
loadItem(1)
    .then((res) => {
        item1 = res;
        return loadItem(2);
    })
    .then((res) => {
        item2 = res;
        console.log('done');
    }); // overall time will be around 2s

// Parallel
Promise.all([loadItem(1), loadItem(2)])
    .then((res) => {
        [item1, item2] = res;
        console.log('done');
    }); // overall time will be around 1s
```

場合によっては、一連の非同期タスクを実行したい場合もありますが、これらのタスクのいずれかが解決されている限り、必要なものはすべて得られます。 `Promise`は、このシナリオに対して静的な`Promise.race`関数を提供します：

```ts
var task1 = new Promise(function(resolve, reject) {
    setTimeout(resolve, 1000, 'one');
});
var task2 = new Promise(function(resolve, reject) {
    setTimeout(resolve, 2000, 'two');
});

Promise.race([task1, task2]).then(function(value) {
  console.log(value); // "one"
  // Both resolve, but task1 resolves faster
});
```

### コールバック関数を約束するように変換する

これを行う最も信頼できる方法は、手書きで書くことです。例えば`setTimeout`をpromisified`delay`関数に変換するのは簡単です：

```ts
const delay = (ms: number) => new Promise(res => setTimeout(res, ms));
```

NodeJSには、この `node style function =>関数を返す`という魔法を使う便利なダンディー関数があることに注意してください。

```ts
/** Sample usage */
import fs = require('fs');
import util = require('util');
const readFile = util.promisify(fs.readFile);
```

[polyfill]：https：//github.com/stefanpenner/es6-promise
