## どのファイルですか？

明示的に `files`を使うことができます：

```json
{
    "files":[
        "./some/file.ts"
    ]
}
```

ファイル/フォルダ/グロブを指定するには `include`と`exclude`を使います。例えば。：


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

いくつかのメモ：

* globsの場合： `** / *`(例えば、サンプル使用法 `somefolder / ** / *`)はすべてのフォルダとファイルを意味します( `.ts`/` .tsx`拡張子が仮定され、 `allowJs：true `so will`.js` / `.jsx`)
