# Typesafe Event Emitter

従来、Node.jsと伝統的なJavaScriptでは、単一のイベントエミッタがあります。このイベントエミッタは内部的に異なるイベントタイプするリスナをトラッキングします。

```typescript
const emitter = new EventEmitter();
// Emit: 
emitter.emit('foo', foo);
emitter.emit('bar', bar);
// Listen: 
emitter.on('foo', (foo)=>console.log(foo));
emitter.on('bar', (bar)=>console.log(bar));
```

基本的に`EventEmitter`は内部的にマップされた配列の形でデータを格納します：

```typescript
{foo: [fooListeners], bar: [barListeners]}
```

代わりに、_event_型の安全のために、イベントタイプごとのエミッタを作成することができます：

```typescript
const onFoo = new TypedEvent<Foo>();
const onBar = new TypedEvent<Bar>();

// Emit: 
onFoo.emit(foo);
onBar.emit(bar);
// Listen: 
onFoo.on((foo)=>console.log(foo));
onBar.on((bar)=>console.log(bar));
```

これには次の利点があります。

* イベントの種類は変数として簡単に検出可能です
* イベントエミッタ変数は簡単に独立してリファクタリングできます
* イベントデータ構造は型安全です

## Reference TypedEvent

```typescript
export interface Listener<T> {
  (event: T): any;
}

export interface Disposable {
  dispose();
}

/** passes through events as they happen. You will not get events from before you start listening */
export class TypedEvent<T> {
  private listeners: Listener<T>[] = [];
  private listenersOncer: Listener<T>[] = [];

  on = (listener: Listener<T>): Disposable => {
    this.listeners.push(listener);
    return {
      dispose: () => this.off(listener)
    };
  }

  once = (listener: Listener<T>): void => {
    this.listenersOncer.push(listener);
  }

  off = (listener: Listener<T>) => {
    var callbackIndex = this.listeners.indexOf(listener);
    if (callbackIndex > -1) this.listeners.splice(callbackIndex, 1);
  }

  emit = (event: T) => {
    /** Update any general listeners */
    this.listeners.forEach((listener) => listener(event));

    /** Clear the `once` queue */
    this.listenersOncer.forEach((listener) => listener(event));
    this.listenersOncer = [];
  }

  pipe = (te: TypedEvent<T>): Disposable => {
    return this.on((e) => te.emit(e));
  }
}
```

