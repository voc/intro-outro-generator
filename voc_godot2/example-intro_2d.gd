extends Node

func apply_template_vars(id:String="", title:="", subtitle:="", personnames:=""):
	$"../Title".text = title
	$"../Personnames".text = personnames
