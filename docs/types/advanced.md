



# 関数

## オプション
`?`アノテーションは、メンバがオプションであることを示すために、関数の引数またはインターフェースのメンバの前に使用できます。つまり、あなたが望むならそれを提供することができます(そしてそれはタイプチェックされます)。しかし、それが省略されていれば* okay *です。これは次の例に示されています。

## 特殊化されたパラメータ

## 関数のオーバーロード
JavaScriptランタイムは、関数オーバーロードの実行時サポートを持っていません。スコープ内の指定された名前には、単一の関数本体のみが存在します。しかし、人々はJavaScriptの非常に動的な性質を利用して関数のオーバーロードをサポートしています。ゲッターとセッター：

```ts
var _value;
function getOrSet(value) {
    if (value === undefined) {
        return _value;
    } else {
        _value = value;
    }
}

getOrSet(1); // set : 1
console.log(getOrSet()); // get : 1
```

このような実装は、関数の実装の前に関数のシグネチャを提供することによって、TypeScriptの型システムによって取得できます。

```ts
var _value;
function getOrSet(): number;
function getOrSet(value: number);
function getOrSet(value?: number) {
    if (value === undefined) {
        return _value;
    } else {
        _value = value;
    }
}

getOrSet(1); // set : 1
console.log(getOrSet()); // get : 1
```

関数のオーバーロードをこのように定義すると、最後のシグネチャは実際にはコール可能ではないことに注意してください*。しかし、機能の実装者が彼の過負荷署名の結果を認識するのを助けるために、それを提供しなければなりません。たとえば、次の例では、 `function callMe(v1?: any, v2?: any): any`という署名を持つ関数は公開されていません。

```ts
function callMe(): number;
function callMe(v1: number);
function callMe(v1: string, v2: number);
function callMe(v1?: any, v2?: any): any {
    // Implementation body goes here
}

// Allowed calls
callMe();
callMe(1);
callMe('jenny', 5309);

// COMPILER ERROR: invalid calls
callMe('jenny');
callMe('jenny', '5309');
```

ヒント：共用体の型と関数のオーバーロードには若干の重複があることに注意してください。 2つの関数シグネチャが異なる型を持つ単一のパラメータによって異なる場合は、オーバーロードシグネチャを作成する代わりに、そのパラメータにユニオン型を使用するだけです。


# インターフェース

インターフェースはTypeScriptで多くのパワーを持っています。これは、それらのすべての複雑さを捉えるように設計されているからです。




# アンビエント宣言

以前は、なぜTypeScript？*というセクションのアンビエント宣言について簡単に見てきました。 TypeScriptの主要な設計目標の1つは、既存のJavaScriptライブラリを簡単に使用できるようにすることです。 * ambient宣言*を使用して、既存のJavaScriptの型情報を宣言することができます。あなたは `declare`キーワードを使って周囲のものを宣言します。実際、これは、ブラウザ環境(例えば `window`、`document`など)でデフォルトで利用できるたくさんのものが `lib.d.ts`というファイルでどのように宣言されているかです


注：[DefinitelyTyped](https://github.com/borisyankov/DefinitelyTyped)には、最も人気のあるJavaScriptライブラリのほぼ90％のタイプ定義が[たくさんの開発者](https://github.com)から寄せられています/ borisyankov / DefinitelyTyped /グラフ/投稿者)。



### lib.d.ts

# インターフェース



### プリミティブ型のインターフェース

### 配列のインターフェース

## 型エイリアス

## 連合の種類
構成オブジェクトに必要

## 型推論
* あなたのコードを明示的にタイプする必要がないように、*可能な限り*推論しようとします。

## 機能シグネチャ

スペシャライズド

## 型アサーション

AがBのサブタイプである場合、またはBはAのサブタイプです。








[インターフェースについての詳細]
構造的にはより多くの情報は大丈夫ですが、情報が少なくてもエラーです。ダックタイピングは、言語デザインの深いところまで焼き付けられています。
オープンエンド
タイプの互換性
