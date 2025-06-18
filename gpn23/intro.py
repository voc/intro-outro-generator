import bpy

bpy.context.scene.render.image_settings.file_format = "FFMPEG"
bpy.context.scene.render.ffmpeg.format = "MKV"
bpy.context.scene.render.ffmpeg.codec = "H264"
bpy.context.scene.render.ffmpeg.audio_codec = "AAC"

obj = bpy.data.objects["TEXT TITLE"]
modifier = obj.modifiers["TEXT TITLE MOD"]

modifier["Socket_2"] = "$title"


obj = bpy.data.objects["TEXT SPEAKER"]
modifier = obj.modifiers["TEXT SPEAKER MOD"]

modifier["Socket_2"] = "$personnames"
