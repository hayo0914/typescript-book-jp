# Promise（プロミス）

## Promise

`Promise`クラスは、多くのモダンなJavaScriptエンジンに存在し、簡単に[polyfill](https://github.com/stefanpenner/es6-promise)できます。Promiseを使う動機は、非同期/コールバック的なスタイルのコードに対して、同期処理的なスタイルでエラーを取り扱うことを可能にすることです。

### コールバックを用いたスタイルのコード

Promiseを完全に理解するため、信頼性の高い非同期処理をコールバックだけで構築する難しさをサンプルコードで示します。ファイルからJSONをロードする処理の非同期バージョンを作成するケースを考えてみましょう。これの同期バージョンは非常にシンプルです:

```typescript
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

このシンプルな`loadJSONSync`には有効な戻り値、ファイルシステムエラー、JSON.parseエラーの3種類の動作があります。私たちは、他の言語で同期処理を行う際に慣れていたように、単純なtry/catchでエラーを処理します。さて、このような関数について、良い関数を非同期バージョンで作ってみましょう。最初の素朴な試みとして作成した関数です。些細なエラーチェックロジックを入れています。:

```typescript
import fs = require('fs');

// A decent initial attempt .... but not correct. We explain the reasons below
function loadJSON(filename: string, cb: (error: Error, data: any) => void) {
    fs.readFile(filename, function (err, data) {
        if (err) cb(err);
        else cb(null, JSON.parse(data));
    });
}
```

十分シンプルです。コールバックをとり、ファイルシステムのエラーをコールバックに渡します。ファイルシステムのエラーがなければ、`JSON.parse`の結果を返します。コールバックに基づいて非同期関数を利用するときに注意すべき点は次のとおりです。

1. 決してコールバックを2回呼ばないでください。
2. 決して Error を投げないでください。

しかしながら、この単純な関数は2つ目の点に対応できません。実際にJSON.parseに間違ったJSONが渡されると、Error が発生し、コールバックが呼び出されず、アプリケーションがクラッシュします。これを以下の例で示します：

```typescript
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

これを修正するための素朴な試みは、次の例に示すように`JSON.parse`をtry catchにラップすることです。

```typescript
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

しかし、このコードには些細なバグがあります。もしコールバック\(`cb`\)がコールされ、`JSON.parse`がコールされず、エラーをスローした場合、`try`/`catch`でラップしているため、`catch`が実行され、コールバックを再度コールされてしまいます。つまり、コールバックが二度コールされてしまいます!これを以下の例で示します：

```typescript
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

これは、`loadJSON`関数が間違って`try`ブロックでコールバックをラップしたためです。ここで覚えておくべき簡単な教訓があります。

> シンプルな教訓：コールバックをコールするとき以外のすべての同期コードをtry catchに含めること。

このシンプルな教訓に基づいて、我々は完全に機能する非同期バージョンの`loadJSON`を作成できます：

```typescript
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

確かに何回か行えば、そう難しいことではありませんが、単に、良いエラー処理を書くためだけに多くの定型的なコードが必要です。では、Promiseを使ってJavaScriptの非同期処理に取り組むための、より良い方法を見てみましょう。

## Promiseを作る

Promiseの状態は、`pending`\(保留中\)または`fulfilled`\(履行済み\)または`rejected`\(拒絶済み\)のいずれかになります。

![Promise&#x306E;&#x5BA3;&#x8A00;&#x3068;&#x904B;&#x547D;](https://raw.githubusercontent.com/basarat/typescript-book/master/images/promise%20states%20and%20fates.png)

Promiseの作り方を見てみましょう。Promise\(Promiseのコンストラクタ\)に対して`new`を呼び出すだけです。Promiseのコンストラクタには、Promiseの状態を決めるための`resolve`関数と`reject`関数が渡されます。

```typescript
const promise = new Promise((resolve, reject) => {
    // the resolve / reject functions control the fate of the promise
});
```

### Promiseの結果を監視\(subscribing\)する

Promiseの結果は、`.then`\(resolveが実行された場合\)または`.catch`\(rejectが実行された場合\)を使用して監視\(Subscribe\)できます。

```typescript
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

```typescript
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

> TIP：Promiseのショートカット
>
> * すでにresolveされているPromiseをクイックに作成する：`Promise.resolve(result)`
> * 既にrejectされているPromiseをクイックに作成する： `Promise.reject(error)`

### Promiseのチェーン

Promiseのチェーンは**Promiseを使う最大のメリット**です。一度Promiseを取得すれば、その時点から、`then`関数を使ってPromiseのチェーンを作れます。

* もしチェーン内の関数からPromiseを返すと、そのPromiseがresolveされた時に1回だけ`.then`が呼び出されます：

```typescript
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

* チェーンの前の部分のエラー処理を単一の`catch`に集約することができます：

```typescript
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

* `catch`は実のところ新しいPromiseを返します\(要するに新しいPromiseのチェーンを作成します\)：

```typescript
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

* `then`\(または`catch`\)で同期エラーがスローされると、返されたPromiseが失敗します：

```typescript
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

* エラーが発生すると関係している\(後方で最も近い\)`catch`だけがコールされます\(同時にcatchが新しい`Promise`のチェーンを作ります\)。

```typescript
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

* `catch`はチェーンの前部分でエラーが発生した場合にのみコールされます：

```typescript
Promise.resolve(123)
    .then((res) => {
        return 456;
    })
    .catch((err) => {
        console.log("HERE"); // never called
    })
```

Promiseチェーンに関する事実：

* エラーが起きた場合、後続の`catch`にジャンプします\(そして途中の`then`はスキップします\)
* 同期処理のエラーについても同様に、最も近い後続の`catch`で捕捉されます

Promiseは、生のコールバックに比べて優れたエラー処理を可能にする非同期プログラミングのパラダイムを我々に提供してくれます。さらに下記に詳しく記載します。

### TypeScriptとPromise

TypeScriptが素晴らしい点は、それがPromiseチェーンを通じて流れる値を理解してくれることです。

```typescript
Promise.resolve(123)
    .then((res) => {
         // res is inferred to be of type `number`
         return true;
    })
    .then((res) => {
        // res is inferred to be of type `boolean`

    });
```

もちろん、Promiseを返す可能性のある関数呼び出しも理解してくれます。

```typescript
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

### コールバックスタイルの関数をPromiseを返すように変える

関数呼び出しをPromiseにラップして

* エラーが発生した場合は `reject`をコールする
* すべてうまく行った場合は`resolve`をコールする

例えば`fs.readFile`をラップしましょう：

```typescript
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

次に、`loadJSON`の例を見直して、Promiseを使う非同期バージョンを書いてみましょう。やるべきことは、Promiseとしてファイル内容を読み、JSONとしてパースする、それだけです。これを以下の例で示します:

```typescript
function loadJSONAsync(filename: string): Promise<any> {
    return readFileAsync(filename) // Use the function we just wrote
                .then(function (res) {
                    return JSON.parse(res);
                });
}
```

使い方\(このセクションの始めに紹介した同期\( `sync` \)バージョンとどれだけ似ているかに注目してください🌹\)：

```typescript
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

この関数がよりシンプルになった理由は、"`loadFile`\(async\)+`JSON.parse`\(sync\)=&gt;`catch`"の連結をPromiseチェーンによって行ったためです。また、コールバックは我々ではなくPromiseチェーンによってコールされるので、コールバックを`try/catch`でラップしてしまう誤りが起きる可能性はありませんでした。

### 並列制御フロー\(Parallel control flow\)

私たちは、Promiseを使って非同期タスクの順次処理（シーケンシャル処理）を行うことがいかに簡単かを見てきました。単に`then`の呼び出しをチェーンするだけなのです。

しかし、複数の非同期処理を実行し、すべてのタスクが終わったタイミングで何らかの処理を行いたいケースがあるかもしれません。`Promise`は静的な`Promise.all`関数を提供します。この関数は、`n`個のPromiseがすべて完了するまで待つことができます。`n`個のPromiseの配列を渡すと、`n`個の解決された値の配列を返します。以下では、チェーンの例と合わせて並列で処理する例を示します。

```typescript
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

ある場合には、複数の非同期タスクを実行するが、これらのタスクの内1つだけが完了すれば良いケースもあるでしょう。`Promise`は、このユースケースに対して`Promise.race`というStatic関数を提供しています：

```typescript
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

### コールバック関数をPromiseに変換する

これを行うために信頼性が高い方法は、自分でコードを書くことです。例えば`setTimeout`をPromiseを使った`delay`関数に変換するのは非常に簡単です：

```typescript
const delay = (ms: number) => new Promise(res => setTimeout(res, ms));
```

NodeJSにはこれを行う便利で使いやすい関数があることを知っておいてください。これは `Nodeスタイルの関数 => Promiseを返す関数` に変える魔法を行ってくれます。

```typescript
/** Sample usage */
import fs = require('fs');
import util = require('util');
const readFile = util.promisify(fs.readFile);
```

