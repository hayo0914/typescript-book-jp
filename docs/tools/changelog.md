## 変更
> プロジェクトの進捗状況を示すマークダウンファイルを読むことは、コミットログを読むより簡単です。

コミットメッセージからの自動変更ログの生成は、今日はかなり一般的なパターンです。 [Convention-changelog](https://github.com/conventional-changelog/conventional-changelog)というプロジェクトがあり、* convention *に続くコミットメッセージから変更履歴を生成します。

### コミットメッセージのコンベンション
もっとも一般的なのは、* angular * commitメッセージの規約です(https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#-git-commit-guidelines)。

### セットアップ
* インストール：

```bash
npm install standard-version -D
```

* あなたの `package.json`に`script`ターゲットを追加してください：

```js
{
  "scripts": {
    "release": "standard-version"
  }
}
```

* オプション：新しい* git commitとtag *を自動的にプッシュして、npmにパブリッシュして `postrelease`スクリプトを追加します：

```js
{
  "scripts": {
    "release": "standard-version",
    "postrelease": "git push --follow-tags origin master && npm publish"
  }
}
```

### リリース

単に実行する：

```bash
npm run release
```

コミットメッセージ `major`に基づいて|マイナーチェンジ`patch`が自動的に決定されます。 *明示的にバージョンを指定するには、例えば--release-asを指定することができます：

```bash
npm run release -- --release-as minor
```
