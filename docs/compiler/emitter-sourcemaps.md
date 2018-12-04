### エミッタソースマップ

`emitter.ts`の大部分はローカル関数`emitJavaScript`です（この関数の初期化ルーチンを前に示しました）。それは基本的に地元の人々の集合を設定し、 `emitSourceFile`にヒットします。以下はこの関数の再訪です。今回は `SourceMap`に焦点を当てています：

```ts
function emitJavaScript(jsFilePath: string, root?: SourceFile) {

    // STUFF ........... removed

    let writeComment = writeCommentRange;

    /** Write emitted output to disk */
    let writeEmittedFiles = writeJavaScriptFile;

    /** Emit a node */
    let emit = emitNodeWithoutSourceMap;

    /** Called just before starting emit of a node */
    let emitStart = function (node: Node) { };

    /** Called once the emit of the node is done */
    let emitEnd = function (node: Node) { };

    /** Emit the text for the given token that comes after startPos
      * This by default writes the text provided with the given tokenKind
      * but if optional emitFn callback is provided the text is emitted using the callback instead of default text
      * @param tokenKind the kind of the token to search and emit
      * @param startPos the position in the source to start searching for the token
      * @param emitFn if given will be invoked to emit the text instead of actual token emit */
    let emitToken = emitTokenText;

    /** Called to before starting the lexical scopes as in function/class in the emitted code because of node
      * @param scopeDeclaration node that starts the lexical scope
      * @param scopeName Optional name of this scope instead of deducing one from the declaration node */
    let scopeEmitStart = function(scopeDeclaration: Node, scopeName?: string) { };

    /** Called after coming out of the scope */
    let scopeEmitEnd = function() { };

    /** Sourcemap data that will get encoded */
    let sourceMapData: SourceMapData;

    if (compilerOptions.sourceMap || compilerOptions.inlineSourceMap) {
        initializeEmitterWithSourceMaps();
    }

    if (root) {
        // Do not call emit directly. It does not set the currentSourceFile.
        emitSourceFile(root);
    }
    else {
        forEach(host.getSourceFiles(), sourceFile => {
            if (!isExternalModuleOrDeclarationFile(sourceFile)) {
                emitSourceFile(sourceFile);
            }
        });
    }

    writeLine();
    writeEmittedFiles(writer.getText(), /*writeByteOrderMark*/ compilerOptions.emitBOM);
    return;

    /// BUNCH OF LOCAL FUNCTIONS
```

ここで重要な関数は、 `initializeEmitterWithSourceMaps`です。ここで既に定義されているいくつかのローカルを上書きする`emitJavaScript`のローカル関数です。 `initializeEmitterWithSourceMaps`の一番下には、オーバーライドがあります。

```ts
    // end of `initializeEmitterWithSourceMaps`

    writeEmittedFiles = writeJavaScriptAndSourceMapFile;
    emit = emitNodeWithSourceMap;
    emitStart = recordEmitNodeStartSpan;
    emitEnd = recordEmitNodeEndSpan;
    emitToken = writeTextWithSpanRecord;
    scopeEmitStart = recordScopeNameOfNode;
    scopeEmitEnd = recordScopeNameEnd;
    writeComment = writeCommentRangeWithMap;
```

つまり、大量のエミッタコードは `SourceMap`を気にすることができず、SourceMapsの有無にかかわらずこれらのローカル関数を同じ方法で使用します。
