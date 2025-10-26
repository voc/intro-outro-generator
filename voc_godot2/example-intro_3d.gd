extends Node

func apply_template_vars(id:String="", title:="", subtitle:="", personnames:=""):
	$"../Templateparts/Personnames".mesh.text = personnames
	$"../Templateparts/Title".mesh.text = title
