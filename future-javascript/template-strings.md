# テンプレートリテラル

構文的には、シングルクォート\('\)またはダブルクォート\("\)の代わりにバッククォート\(\`\)を使う文字列です。テンプレートリテラルを使う理由は、3つに分かれます:

* 文字列展開\(String Interpolation\)
* 複数行の文字列
* タグ付きテンプレート

## 文字列展開\(String Interpolation\)

一般的なユースケースは、静的な文字列と変数を組み合わせて何らかの文字列を生成することです。このために何かしらのテンプレートロジック\( `templating logic` \)が必要です。これはテンプレート文字列\( `template strings` \)の由来になったものです。これらは、公式にテンプレートリテラル\( `template literals` \)という名前に変更されました。下記は、今まであなたがhtmlを生成する時に使っていたかもしれない方法です。

```typescript
var lyrics = '絶対にあきらめない';
var html = '<div>' + lyrics + '</div>';
```

テンプレートリテラルを使用すると、次のようにできます。

```typescript
var lyrics = '絶対にあきらめない';
var html = `<div>${lyrics}</div>`;
```

補間\(`${`と`}`\)の内側のプレースホルダは、JavaScriptの式として評価される点に注目してください。例えば、何らかの計算をすることができます。

```typescript
console.log(`1 and 1 make ${1 + 1}`);
```

## 複数行文字列\(Multiline Strings\)

JavaScriptの文字列に改行を入れたくなったことはありませんか?おそらく、あなたは何かの歌詞を埋め込みたかったのでは？あなたは大好きなエスケープ文字`\`を使ってリテラルの改行をエスケープする必要があったでしょう。そして、次の行で文字列に新しい行`\ n`を手動で入力する必要がありました。これを以下に示します:

```typescript
var lyrics = "絶対にあきらめない \
\n絶対にがっかりさせない";
```

TypeScriptでは単にテンプレートリテラルを利用すれば同じことができます。

```typescript
var lyrics = `絶対にあきらめない
絶対にがっかりさせない`;
```

## タグ付きテンプレート

テンプレートリテラルの前にタグ\(`tag`\)と呼ばれる関数を置き、テンプレートリテラルとすべてのプレースホルダの値を前処理することが可能です。

メモ：

* すべての静的なリテラルは、最初の引数に配列として渡されます。
* プレースホルダのすべての値は、残りの引数として渡されます。一般的には、単に可変長引数\(Rest パラメータ\)を使用してこれらを配列に変換します。

ここでは、すべてのプレースホルダからhtmlをエスケープするタグ関数\(`htmlEscape`\)の例を示します:

```typescript
var say = "手の中にある一羽 > ヤブの中の二羽";
var html = htmlEscape `<div> 私はこのように言いたい : ${say}</div>`;

// タグ関数の例
function htmlEscape(literals: TemplateStringsArray, ...placeholders: string[]) {
    let result = "";

    // プレースホルダをリテラルに埋め込む
    for (let i = 0; i < placeholders.length; i++) {
        result += literals[i];
        result += placeholders[i]
            .replace(/&/g, '&amp;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
    }

    // 最後のリテラルを追加する
    result += literals[literals.length - 1];
    return result;
}
```

> 補足: `placeholders`は、任意の型の`[]`として型指定することができます。どの型を指定したにせよ、TypeScriptは型チェックを行って、タグを呼び出すときに渡されたplaceholdersが指定された型と一致することを確かめます。たとえば、`string`か`number`の配列を期待する場合、`...placeholders:(string | number)[]`と型を指定することができます。

## 生成されるJavaScript

ES6未満をターゲットにしてコンパイルする場合、コードはかなりシンプルです。複数行の文字列は改行がエスケープされた文字列になります。テンプレートリテラルは単なる文字列の結合処理になります。タグ付きテンプレートは関数の呼び出しになります。

## まとめ

複数行の文字列とテンプレートリテラルは、あらゆる言語において素晴らしいものです。JavaScriptでこれを使用できることは素晴らしいことです\(ありがとう、TypeScript!\)。さらに、タグ付きテンプレートを使って、強力な文字列ユーティリティを作成できます。

