# Create Arrays

空の配列を作成するのは簡単です：

```typescript
const foo:string[] = [];
```

あるコンテンツで事前に埋められた配列を作成するには、ES6`Array.prototype.fill`を使います：

```typescript
const foo:string[] = new Array(3).fill('');
console.log(foo); // ['','',''];
```

