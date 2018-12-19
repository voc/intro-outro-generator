
var comp;
for (var i = 1; i <= app.project.numItems; i ++) {
    if ((app.project.item(i) instanceof CompItem) && (app.project.item(i).name === 'intro')) {
        comp = app.project.item(i);
        break;
    }
}
var layer_title = comp.layer('intro_title');
var textProp_title = layer_title.property("Source Text");
var textDocument_title = textProp_title.value;

var layer_persons = comp.layer('intro_personnames');
var textProp_persons = layer_persons.property("Source Text");
var textDocument_persons = textProp_persons.value;

var layer_id = comp.layer('intro_id');
var textProp_id = layer_id.property("Source Text");
var textDocument_id = textProp_id.value;

textDocument_title.text = "$title";
textProp_title.setValue(textDocument_title);

textDocument_persons.text = "$personnames";
textProp_persons.setValue(textDocument_persons);

textDocument_id.text = "$id";
textProp_id.setValue(textDocument_id);

app.project.save();
app.quit();