import bpy

sce = bpy.context.scene

sce.objects['SPEAKERS'].data.body = '$personnames'
sce.objects['TITLE'].data.body = '$title'
sce.objects['TALKID'].data.body = '$id'
