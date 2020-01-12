`include`と`exclude`を使い、ファイル/フォルダ/グロブ(glob)を指定します。例:

```json
{
    "include":[
        "./folder"
    ],
    "exclude":[
        "./folder/**/*.spec.ts",
        "./folder/someSubFolder"
    ]
}
```

### グロブ(glob)
* グロブ(globs)の場合：`**/*`(例えば、サンプル使用法 `somefolder/**/*`)はすべてのフォルダとファイルを意味します(`.ts`/`.tsx`拡張子が対象になります。`allowJs:true`を設定した場合は`.js`/`.jsx`)。

### `files`オプション
明示的に `files`を使うこともできます：

```json
{
    "files":[
        "./some/file.ts"
    ]
}
```

ただし、指定したファイルを更新し続ける必要があるためおすすめしません。代わりに`include`を使用して指定したいファイルがあるフォルダを追加してください。
* グロブ(globs)の場合：`**/*`(例えば、サンプル使用法 `somefolder/**/*`)はすべてのフォルダとファイルを意味します(`.ts`/`.tsx`拡張子が対象になります。`allowJs:true`を設定した場合は`.js`/`.jsx`)。
