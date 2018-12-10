## ファイルの指定

明示的に `files`を使うことができます：

```json
{
    "files":[
        "./some/file.ts"
    ]
}
```

ファイル/フォルダ/グロブ(glob)を指定するには `include`と`exclude`を使います。例:


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

メモ：

* グロブ(globs)の場合：`**/*`(例えば、サンプル使用法 `somefolder/**/*`)はすべてのフォルダとファイルを意味します(`.ts`/`.tsx`拡張子が対象になります。`allowJs：true`を設定した場合は`.js`/`.jsx`)。
