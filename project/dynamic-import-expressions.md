# 動的インポート

**動的インポート**は新しい機能であり、**ECMAScript**の一部で、ユーザーはプログラムの任意の時点でモジュールを非同期にロードできます。 **TC39**\(JavaScript committee\)が、その提案（[import\(\) proposal for JavaScript](https://github.com/tc39/proposal-dynamic-import)）を行っており、ステージ3の段階にあります。

また、**webpack**バンドラにはバンドルを分割することができる[**Code Splitting**](https://webpack.js.org/guides/code-splitting/)という機能があります。それは、コードをチャンクファイルに分割し、後で非同期にダウンロードされるようにすることができます。たとえば、これにより、最小の起動用のバンドルを最初に提供し、後で追加の機能を非同期にロードすることができます。

私たちの開発ワークフローでwebpackを使用している場合、[TypeScript 2.4 dynamic import expressions](https://github.com/Microsoft/TypeScript/wiki/What%27s-new-in-TypeScript#dynamic-import-expressions)は**自動的に**チャンク化されたバンドルを生成し、最終的なJavaScriptバンドルを自動的に分割します。しかし、これは**tsconfig.jsonの設定**に依存しているので、そう簡単ではありません。

重要なことは、webpackのコード分割機能は、この目標を実現するための 2 つのやり方をサポートしているということです:  **import\(\)**\(ECMAScriptの推奨\)または、**require.ensure\(\)**\(従来から存在するwebpack固有の方法\)がサポートされています。これが意味することは、TypeScriptにおいては、**import\(\)文**を他の何らかの構文にトランスパイルするのではなく、そのままの形で出力しなければならない、ということです。

webpack + TypeScript 2.4の設定方法の例を見てみましょう。

次のコードは _**moment**_ ライブラリを遅延ロードしようとしているコードです。しかし、それだけではなく、コード分割もしたいと思っています。つまり、momentライブラリを別のJavaScriptのチャンクファイルに分割して、必要なときだけロードされるようにしたい、ということです。このコメント`/* webpackChunkName: "momentjs" */`を`import`文に追加して、webpackのチャンク名を明示的に伝えることができます。

```typescript
import(/* webpackChunkName: "momentjs" */ "moment")
  .then((moment) => {
      // 遅延ロードされるモジュールでも、型が有効であり、自動補完や、型チェックが機能します \o/
      const time = moment().format();
      console.log("TypeScript >= 2.4.0 動的インポートがサポートされています:");
      console.log(time);
  })
  .catch((err) => {
      console.log("momentのロードに失敗しました", err);
  });
```

tsconfig.jsonは次のようになります：

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

**重要**：

* **"module":"esnext"** を使うとTypeScriptは、Webpackコード分割に利用する見せかけのimport\(\)文を生成します
* さらに詳しい情報については、この記事を読んでください：[Dynamic Import Expressions and webpack 2 Code Splitting integration with TypeScript 2.4](https://blog.josequinto.com/2017/06/29/dynamic-import-expressions-and-webpack-code-splitting-integration-with-typescript-2-4/)

完全な例は[ここ](https://cdn.rawgit.com/basarat/typescript-book/705e4496/code/dynamic-import-expressions/dynamicImportExpression.js)で見ることができます。

