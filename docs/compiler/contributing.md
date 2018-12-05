## 寄稿

TypeScriptは[OSS and GitHub](https://github.com/Microsoft/TypeScript)であり、チームはコミュニティの入力を歓迎する。

### セットアップ
超簡単：

```bash
git clone https://github.com/Microsoft/TypeScript.git
cd TypeScript
npm install -g jake
npm install
```

### セットアップフォーク
明らかに、Microsoft / TypeScriptを `上流 'のリモートと独自の* fork *(GitHub * fork *ボタンを使用)を`origin`としてセットアップする必要があります。

```bash
git remote rm origin
git remote rm upstream
git remote add upstream https://github.com/Microsoft/TypeScript.git
git remote add origin https://github.com/basarat/TypeScript.git
```
さらに、私は `bas /`のようなブランチを使って、ブランチリストにクリーナーを表示させたいと思っています。

### ランニングテスト
JakeFileにはたくさんの `test`オプションと`build`オプションがあります。 `すべてのテストを`jake runtests`で実行することができます

### ベースライン
ベースラインは、TypeScriptコンパイラの* expected *出力に変更があるかどうかを管理するために使用されます。ベースラインは `テスト/ベースライン`に位置しています。

* Reference(* expected *)ベースライン： `tests / baselines / reference`
* ベースライン： `テスト/ベースライン/ローカル`(このフォルダは**。gitignore **にあります)

> これらのフォルダ間に相違がある場合、テストは失敗します。 BeyondCompareやKDiff3のようなツールで2つのフォルダを比較することができます。

生成されたファイルのこれらの変更が有効であると思うなら、 `jake baseline-accept`を使ってベースラインを受け入れます。 `参照`ベースラインへの変更はコミットできるgit diffとして表示されます。

> *すべての*テストを実行しない場合は、 `jake baseline-accept [soft]`を使用します。これは新しいファイルをコピーし、 `reference`ディレクトリ全体を削除しないことに注意してください。

### テストカテゴリ

さまざまなシナリオやさまざまなテストインフラストラクチャにもさまざまなカテゴリがあります。これらはいくつか説明されています。

#### コンパイラのテスト

これらはファイルをコンパイルすることを保証します：

* 期待どおりのエラーを生成する
* 期待通りにJSを生成
* タイプは期待どおりに識別されます
* シンボルは期待どおりに識別されます

これらの期待は、ベースラインインフラストラクチャを使用して検証されます。

##### コンパイラテストの作成
テストは `tests / cases / compiler`に新しいファイル`yourtest.ts`を追加することで作成できます。テストを実行するとすぐに、ベースラインに失敗するはずです。これらのベースラインを受け入れて(gitでそれらを表示させる)、それらがあなたが*期待しているものになるように微調整してください...今テストをパスしてください。

`jake runtests tests = compiler`を使ってこれらをすべて単独で実行するか、`jake runtests tests = compiler / yourtest`を使って新しいファイルだけを実行してください

私はしばしば `jake runtests tests = compiler / yourtest || jake baseline-accept [soft] `を実行し、`git`でdiffを取得します。

### テストのデバッグ

`jake runtests-browser tests = theNameOfYourTest`とブラウザ内のデバッグは、通常かなりうまく動作します。

### もっと
* Remoの記事：https://dev.to/remojansen/learn-how-to-contribute-to-the-typescript-compiler-on-github-through-a-real-world-example-4df0
