# vim: tabstop=4 shiftwidth=4 expandtab
import builtins
import cssutils
import os
from lxml import etree
from xml.sax.saxutils import escape as xmlescape

def open(task):
    with builtins.open(os.path.join(task.workdir, task.infile), 'r') as fp:
        return fp.read()

def replacetext(svgstr, task):
    for key in task.parameters.keys():
        svgstr = svgstr.replace(key, xmlescape(str(task.parameters[key])))
    return svgstr

def transform(svgstr, frame, task):
    parser = etree.XMLParser(huge_tree=True)
    svg = etree.fromstring(svgstr.encode('utf-8'), parser)
    # apply the replace-pairs to the input text, by finding the specified xml-elements by their id and modify their css-parameter the correct value
    for replaceinfo in frame:
        (id, type, key, value) = replaceinfo
        for el in svg.findall(".//*[@id='" + id.replace("'", "\\'") + "']"):
            if type == 'style':
                style = cssutils.parseStyle(el.attrib['style'] if 'style' in el.attrib else '')
                style[key] = str(value)
                el.attrib['style'] = style.cssText
            elif type == 'attr':
                el.attrib[key] = str(value)
            elif type == 'text':
                el.text = str(value)
    # if '$subtitle' in task.parameters and task.parameters['$subtitle'] == '':
    #   child = svg.findall(".//*[@id='subtitle']")[0]
    #   child.getparent().remove(child)
    return etree.tostring(svg, encoding='unicode')

def write(svgstr, task):
    # open the output-file (named ".gen.svg" in the workdir)
    outfile = os.path.join(task.workdir, '.gen.svg')
    with builtins.open(outfile, 'w') as fp:
        # write the generated svg-text into the output-file
        fp.write(svgstr)
    return outfile
