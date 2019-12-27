## TypeScriptのnode moduleを作成する

* [Typecriptのnodemoduleの作成に関するレッスン](https://egghead.io/lessons/typescript-create-high-quality-npm-packages-using-typescript)

TypeScriptで書かれたモジュールを使用することは、コンパイル時の安全性とオートコンプリートが得られるので、非常に楽しいことです。

TypeScriptのモジュールは、Node.jsではそのまま使用でき、ブラウザでもWebpackなどを使うことで利用できるようになります。

高品質のTypeScriptモジュールの作成は簡単です。以下の望ましいフォルダ構造を仮定します。

```text
package
├─ package.json
├─ tsconfig.json
├─ src
│  ├─ index.ts
│  ├─ foo.ts
│  └─ ...All your source files (Authored)
└─ lib
  ├─ index.d.ts.map
  ├─ index.d.ts
  ├─ index.js
  ├─ foo.d.ts.map
  ├─ foo.d.ts
  ├─ foo.js
  └─ ... All your compiled files (Generated)
```

* `src/index.ts`: ここでは、他のプロジェクトから使用できるようにしたいすべてのものをexportします。たとえば、`export { Foo } from './foo';`などを書きます。このファイルからexportしたオブジェクトは、このライブラリを使用する他の人が `import { /* Here */ } from 'example';` のように書いてimportすることができるようになります。

* `tsconfig.json`について
  * `compilerOptions`に`"outDir": "lib"`と、`"declaration": true`と`"declarationMap" : true`を設定します < これは、libフォルダに`.js` (JavaScript)と`.d.ts` (型安全性のための型宣言)と`.d.ts.map` (このファイルは、IDE上で`declaration .d.ts` => `source .ts`というナビゲーションを可能にします)が生成されます
  * `include: ["src"]`を設定します < これは`src`ディレクトリからのすべてのファイルを対象に含めます

* `package.json`について
  * `"main": "lib/index"` < これはNode.jsに`lib/index.js`をロードするように指示します
  * `"types": "lib/index"` < これはTypeScriptに`lib/index.d.ts`をロードするように指示します


パッケージの例：
* `npm install typestyle` [for TypeStyle](https://www.npmjs.com/package/typestyle)
* 使用法：`import { style } from 'typestyle';`は、完全な型安全性を提供します

### Dependenciesの管理

#### devDependencies

* パッケージの開発中にのみ他のパッケージに依存している場合(例: `prettier`)、依存するパッケージは`devDependency`に追加します。こうすることで、あなたのパッケージを使用するユーザーの`node_modules`には開発用の依存パッケージをインストールしないようにできます(`npm i foo`というコマンドを実行した場合には、`foo`のdevDependencies`はインストールされないためです)。
*`typescript`は通常パッケージのビルド時にのみ使用されるため、`devDependency`に追加します。パッケージのユーザーはTypeScriptなしでもあなたのパッケージを利用できます。
* あなたのパッケージがJavaScriptで作られた他のパッケージに依存していて、あなたのプロジェクトでは型安全性を活用したい場合には、依存しているパッケージの型パッケージ(例: `@types/foo`)を`devDependencies`に追加してください。JavaScriptの型は、メインのNPMエコシステムの*外側で*管理されています。JavaScriptエコシステムでは、セマンティックバージョニングを使用していない場合には特に、型が破壊されるのは日常茶飯事です。そのため、ユーザーが型を使用したい場合には、自分でパッケージに適したバージョンの型`@types/foo`をインストールする必要があります。型パッケージをインストールするようにユーザーに支持したい場合には、次のセクションに示すように、パッケージを`peerDependencies`に追加します。

#### peerDependencies

あなたのパッケージが依存するパッケージで、(*インストールしないと動作しない*というわけではなく)同時にインストールしたときに*よりよく動作する*というようなパッケージがある場合には、生のJSパッケージでするのと同じように、そのパッケージを`peerDependencies`に追加してください(たとえば、`react`など)。ローカルでテストする場合にも、`devDependencies`に追加する必要があります。

このように設定を行うことで、次のように動作するようになります。
* パッケーの開発中は、`devDependencies`で指定したバージョンのパッケージがインストールされます。
* 他のユーザーがあなたのパッケージをインストールした場合には、`devDependencies`で指定されたパッケージはインストール*されません*が、あなたのパッケージの`peerDependencies`に指定されているパッケージが存在しない場合には、ユーザーにそのパッケージをインストールするべきであるという警告が表示されます。

#### dependencies

あなたのパッケージが他のパッケージの*ラッパー*である場合(つまり、TypeScriptのコンパイル後にも内部で他のライブラリを使用する場合)には、そのパッケージは`dependencies`に追加しなければなりません。そうすることで、あなたのパッケージをインストールしたユーザーはあなたのパッケージに加えて、その依存パッケージを同時にインストールできるようになります。
