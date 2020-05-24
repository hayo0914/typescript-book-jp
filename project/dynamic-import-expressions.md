# 動的インポート

**動的インポート式**は新しい機能であり、**ECMAScript**の一部で、ユーザーはプログラムの任意の時点でモジュールを非同期に要求できます。 **TC39**\(JavaScript committee\)が、その提案を行っており、ステージ3の段階にあります。それは、[import\(\) proposal for JavaScript](https://github.com/tc39/proposal-dynamic-import)と呼ばれています。

また、**webpack**バンドラにはバンドルを分割することができる[**Code Splitting**](https://webpack.js.org/guides/code-splitting/)という機能があります。それは、コードをチャンクに分割し、後で非同期にダウンロードされるようにすることができます。たとえば、これにより、最小の起動用のバンドルを最初に提供し、後で追加の機能を非同期にロードすることができます。

私たちの開発ワークフローでwebpackを使用している場合、[TypeScript 2.4 dynamic import expressions](https://github.com/Microsoft/TypeScript/wiki/What%27s-new-in-TypeScript#dynamic-import-expressions)は**自動的に**チャンク化されたバンドルを生成し、最終的なJSバンドルを自動的に分割します。しかし、**tsconfig.jsonの設定**に依存しているので、それはそう簡単ではありません。

webpackのコード分割では、この目標を達成するための2つの同様なテクニックをサポートしています: **import\(\)**\(ECMAScriptの推奨\)と**require.ensure\(\)**\(従来から存在するwebpack固有の方法\)です。そして、それが意味するのは、TypeScriptにおいて**import\(\)文**を他の何かにトランスパイルするのではなく、そのままの形で出力することです。

webpack + TypeScript 2.4の設定方法の例を見てみましょう。

次のコードでは、ライブラリの _**moment**_ の遅延ロードとコード分割を行いたいと考えています。つまり、momentライブラリを別のJSチャンク\(JavaScript file\)に分けて、必要なときにロードされるようにします。

```typescript
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

```javascript
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

**重要なメモ**：

* **"module":"esnext"** を使うとTypeScriptは、Webpackコード分割のために入力する見せかけのimport\(\)文を生成します。
* さらに詳しい情報については、この記事を読んでください：[Dynamic Import Expressions and webpack 2 Code Splitting integration with TypeScript 2.4](https://blog.josequinto.com/2017/06/29/dynamic-import-expressions-and-webpack-code-splitting-integration-with-typescript-2-4/)

完全な例は[ここ](https://cdn.rawgit.com/basarat/typescript-book/705e4496/code/dynamic-import-expressions/dynamicImportExpression.js)で見ることができます。

