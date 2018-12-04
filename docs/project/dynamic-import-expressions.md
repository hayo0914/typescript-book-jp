## 動的インポート式

** 動的インポート式**は新しい機能であり、** ECMAScript **の一部で、ユーザーはプログラムの任意の時点でモジュールを非同期に要求できます。
** TC39 ** JavaScript委員会には、ステージ3にある独自の提案があり、JavaScriptの[import（）proposal for]（https://github.com/tc39/proposal-dynamic-import）と呼ばれています。

また、** webpack ** bundlerにはバンドルを分割することができる[**コード分割**]（https://webpack.js.org/guides/code-splitting/）という機能があります。後で非同期にダウンロードされます。たとえば、これにより、最小のブートストラップバンドルを最初に提供し、後で追加の機能を非同期にロードすることができます。

私たちの開発ワークフローでwebpackを使用している場合、[TypeScript 2.4動的インポート式]（https://github.com/Microsoft/TypeScript/wiki/What%27s-new-in-TypeScript#dynamic- import-expressions）は自動的に**バンドルチャンクを生成し、JS最終バンドルを自動的にコード分割します。しかし、** tsconfig.jsonの設定**に依存しているので、それはそう簡単ではありません**。

webpackのコード分割では、** import（）**（ECMAScriptの推奨）と** require.ensure（）**（従来のwebpack固有）を使用して、この目標を達成するための2つの同様の手法をサポートしています。そして、それが意味するのは、期待されるTypeScriptの出力は、** import（）ステートメントをそのまま**そのまま残すことです。

webpack + TypeScript 2.4の設定方法の例を見てみましょう。

次のコードでは、**ライブラリの_moment _ **を遅延ロードしたいと思いますが、コード分割にも興味があります。つまり、必要なときにのみロードされる別のJS（javascriptファイル） 。

```ts
import(/* webpackChunkName: "momentjs" */ "moment")
  .then((moment) => {
      // lazyModule has all of the proper types, autocomplete works,
      // type checking works, code references work \o/
      const time = moment().format();
      console.log("TypeScript >= 2.4.0 Dynamic Import Expression:");
      console.log(time);
  })
  .catch((err) => {
      console.log("Failed to load moment", err);
  });
```

ここにtsconfig.jsonがあります：

```json
{
    "compilerOptions": {
        "target": "es5",                          
        "module": "esnext",                     
        "lib": [
            "dom",
            "es5",
            "scripthost",
            "es2015.promise"
        ],                                        
        "jsx": "react",                           
        "declaration": false,                     
        "sourceMap": true,                        
        "outDir": "./dist/js",                    
        "strict": true,                           
        "moduleResolution": "node",               
        "typeRoots": [
            "./node_modules/@types"
        ],                                        
        "types": [
            "node",
            "react",
            "react-dom"
        ]                                       
    }
}
```


** 重要なメモ**：

 -  ** "module"を使う： "esnext" ** TypeScriptは、Webpackコード分割のために入力する模擬import（）文を生成します。
 - さらに詳しい情報については、この記事を読んでください：[動的インポート式とwebpack 2コード分割とTypeScript 2.4の統合]（https://blog.josequinto.com/2017/06/29/dynamic-import-expressions-and-webpack-code -splitting-integration-with-typescript-2-4 /）を使用します。


完全な例[here] [dynamicimportcode]を見ることができます。

[dynamicimportcode]：https：//cdn.rawgit.com/basarat/typescript-book/705e4496/code/dynamic-import-expressions/dynamicImportExpression.js
