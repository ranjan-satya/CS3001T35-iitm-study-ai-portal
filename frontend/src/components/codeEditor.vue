<!-- MonacoEditor.vue -->
<template>
<div ref="editorContainer" class="monaco-editor-container"></div>
</template>

<script>
import * as monaco from 'monaco-editor';

export default {
    props: {
        value: {
            type: String,
            default: ''
        }
    },
    mounted() {
        this.editor = monaco.editor.create(this.$refs.editorContainer, {
        value: this.value,
        language: 'python', // Set the language mode here
        theme: 'vs' // Set the theme here
        });

        // Define read-only ranges based on the initial value
        const lines = this.value.split('\n');
        const readOnlyLines = lines.slice(0, 5); // Example: First 4 lines are read-only
        this.readOnlyRanges = [
        new monaco.Range(1, 1, readOnlyLines.length, 1),
        new monaco.Range(8, 1, 9, lines[10].length + 1)
        ];

        // Apply decorations to read-only ranges
        this.applyReadOnlyDecorations();

        // Prevent editing in read-only ranges
        this.editor.onDidChangeModelContent((event) => {
            this.preventEditingInReadOnlyRanges(event);
        });

        this.editor.onDidChangeCursorPosition((event) => {
            this.preventCursorInReadOnlyRanges(event);
        });

        this.editor.onDidChangeModelContent(() => {
            const value = this.editor.getValue();
            // console.log('Emitting input event with value:', value); // Add this line
            this.$emit('written', value);
        });

        // Prevent clicks in read-only ranges
        this.editor.onMouseDown((event) => {
            const position = event.target.position;
            if (position && this.isInReadOnlyRange(position)) {
                event.event.stopPropagation();
            }
        });

         // Prevent backspace in read-only ranges
        this.editor.onKeyDown((event) => {
            if (event.keyCode === monaco.KeyCode.Backspace) {
                const position = this.editor.getPosition();
                if (this.isInReadOnlyRange(position)) {
                    event.preventDefault();
                }
            }
        });
    },
    methods: {
        applyReadOnlyDecorations() {
        const decorations = this.readOnlyRanges.map(range => ({
            range: range,
            options: {
                isWholeLine: true,
                className: 'read-only-line',
                glyphMarginClassName: 'read-only-glyph'
            }
        }));
        this.editor.deltaDecorations([], decorations);
        },
        preventEditingInReadOnlyRanges(event) {
        const model = this.editor.getModel();
        const edits = event.changes;
        for (let edit of edits) {
            const range = new monaco.Range(
            edit.range.startLineNumber,
            edit.range.startColumn,
            edit.range.endLineNumber,
            edit.range.endColumn
            );
            for (let readOnlyRange of this.readOnlyRanges) {
            if (readOnlyRange.intersectRanges(range)) {
                // Revert the change if it intersects with a read-only range
                model.applyEdits([{
                range: range,
                text: model.getValueInRange(range)
                }]);
                break;
            }
            }
        }
        },
        preventCursorInReadOnlyRanges(event) {
        const position = event.position;
        for (let readOnlyRange of this.readOnlyRanges) {
            if (readOnlyRange.containsPosition(position)) {
            // Move cursor to the end of the read-only range
            this.editor.setPosition({
                lineNumber: readOnlyRange.endLineNumber + 1,
                column: 1
            });
            break;
            }
        }
        },
        isInReadOnlyRange(position) {
            return this.readOnlyRanges.some(range => range.containsPosition(position));
        }
    },
    beforeUnmount() {
        if (this.editor) {
        this.editor.dispose();
        }
    }
};
</script>

<style scoped>
.monaco-editor-container {
width: 100%;
height: 400px; /* Adjust the height as needed */
}

.read-only-line {
    background-color: #e49696; /* Light grey background for read-only lines */
  }
  
  .read-only-glyph {
    background-color: #d0d0d0; /* Darker grey for glyph margin */
  }
</style>