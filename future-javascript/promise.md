# Promise

## Promise

`Promise`クラスは、多くのモダンなJavaScriptエンジンに存在しており、簡単に[polyfill](https://github.com/stefanpenner/es6-promise)することができます。Promiseを使いたい理由は、非同期/コールバック的なスタイルのコードに対して、同期処理の書き方でエラーを取り扱うことができるからです。

### コールバックを用いたスタイルのコード

Promiseを完全に理解するため、信頼性の高い非同期処理をコールバックだけで構築する難しさをサンプルコードで示します。ファイルからJSONをロードする処理の非同期バージョンを作成するケースを考えてみましょう。これの同期処理バージョンは非常にシンプルです:

```typescript
import fs = require('fs');

function loadJSONSync(filename: string) {
    return JSON.parse(fs.readFileSync(filename));
}

// 正しいjsonファイル
console.log(loadJSONSync('good.json'));

// 存在しないファイル: fs.readFileSync が失敗する
try {
    console.log(loadJSONSync('absent.json'));
}
catch (err) {
    console.log('absent.json error', err.message);
}

// 正しくないjsonファイル 例: ファイルは存在するが、JSON.parseが失敗する
try {
    console.log(loadJSONSync('invalid.json'));
}
catch (err) {
    console.log('invalid.json error', err.message);
}
```

このシンプルな`loadJSONSync`には有効な戻り値、ファイルシステムエラー、JSON.parseエラーの3種類の動作があります。私たちは、他の言語で同期処理を行う際に慣れていたように、単純なtry/catchでエラーを処理します。さて、このような関数について、良い関数を非同期バージョンで作ってみましょう。最初の素朴な試みとして作成した関数です。些細なエラーチェックのロジックを追加しています。:

```typescript
import fs = require('fs');

// 最初に思いつくであろう試みですが、正しくありません. その理由は下で説明します
function loadJSON(filename: string, cb: (error: Error, data: any) => void) {
    fs.readFile(filename, function (err, data) {
        if (err) cb(err);
        else cb(null, JSON.parse(data));
    });
}
```

十分にシンプルです。コールバックを引数に受け取り、ファイルシステムのエラーをコールバックに渡します。ファイルシステムのエラーがなければ、`JSON.parse`の結果を返します。コールバックに基づいて非同期関数を利用するときに注意すべき点は次のとおりです。

1. 決してコールバックを2回呼ばないでください。
2. 決して Error を`throw`しないでください。

しかしながら、この単純な関数は2つ目の点に対応できません。実際にJSON.parseに間違ったJSONが渡されると、Error が`throw`され、コールバックが呼び出されず、アプリケーションがクラッシュします。これを以下の例で示します：

```typescript
import fs = require('fs');

// 最初に思いつくであろう試みですが、正しくありません
function loadJSON(filename: string, cb: (error: Error, data: any) => void) {
    fs.readFile(filename, function (err, data) {
        if (err) cb(err);
        else cb(null, JSON.parse(data));
    });
}

// 正しくないJSONファイルのロード
loadJSON('invalid.json', function (err, data) {
    // このコードは永久に実行されません
    if (err) console.log('bad.json error', err.message);
    else console.log(data);
});
```

これを修正するための素朴な試みは、次の例に示すように`JSON.parse`をtry catchで囲むことです。

```typescript
import fs = require('fs');

// より改善したバージョンです。しかし、まだ正しくありません。
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

// 正しくないJSONファイルのロード
loadJSON('invalid.json', function (err, data) {
    if (err) console.log('bad.json error', err.message);
    else console.log(data);
});
```

しかし、このコードには些細なバグがあります。もしコールバック\(`cb`\)が呼び出され、`JSON.parse`が呼び出されずに、エラーを`throw`した場合、`try`/`catch`で囲んでいるため、`catch`が実行され、コールバックを再度呼び出してしまいます。つまり、コールバックが二度呼び出されてしまいます！これを以下の例で示します：

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

// 正しいファイルですが、コールバックの呼び方が間違っています。２回呼び出されてしまいます！
loadJSON('good.json', function (err, data) {
    console.log('our callback called');

    if (err) console.log('Error:', err.message);
    else {
        // undefinedの値にアクセスすることによってエラーを再現します
        var foo;
        // このコードは `Error: undefined の'bar'プロパティを読み込めません` というエラーを表示します
        console.log(foo.bar);
    }
});
```

```bash
$ node asyncbadcatchdemo.js
our callback called
our callback called
Error: undefined の'bar'プロパティを読み込めません
```

これは、`loadJSON`関数が間違って`try`ブロックでコールバックを囲んでいるためです。ここで覚えておくべき簡単な教訓があります。

> シンプルな教訓：コールバックをコールするとき以外のすべての同期処理コードをtry catchで囲むこと。

このシンプルな教訓に基づいて、私達は完全に機能する非同期バージョンの`loadJSON`を作成できます：

```typescript
import fs = require('fs');

function loadJSON(filename: string, cb: (error: Error) => void) {
    fs.readFile(filename, function (err, data) {
        if (err) return cb(err);
        // すべての同期処理コードをtry catchブロックに含める
        try {
            var parsed = JSON.parse(data);
        }
        catch (err) {
            return cb(err);
        }
        // コールバックを呼び出す時を除く
        return cb(null, parsed);
    });
}
```

確かに何回か行えば、そう難しいことではありませんが、単に、良いエラー処理を書くためだけに、このような多くの定型的なコードが必要です。では、Promiseを使ってJavaScriptの非同期処理に取り組むための、より良い方法を見てみましょう。

## Promiseを作る

Promiseの状態は、`pending`\(保留中\)または`fulfilled`\(履行済み\)または`rejected`\(拒絶済み\)のいずれかになります。

![Promise&#x306E;&#x5BA3;&#x8A00;&#x3068;&#x904B;&#x547D;](https://raw.githubusercontent.com/basarat/typescript-book/master/images/promise%20states%20and%20fates.png)

Promiseの作り方を見てみましょう。Promise\(Promiseのコンストラクタ\)に対して`new`を呼び出すだけです。Promiseのコンストラクタには、Promiseの状態を決めるための`resolve`関数と`reject`関数が渡されます。

```typescript
const promise = new Promise((resolve, reject) => {
    // resolve / reject 関数がPromiseの運命を決定します
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
    // これは呼び出されません
});
```

```typescript
const promise = new Promise((resolve, reject) => {
    reject(new Error("何かひどいことが起きた"));
});
promise.then((res) => {
    // これは呼び出されません
});
promise.catch((err) => {
    console.log('I get called:', err.message); // I get called: '何かひどいことが起きた'
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
        return Promise.resolve(123); // resolveされたPromiseを返しています
    })
    .then((res) => {
        console.log(res); // 123 : resolveされた値で`then`が呼び出されます
        return 123;
    })
```

* チェーンの前の部分のエラー処理を単一の`catch`に集約することができます：

```typescript
// rejectされたPromiseを作成する
Promise.reject(new Error('何か悪いことが起きた'))
    .then((res) => {
        console.log(res); // 呼び出されない
        return 456;
    })
    .then((res) => {
        console.log(res); // 呼び出されない
        return 123;
    })
    .then((res) => {
        console.log(res); // 呼び出されない
        return 123;
    })
    .catch((err) => {
        console.log(err.message); // 何か悪いことが起きた
    });
```

* `catch`は実のところ新しいPromiseを返します\(要するに新しいPromiseのチェーンを作成します\)：

```typescript
// rejectされたPromiseを作成する
Promise.reject(new Error('何か悪いことが起きた'))
    .then((res) => {
        console.log(res); // 呼び出されない
        return 456;
    })
    .catch((err) => {
        console.log(err.message); // 何か悪いことが起きた
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
        throw new Error('何か悪いことが起きた'); // 同期処理でエラーを発生させる
        return 456;
    })
    .then((res) => {
        console.log(res); // 呼び出されない
        return Promise.resolve(789);
    })
    .catch((err) => {
        console.log(err.message); // 何か悪いことが起きた
    })
```

* エラーが発生すると関係している\(後方で最も近い\)`catch`だけがコールされます\(同時にcatchが新しい`Promise`のチェーンを作ります\)。

```typescript
Promise.resolve(123)
    .then((res) => {
        throw new Error('何か悪いことが起きた'); // 同期処理でエラーを発生させる
        return 456;
    })
    .catch((err) => {
        console.log('first catch: ' + err.message); // 何か悪いことが起きた
        return 123;
    })
    .then((res) => {
        console.log(res); // 123
        return Promise.resolve(789);
    })
    .catch((err) => {
        console.log('second catch: ' + err.message); // 呼び出されない
    })
```

* `catch`はチェーンの前部分でエラーが発生した場合にのみコールされます：

```typescript
Promise.resolve(123)
    .then((res) => {
        return 456;
    })
    .catch((err) => {
        console.log("HERE"); // 呼び出されない
    })
```

Promiseチェーンに関する事実：

* エラーが起きた場合、後続の`catch`にジャンプします\(そして途中の`then`はスキップします\)
* 同期処理のエラーについても同様に、最も近い後続の`catch`で捕捉されます

Promiseは、単なるコールバックに比べて優れたエラー処理を可能にする非同期プログラミングのパラダイムを我々に提供してくれます。さらに下記に詳しく記載します。

### TypeScriptとPromise

TypeScriptが素晴らしい点は、それがPromiseチェーンを通じて流れる値を理解してくれることです。

```typescript
Promise.resolve(123)
    .then((res) => {
         // res は `number` 型と推論される
         return true;
    })
    .then((res) => {
        // res は `boolean` 型と推論される

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
        // res は `number` 型と推論される
        return iReturnPromiseAfter1Second(); // `Promise<string>`を返す
    })
    .then((res) => {
        // res は `string` 型と推論される
        console.log(res); // Hello world!
    });
```

### コールバック関数からPromiseを返すように変更する

関数呼び出しをPromiseに包んで、下記のようにしてみましょう。

* エラーが発生した場合は `reject`を呼出す
* すべてうまく行った場合は`resolve`を呼び出す

例えば`fs.readFile`をPromiseで囲んでみましょう：

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
    return readFileAsync(filename) // 直前に作成した関数を使います
                .then(function (res) {
                    return JSON.parse(res);
                });
}
```

使い方\(このセクションの始めに紹介した同期処理のコードとの違いに注目してください🌹\)：

```typescript
// 正しいjsonファイル
loadJSONAsync('good.json')
    .then(function (val) { console.log(val); })
    .catch(function (err) {
        console.log('good.json error', err.message); // 呼び出されない
    })

// 存在しないjsonファイル
    .then(function () {
        return loadJSONAsync('absent.json');
    })
    .then(function (val) { console.log(val); }) // 呼び出されない
    .catch(function (err) {
        console.log('absent.json error', err.message);
    })

// 正しくないjsonファイル
    .then(function () {
        return loadJSONAsync('invalid.json');
    })
    .then(function (val) { console.log(val); }) // 呼び出されない
    .catch(function (err) {
        console.log('bad.json error', err.message);
    });
```

この関数がよりシンプルになった理由は、"`loadFile`\(async\)+`JSON.parse`\(sync\)=&gt;`catch`"の連結をPromiseチェーンによって行ったためです。また、コールバックは我々ではなくPromiseチェーンによって呼び出されるので、コールバックを`try/catch`で囲んでしまう誤りが起きる可能性はありませんでした。

### 並列制御フロー\(Parallel control flow\)

私たちは、Promiseを使って非同期タスクの順次処理（シーケンシャル処理）を行うことがいかに簡単かを見てきました。単に`then`の呼び出しを連結するだけなのです。

しかし、複数の非同期処理を実行し、すべてのタスクが終わったタイミングで何らかの処理を行いたいケースがあるかもしれません。`Promise`は静的な`Promise.all`関数を提供します。この関数は、`n`個のPromiseがすべて完了するまで待つことができます。`n`個のPromiseの配列を渡すと、`n`個の解決された値の配列を返します。以下では、Promiseチェーンの例と合わせて並列で処理する例を示します。

```typescript
// 何らかのデータをサーバから読み込むことを再現する処理
function loadItem(id: number): Promise<{ id: number }> {
    return new Promise((resolve) => {
        console.log('loading item', id);
        setTimeout(() => { // サーバーからのレスポンス遅延を再現
            resolve({ id: id });
        }, 1000);
    });
}

// Promiseチェーン
let item1, item2;
loadItem(1)
    .then((res) => {
        item1 = res;
        return loadItem(2);
    })
    .then((res) => {
        item2 = res;
        console.log('done');
    }); // 全体で 2秒 かかる

// 並列処理
Promise.all([loadItem(1), loadItem(2)])
    .then((res) => {
        [item1, item2] = res;
        console.log('done');
    }); // 全体で 1秒 かかる
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
  // 両方ともresolveされるが、task1の方が早く終わる
});
```

### コールバック関数をPromiseに変換する

これを行うために信頼性が高い方法は、自分でコードを書くことです。例えば`setTimeout`をPromiseを使った`delay`関数に変換するのは非常に簡単です：

```typescript
const delay = (ms: number) => new Promise(res => setTimeout(res, ms));
```

NodeJSにはこれを行う便利で使いやすい関数があることを知っておいてください。これは `コールバックスタイルの関数 => Promiseを返す関数` に変える魔法をかけてくれます。

```typescript
/** 利用例 */
import fs = require('fs');
import util = require('util');
const readFile = util.promisify(fs.readFile);
```

