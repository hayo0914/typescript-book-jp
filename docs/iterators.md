### イテレータ(Iterators)

イテレータ自体はTypeScriptまたはES6の機能ではなく、オブジェクト指向プログラミング言語において一般的な、振る舞いに関するデザインパターン(Behavioral Design Pattern)です。これは、一般に次のインタフェースを実装するオブジェクトです。

```ts
interface Iterator<T> {
    next(value?: any): IteratorResult<T>;
    return?(value?: any): IteratorResult<T>;
    throw?(e?: any): IteratorResult<T>;
}
```
([`<T>`記法についてはのちに説明します](./types/generics.html))  
このインタフェースは、コレクションまたはシーケンスのオブジェクトに属する値を取得することを可能にします。

`IteratorResult`は単なる`value`+`done`のペアです：
```ts
interface IteratorResult<T> {
    done: boolean;
    value: T;
}
```

何らかのフレームのようなオブジェクトがあるとしましょう。このフレームは、コンポーネントのリストで構成されています。イテレータのインターフェースは、フレームオブジェクトのコンポーネントを次のように取得することを可能にします。

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

繰り返しになりますが、イテレータ自体はTypeScriptの機能ではありません。このコードは`Iterator`と`IteratorResult`のインターフェースを明示的に実装しなくても動作します。しかしながら、ES6の[インターフェース](./types/interfaces.md)を使うことはコードの一貫性を保つ上で非常に便利です。

それはOK、良いことです。しかし、さらに役立つことがあるかもしれません。ES6はイテラブルプロトコル(iterable protocol)を定義しています。それを実装する場合は、[Symbol.iterator]シンボル(`symbol`)を含みます：
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

残念ながら `frame.next()`はこのパターンでは動作しません。また、見た目が少し不格好です。そこで救いになるのがIterableIteratorインターフェースです!
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
`frame.next()`と`for`ループの両方が、IterableIteratorインターフェースでうまく動作するようになりました。

イテレータが反復する対象は有限である必要はありません。典型的な例はフィボナッチ計算の処理です：
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

#### ES5で動作するイテレータを使ってコードを書く
上記のコード例はES6に対応しているJSエンジンが必要ですが、ES5をターゲットとするJSエンジンであっても、`Symbol.iterator`をサポートしている場合は、動作する可能性があります。これは、ES6 lib(es6.d.ts)をプロジェクトに追加してES5をターゲットにコンパイルすることで可能です。コンパイルされたコードは、node 4+、Google Chrome、その他のブラウザで動作するはずです。
