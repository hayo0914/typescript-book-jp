# Prettier

Prettierは、Facebookによる優れたツールです。それは言及に値するほど、コードフォーマットを非常に簡単にします。私達が推奨するプロジェクトのセットアップを使用してTypeScriptとともに使えるようにするのは簡単です：

## セットアップ

* `npm install prettier -D`
* `scripts`を`package.json`に追加します：

```
    "prettier:base": "prettier --parser typescript --single-quote",
    "prettier:check": "npm run prettier:base -- --list-different \"src/**/*.{ts,tsx}\"",
    "prettier:write": "npm run prettier:base -- --write \"src/**/*.{ts,tsx}\""
```

## 使用法
あなたのビルドサーバーで：
* `npm run prettier:check`

開発中(またはpre commit hook)で：
* `npm run prettier:write`
