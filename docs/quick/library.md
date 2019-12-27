## TypeScriptのnode moduleを作成する

* [Typecriptのnodemoduleの作成に関するレッスン](https://egghead.io/lessons/typescript-create-high-quality-npm-packages-using-typescript)

TypeScriptで書かれたモジュールを使用することは、コンパイル時の安全性とオートコンプリートが得られるので、非常に楽しいことです。

TypeScript modules can be consumed both in the nodejs (as is) browser (with something like webpack).

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

* `src/index.ts`: Here you would export anything you expect to be consumed from your project. E.g `export { Foo } from './foo';`. Exporting from this file makes it available for consumption when someone does `import { /* Here */ } from 'example';`

* `tsconfig.json`について
  * `compilerOptions`に`"outDir": "lib"`と、`"declaration": true`と`"declarationMap" : true`を設定します < これはlibフォルダに`.js` (JavaScript) `.d.ts` (declarations for TypeSafety) and `.d.ts.map` (enables `declaration .d.ts` => `source .ts` IDE navigation)生成します
  * `include: ["src"]`を設定します < これは`src`ディレクトリからのすべてのファイルを対象に含めます

* `package.json`について
  * `"main": "lib/index"` <これはNode.jsに`lib/index.js`をロードするように指示します
  * `"types": "lib/index"` <これはTypeScriptに`lib/index.d.ts`をロードするように指示します


パッケージの例：
* `npm install typestyle` [for TypeStyle](https://www.npmjs.com/package/typestyle)
* 使用法：`import { style } from 'typestyle';`は、完全な型安全性を提供します

### Managing Dependencies

#### devDependencies

* If your package depends on another package while you are developing it (e.g. `prettier`) you should install them as a `devDependency`. This way they will not pollute the `node_modules` of your module's consumers (as `npm i foo` does not install `devDependencies` of `foo`).
* `typescript` is normally a `devDependency` as you only use it to build your package. The consumers can use your package with or without TypeScript.
* If your package depends on other JavaScript authored packages and you want to use it with type safety in your project, put their types (e.g. `@types/foo`) in `devDependencies`. JavaScript types should be managed *out of bound* from the main NPM streams. The JavaScript ecosystem breaks types without semantic versioning too commonly, so if your users need types for these they should install the `@types/foo` version that works for them. If you want to guide users to install these types you can put them in `peerDependencies` mentioned next.

#### peerDependencies

If your package depends on a package that it heavily *works with* (as opposed to *works using*) e.g. `react`, put them in `peerDependencies` just like you would with raw JS packages. To test them locally you should also put them in `devDependencies`.

Now:
* When you are developing the package you will get the version of the dependency you specified in your `devDependencies`.
* When someone installs your package they will *not* get this dependency (as `npm i foo` does not install `devDependencies` of `foo`) but they will get a warning that they should install the missing `peerDependencies` of your package.

#### dependencies

If your package *wraps* another package (meant for internal use even after compilation) you should put them in `dependencies`. Now when someone installs your package they will get your package + any of its dependencies.
