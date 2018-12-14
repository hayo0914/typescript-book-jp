## ステートフル関数(Stateful Functions)
他のプログラミング言語の共通の特徴は、`static`キーワードの使って関数内の変数の生存時間(スコープではない)を増加させ、関数の呼び出しをまたがって生かすことです。これを実現する `C`サンプルがあります：

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

JavaScript(またはTypeScript)には関数の静的変数がないため、ローカル変数をラップする、さまざまな抽象化を使用して同じことを達成できます。 `class`を使った例：

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

> C++デベロッパーはまた、`functor`(演算子`()`をオーバーライドするクラス)というパターンを使ってこれを達成しています。
