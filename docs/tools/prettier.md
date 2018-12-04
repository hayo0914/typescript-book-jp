# かわいい

Prettierは、コードフォーマットを非常に簡単にして、言及する価値があるようにする、Facebookの優れたツールです。推奨されるプロジェクトセットを使用してTypeScriptをセットアップするのは簡単です：

## セットアップ

* `npm install prettier -D`
* `scripts 'を`package.json`に追加します：

```
    "prettier:base": "prettier --parser typescript --single-quote",
    "prettier:check": "npm run prettier:base -- --list-different \"src/**/*.{ts,tsx}\"",
    "prettier:write": "npm run prettier:base -- --write \"src/**/*.{ts,tsx}\""
```

## 使用法
あなたのビルドサーバーで：
* `npmはもっときれいに走る：check`

dev（またはプリコミットフック）中：
* `npmはもっときれいになる：write`
