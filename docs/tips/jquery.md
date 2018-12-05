## JQueryのヒント

注意：これらのヒント用に `jquery.d.ts`ファイルをインストールする必要があります

### 新しいプラグインをすばやく定義する

次のように `jquery-foo.d.ts`を作成してください：

```ts
interface JQuery {
  foo: any;
}
```

そして、あなたは `$( 'something')を使うことができます。foo({whateverYouWant： 'hello jquery plugin'})`
