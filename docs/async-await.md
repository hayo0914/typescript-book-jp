## Async Await

> [同内容をカバーするPRO eggheadのビデオコース](https://egghead.io/courses/async-await-using-typescript)

思考実験として、`await`キーワードがPromiseに対して使われたときにコードの実行を一時停止し、その関数から返されたPromiseが完了したときだけ実行が再開されるようにJavaScriptランタイムに指示する方法を考えてみましょう：

```ts
// Not actual code. A thought experiment
async function foo() {
    try {
        var val = await getMeAPromise();
        console.log(val);
    }
    catch(err) {
        console.log('Error: ', err.message);
    }
}
```

Promiseが完了したとき、次の処理を続けます
* Promiseがresolveされた場合、値が返されることを待つ
* Promiseがrejectされた場合、同期的にキャッチ可能なエラーを投げる


これは一瞬にして(そして魔法のように)非同期プログラミングを同期プログラミングと同じように簡単にします。この思考実験に必要な3つのものは次のとおりです。

* 関数実行を一時停止する能力
* 関数の内側に値を入れる能力
* 関数の内側に例外をスローする能力

これはまさにジェネレータが可能にしたことです!上記の思考実験は実際の事実です。なので、TypeScript/JavaScriptの`async`/`await`の実装も存在します。裏側の仕組みは、単にジェネレータを使っています。

### 生成されたJavaScript

これを理解する必要はありませんが、[ジェネレータ](./generators.md)のことを知っていれば、かなり簡単です。関数`foo`は次のように単純にラップされたもので実現できます：

```ts
const foo = wrapToReturnPromise(function* () {
    try {
        var val = yield getMeAPromise();
        console.log(val);
    }
    catch(err) {
        console.log('Error: ', err.message);
    }
});
```

`wrapToReturnPromise`はジェネレータ関数を実行して`generator`を取得し、`generator.next()`を使います。返却値が`promise`なら、その`promise`を`then`+`catch`し、結果に応じて、`generator.next(result)`または `generator.throw(error)`をコールします。それでおしまい!



### TypeScriptにおけるAsync Awaitのサポート
**Async - Await**は[TypeScript1.7以降](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-1-7.html)でサポートされています。非同期関数の先頭に*async*キーワードが付きます。 *await*は、非同期関数の戻り値promiseが満たされ、*Promise*からの値を取得するまで実行を中断します。
以前は、**ターゲットがES6**の場合のみサポートされていて、**ES6ジェネレータ**に直接トランスパイルしていました。

**TypeScript2.1**は、[ES3とES5のランタイムにAsync/Await機能を追加](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-2-1.html)しました。あなたが使っている環境を気にせずに利用することができます。TypeScript 2.1以降で、async/awaitを使用できることに注意することが重要です。もちろん多くのブラウザがサポートされています。もちろん、Promiseのためのpolyfillがグローバルに追加されています。

この例のコードを見て、TypeScriptのasync/await記法がどのように働くかを理解してください。
```ts
function delay(milliseconds: number, count: number): Promise<number> {
    return new Promise<number>(resolve => {
            setTimeout(() => {
                resolve(count);
            }, milliseconds);
        });
}

// async function always returns a Promise
async function dramaticWelcome(): Promise<void> {
    console.log("Hello");

    for (let i = 0; i < 5; i++) {
        // await is converting Promise<number> into number
        const count:number = await delay(500, i);
        console.log(count);
    }

    console.log("World!");
}

dramaticWelcome();
```

**ES6へのトランスパイル結果(--target es6)**
```js
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
function delay(milliseconds, count) {
    return new Promise(resolve => {
        setTimeout(() => {
            resolve(count);
        }, milliseconds);
    });
}
// async function always returns a Promise
function dramaticWelcome() {
    return __awaiter(this, void 0, void 0, function* () {
        console.log("Hello");
        for (let i = 0; i < 5; i++) {
            // await is converting Promise<number> into number
            const count = yield delay(500, i);
            console.log(count);
        }
        console.log("World!");
    });
}
dramaticWelcome();
```
完全な例を [ここ][asyncawaites6code] で見ることができます。


**ES5へのトランスパイル結果(--target es5)**
```js
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = y[op[0] & 2 ? "return" : op[0] ? "throw" : "next"]) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [0, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
function delay(milliseconds, count) {
    return new Promise(function (resolve) {
        setTimeout(function () {
            resolve(count);
        }, milliseconds);
    });
}
// async function always returns a Promise
function dramaticWelcome() {
    return __awaiter(this, void 0, void 0, function () {
        var i, count;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    console.log("Hello");
                    i = 0;
                    _a.label = 1;
                case 1:
                    if (!(i < 5)) return [3 /*break*/, 4];
                    return [4 /*yield*/, delay(500, i)];
                case 2:
                    count = _a.sent();
                    console.log(count);
                    _a.label = 3;
                case 3:
                    i++;
                    return [3 /*break*/, 1];
                case 4:
                    console.log("World!");
                    return [2 /*return*/];
            }
        });
    });
}
dramaticWelcome();
```
完全な例を [ここ][asyncawaites5code] で見ることができます。


**注意**：両方のターゲットシナリオでは、実行時にグローバルにECMAScriptに準拠したPromiseがあることを確認する必要があります。PromiseのためにPolyfillを用意する必要があるかもしれません。また、libフラグを "dom", "es2015"もしくは"dom", "es2015.promise", "es5"のように設定することで、TypeScriptがPromiseを認識していることを確認する必要があります。
**各ブラウザのPromiseサポート(ネイティブおよびPolyfill)の有無を [ここ](https://kangax.github.io/compat-table/es6/#test-Promise) で確認できます。**

[ジェネレータ]:./generators.md
[asyncawaites5code]:https://cdn.rawgit.com/basarat/typescript-book/705e4496/code/async-await/es5/asyncAwaitES5.js
[asyncawaites6code]:https://cdn.rawgit.com/basarat/typescript-book/705e4496/code/async-await/es6/asyncAwaitES6.js
