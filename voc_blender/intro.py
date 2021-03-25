import bpy

sce = bpy.context.scene

sce.sequence_editor.sequences_all['Text: Title'].text = '$title'
sce.sequence_editor.sequences_all['Text: Speakers'].text = '$personnames'