# Contributing

TypeScriptは[GitHubにあるOSS](https://github.com/Microsoft/TypeScript)であり、チームはコミュニティのインプットを歓迎します。

## セットアップ

凄く簡単です：

```bash
git clone https://github.com/Microsoft/TypeScript.git
cd TypeScript
npm install -g jake
npm install
```

## Forkのセットアップ

当然、あなたはMicrosoft/TypeScriptを`upstream`リモートとしてセットアップし、自分の_fork_\(GitHub _fork_ボタンを使用\)を`origin`としてセットアップする必要があります。

```bash
git remote rm origin
git remote rm upstream
git remote add upstream https://github.com/Microsoft/TypeScript.git
git remote add origin https://github.com/basarat/TypeScript.git
```

さらに、私は`bas/`のようなブランチを使って、ブランチリストをよりクリーンに表示させたいと思っています。

## Testの実行

JakeFileにはたくさんの`test`オプションと`build`オプションがあります。すべてのテストを`jake runtests`で実行することができます。

## ベースライン\(Baselines\)

ベースラインは、TypeScriptコンパイラの期待された出力に変更があるかどうかを管理するために使用されます。ベースラインは`test/baselines`に配置されています。

* Reference\(期待された\)ベースライン： `tests/baselines/reference`
* \(このテスト実行の中で\)生成されたベースライン： `tests/baselines/local`\(このフォルダは**.gitignore**にあります\)

> これらのフォルダ間に相違がある場合、テストは失敗します。BeyondCompareやKDiff3のようなツールで2つのフォルダを比較することができます。

生成されたファイルのこれらの変更が正しいものであるなら、`jake baseline-accept`を使ってベースラインを受け入れます。この`reference`ベースラインへの変更はコミットできるgit diffとして表示されます。

> すべてのテストを実行しない場合は、`jake baseline-accept[soft]`を使用します。これは新しいファイルをコピーするだけで、`reference`ディレクトリ全体を削除しないことに注意してください。

## テストのカテゴリ

異なるシナリオに対して異なるカテゴリがあります。そして、異なるテストインフラに対してでさえもそうです。ここではそれらのうちのいくつかを説明します。

### Compilerテスト

これらはファイルのコンパイルを確認します：

* 期待どおりのエラーを生成すること
* 期待通りのJSを生成すること
* 型が期待どおりに識別されること
* Symbolが期待どおりに識別されること

これらの期待は、ベースラインのインフラストラクチャを使用して検証されます。

#### Compilerテストの作成

テストは `tests/cases/compiler`に新しいファイル`yourtest.ts`を追加することで作成できます。テストを実行するとすぐに、ベースラインに失敗するはずです。これらのベースラインを受け入れて\(gitでそれらを表示させるために\)、それらがあなたが期待しているものになるように微調整してください...そしてテストが通るようにしてください。

`jake runtests tests = compiler`を使ってこれらをすべて単独で実行するか、`jake runtests tests=compiler/yourtest`を使って新しいファイルだけを実行してください。

私はしばしば`jake runtests tests=compiler/yourtest || jake baseline-accept[soft]`を実行し、`git`でdiffを取得します。

## テストのデバッグ

`jake runtests-browser tests=theNameOfYourTest`とブラウザ内でのデバッグは、通常、非常にうまく行きます。

## More

* Remoによる記事：[https://dev.to/remojansen/learn-how-to-contribute-to-the-typescript-compiler-on-github-through-a-real-world-example-4df0](https://dev.to/remojansen/learn-how-to-contribute-to-the-typescript-compiler-on-github-through-a-real-world-example-4df0)

