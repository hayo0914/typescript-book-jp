### テンプレート文字列
構文的には、単一引用符（ '）または二重引用符（ "）の代わりにバッククォート（すなわち、\`）を使用する文字列です。

* 文字列の補間
* 複数行の文字列
* タグ付きテンプレート

#### 文字列の補間
別の一般的な使用例は、いくつかの静的な文字列+いくつかの変数からいくつかの文字列を生成したいときです。このためには*テンプレートロジック*が必要です。これはテンプレート文字列*の名前を取得する場所です。以前はHTML文字列を生成する可能性があります：

```ts
var lyrics = 'Never gonna give you up';
var html = '<div>' + lyrics + '</div>';
```
テンプレート文字列を使用すると、次のことができます。

```ts
var lyrics = 'Never gonna give you up';
var html = `<div>${lyrics}</div>`;
```

補間（ `$ {`と `}`）内の任意のプレースホルダは、JavaScript式として扱われ、評価されます。あなたは空想の数学をすることができます。

```ts
console.log(`1 and 1 make ${1 + 1}`);
```

#### 複数の文字列
JavaScriptの文字列に改行を入れたかったのですか？おそらく、あなたはいくつかの歌詞を埋め込むことを望んでいたでしょうか？あなたは*好きなエスケープ文字 `\`を使ってリテラル改行*をエスケープし、次の行で文字列に新しい行を手動で `\ n`する必要がありました。これを以下に示します。

```ts
var lyrics = "Never gonna give you up \
\nNever gonna let you down";
```

TypeScriptではテンプレート文字列を使うことができます：

```ts
var lyrics = `Never gonna give you up
Never gonna let you down`;
```

#### タグ付きテンプレート

テンプレート文字列の前に関数（ `tag`と呼ばれる）を置くことができ、テンプレート文字列リテラルとすべてのプレースホルダー式の値を前処理して結果を返す機会を得ます。いくつかのメモ：
* すべての静的リテラルは、最初の引数の配列として渡されます。
* プレースホルダ式のすべての値は、残りの引数として渡されます。最も一般的には、残りのパラメータを使用してこれらを配列に変換するだけです。

ここでは、すべてのプレースホルダからhtmlをエスケープするタグ関数（htmlEscapeという名前）がある例を示します。

```ts
var say = "a bird in hand > two in the bush";
var html = htmlEscape `<div> I would just like to say : ${say}</div>`;

// a sample tag function
function htmlEscape(literals, ...placeholders) {
    let result = "";

    // interleave the literals with the placeholders
    for (let i = 0; i < placeholders.length; i++) {
        result += literals[i];
        result += placeholders[i]
            .replace(/&/g, '&amp;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
    }

    // add the last literal
    result += literals[literals.length - 1];
    return result;
}
```

#### 生成されたJS
ES6以前のコンパイルの場合、コードはかなりシンプルです。複数行の文字列はエスケープ文字列になります。文字列補間は*文字列連結*になります。タグ付きテンプレートは関数呼び出しになります。

#### 要約
複数行の文字列と文字列の補間は、あらゆる言語で使用するのに最適です。 JavaScriptでこれを使用できるようになりました（TypeScriptに感謝します）。タグ付きテンプレートを使用すると、強力な文字列ユーティリティを作成できます。
