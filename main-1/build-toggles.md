# Build Toggles

実行されている場所に基づいてJavaScriptプロジェクトを切り替えるのが一般的です。環境変数に基づいたデッドコードの削除をサポートするので、webpackでこれを非常に簡単に行うことができます。

あなたの`package.json`の`scripts`に異なるターゲットを追加してください：

```javascript
"build:test": "webpack -p --config ./src/webpack.config.js",
"build:prod": "webpack -p --define process.env.NODE_ENV='\"production\"' --config ./src/webpack.config.js",
```

もちろん、あなたは`npm install webpack --save-dev`を行っていることを前提にしています。これで`npm run build:test`などを実行できます。

この変数を使うのも簡単です：

```typescript
/**
 * This interface makes sure we don't miss adding a property to both `prod` and `test`
 */
interface Config {
  someItem: string;
}

/**
 * We only export a single thing. The config.
 */
export let config: Config;

/**
 * `process.env.NODE_ENV` definition is driven from webpack
 *
 * The whole `else` block will be removed in the emitted JavaScript
 *  for a production build
 */
if (process.env.NODE_ENV === 'production') {
  config = {
    someItem: 'prod'
  }
  console.log('Running in prod');
} else {
  config = {
    someItem: 'test'
  }
  console.log('Running in test');
}
```

> 単に多くのJavaScriptライブラリ\(例:`React`\)で慣習的であることから、`process.env.NODE_ENV`を使用します。

