### イテレータ

Iterator自体はTypeScriptまたはES6の機能ではないため、Iteratorは
ビヘイビアデザインオブジェクト指向プログラミング言語に共通するパターン。
これは、一般に、次のインタフェースを実装するオブジェクトです。

```ts
interface Iterator<T> {
    next(value?: any): IteratorResult<T>;
    return?(value?: any): IteratorResult<T>;
    throw?(e?: any): IteratorResult<T>;
}
```

このインタフェースでは、コレクションまたはシーケンスから値を取得できます。
オブジェクトに属します。

`IteratorResult`は単なる`value` + `done`ペアです：
```ts
interface IteratorResult<T> {
    done: boolean;
    value: T;
}
```

いくつかのフレームのオブジェクトがあるとしましょう。
このフレームが構成するコンポーネントイテレータインタフェースを使用すると可能です
このフレームオブジェクトから以下のようなコンポーネントを取得します。

```ts
class Component {
  constructor (public name: string) {}
}

class Frame implements Iterator<Component> {

  private pointer = 0;

  constructor(public name: string, public components: Component[]) {}

  public next(): IteratorResult<Component> {
    if (this.pointer < this.components.length) {
      return {
        done: false,
        value: this.components[this.pointer++]
      }
    } else {
      return {
        done: true
      }
    }
  }

}

let frame = new Frame("Door", [new Component("top"), new Component("bottom"), new Component("left"), new Component("right")]);
let iteratorResult1 = frame.next(); //{ done: false, value: Component { name: 'top' } }
let iteratorResult2 = frame.next(); //{ done: false, value: Component { name: 'bottom' } }
let iteratorResult3 = frame.next(); //{ done: false, value: Component { name: 'left' } }
let iteratorResult4 = frame.next(); //{ done: false, value: Component { name: 'right' } }
let iteratorResult5 = frame.next(); //{ done: true }

//It is possible to access the value of iterator result via the value property:
let component = iteratorResult1.value; //Component { name: 'top' }
```
再び。 Iterator自体はTypeScriptの機能ではなく、このコードは
IteratorとIteratorResultインタフェースを明示的に実装します。
しかし、これらの共通点を使用すると非常に便利です
コード一貫性のためのES6 [interfaces]（./ types / interfaces.md）

よかったですが、もっと役立つかもしれません。 ES6は* iterableプロトコルを定義します*
Iterableインターフェースが実装されている場合は、[Symbol.iterator] `symbol`を含みます：
```ts
//...
class Frame implements Iterable<Component> {

  constructor(public name: string, public components: Component[]) {}

  [Symbol.iterator]() {
    let pointer = 0;
    let components = this.components;

    return {
      next(): IteratorResult<Component> {
        if (pointer < components.length) {
          return {
            done: false,
            value: components[pointer++]
          }
        } else {
          return {
            done: true,
            value: null
          }
        }
      }
    }
  }
}

let frame = new Frame("Door", [new Component("top"), new Component("bottom"), new Component("left"), new Component("right")]);
for (let cmp of frame) {
  console.log(cmp);
}
```

残念ながら `frame.next（）`はこのパターンでは動作しません。
少し不器用です。レスキューへのIterableIteratorインターフェイス！
```ts
//...
class Frame implements IterableIterator<Component> {

  private pointer = 0;

  constructor(public name: string, public components: Component[]) {}

  public next(): IteratorResult<Component> {
    if (this.pointer < this.components.length) {
      return {
        done: false,
        value: this.components[this.pointer++]
      }
    } else {
      return {
        done: true,
        value: null
      }
    }
  }

  [Symbol.iterator](): IterableIterator<Component> {
    return this;
  }

}
//...
```
`frame.next（）`と `for`サイクルの両方が、IterableIteratorインターフェースでうまく動作するようになりました。

反復子は有限の値を反復する必要はありません。
典型的な例はフィボナッチシーケンスです：
```ts
class Fib implements IterableIterator<number> {

  protected fn1 = 0;
  protected fn2 = 1;

  constructor(protected maxValue?: number) {}

  public next(): IteratorResult<number> {
    var current = this.fn1;
    this.fn1 = this.fn2;
    this.fn2 = current + this.fn1;
    if (this.maxValue != null && current >= this.maxValue) {
      return {
        done: true,
        value: null
      } 
    } 
    return {
      done: false,
      value: current
    }
  }

  [Symbol.iterator](): IterableIterator<number> {
    return this;
  }

}

let fib = new Fib();

fib.next() //{ done: false, value: 0 }
fib.next() //{ done: false, value: 1 }
fib.next() //{ done: false, value: 1 }
fib.next() //{ done: false, value: 2 }
fib.next() //{ done: false, value: 3 }
fib.next() //{ done: false, value: 5 }

let fibMax50 = new Fib(50);
console.log(Array.from(fibMax50)); // [ 0, 1, 1, 2, 3, 5, 8, 13, 21, 34 ]

let fibMax21 = new Fib(21);
for(let num of fibMax21) {
  console.log(num); //Prints fibonacci sequence 0 to 21
}
```

#### ES5ターゲットのイテレーターによるビルドコード
上記のコード例ではES6ターゲットが必要ですが、動作する可能性があります
ターゲットJSエンジンが `Symbol.iterator`をサポートしている場合は、ES5ターゲットも使用できます。
これは、ES5ターゲットでES6 libを使用することで実現できます
（es6.d.tsをプロジェクトに追加して）コンパイルします。
コンパイルされたコードは、ノード4+、Google Chrome、その他のブラウザで動作するはずです。
