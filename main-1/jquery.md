# JQuery tips

注意：これらのTipsのために`jquery.d.ts`ファイルをインストールする必要があります

## 新しいプラグインをすばやく定義する

次のように`jquery-foo.d.ts`を作成してください：

```typescript
interface JQuery {
  foo: any;
}
```

そして、あなたは`$('something').foo({whateverYouWant:'hello jquery plugin'})`を使うことができます。

