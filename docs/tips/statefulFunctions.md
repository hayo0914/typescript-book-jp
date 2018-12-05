## ステートフル関数
他のプログラミング言語の共通の特徴は、関数呼び出しの存続期間を超えて存続する関数変数の*寿命*(スコープではない*)を増やすための `static`キーワードの使用です。これを実現する `C`サンプルがあります：

```c
void called() {
    static count = 0;
    count++;
    printf("Called : %d", count);
}

int main () {
    called(); // Called : 1
    called(); // Called : 2
    return 0;
}
```

JavaScript(またはTypeScript)には関数の静的変数がないため、ローカル変数を包むさまざまな抽象化を使用して同じことを達成できます。 `class`を使って：

```ts
const {called} = new class {
    count = 0;
    called = () => {
        this.count++;
        console.log(`Called : ${this.count}`);
    }
};

called(); // Called : 1
called(); // Called : 2
```

> C ++開発者は、 `functor`(演算子`() `をオーバーライドする)というパターンを使ってこれを試してみましょう。
