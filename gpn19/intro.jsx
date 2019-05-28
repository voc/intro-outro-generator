
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

textDocument_title.text = "$title";
textProp_title.setValue(textDocument_title);

textDocument_persons.text = "$personnames";
textProp_persons.setValue(textDocument_persons);

app.project.save();
app.quit();
