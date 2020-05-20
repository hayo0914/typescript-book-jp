## Changelog
> プロジェクトの進捗状況をマークダウンで読むことは、コミットログを読むより簡単です。

コミットメッセージからのChangelog生成は、今はかなり一般的なパターンです。[Convention-changelog](https://github.com/conventional-changelog/conventional-changelog)というプロジェクトがあり、*convention*に続くコミットメッセージからChangelogを生成します。

### コミットメッセージの規約
もっとも一般的なのは、[*angular*のCommitメッセージ](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#-git-commit-guidelines)の規約です。

### セットアップ
* インストール：

```bash
npm install standard-version -D
```

* あなたの`package.json`に`script`ターゲットを追加してください：

```json
{
  "scripts": {
    "release": "standard-version"
  }
}
```

* オプション： 自動的に新しいgit commitとtagをpushして、npmにpublishする`postrelease`スクリプトを追加します:

```json
{
  "scripts": {
    "release": "standard-version",
    "postrelease": "git push --follow-tags origin master && npm publish"
  }
}
```

### リリース

単に以下を実行します：

```bash
npm run release
```

バージョンはコミットメッセージ`major`|`minor`|`patch`に基づいて自動的に決定されます。明示的にバージョンを指定したい場合は、`--release-as`を指定することができます：

```bash
npm run release -- --release-as minor
```
