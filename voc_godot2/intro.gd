extends Node

# The project can be started from command line with the data as parameters:
# --id="talk-id"
# --title="How to render intros using Godot"
# --subtitle="Using Movie Mode"
# --personnames="John Doe & Jane Doe"
# --write-movie output.avi
# --resolution 1920x1080
# --fixed-fps 25
# --movie-quality 0.75 (value between 0.0 [bad] and 1.0 [best])

# It's also import to quit the project when done with the rendering.
# There are different ways of doing so, in this example it's done via the
# Animation Player -> Movie Quit On Finish

# More:
# https://docs.godotengine.org/en/latest/tutorials/animation/creating_movies.html#quitting-movie-maker-mode

@export var id_node : Node
@export var title_node : Node
@export var subtitle_node : Node
@export var personnames_node : Node

@export var path_to_id_property := ""
@export var path_to_title_property := ""
@export var path_to_subtitle_property := ""
@export var path_to_personnames_property := ""

var id := ""
var title := ""
var subtitle := ""
var personnames := ""

func _ready():
	if OS.has_feature("Editor"):
		return
	
	var arguments = {}
	for argument in OS.get_cmdline_args():
		if argument.find("=") > -1:
			var key_value = argument.split("=")
			arguments[key_value[0].lstrip("--")] = key_value[1]
		else:
			arguments[argument.lstrip("--")] = ""
	
	ProjectSettings.set_setting("editor/movie_writer/mjpeg_quality", clamp(arguments.get("quality", 0.75), 0.1, 1.0))
	
	id = arguments.get("id", "")
	title = arguments.get("title", "")
	subtitle = arguments.get("subtitle", "")
	personnames = arguments.get("personnames", "")
	
	$ApplyTemplate.apply_template_vars(id, title, subtitle, personnames)
