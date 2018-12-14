## 配列を作る

空の配列を作成するのは簡単です：

```ts
const foo:string[] = [];
```

あるコンテンツで事前に埋められた配列を作成するには、ES6`Array.prototype.fill`を使います：

```ts
const foo:string[] = new Array(3).fill('');
console.log(foo); // ['','',''];
```
