# vim: tabstop=4 shiftwidth=4 expandtab
import builtins
import cssutils
import logging
import os
import difflib
import sys
from lxml import etree
from xml.sax.saxutils import escape as xmlescape

cssutils.ser.prefs.lineSeparator = ' '
cssutils.log.setLevel(logging.FATAL)

class SVGTemplate:
    def __init__(self, task, outfile):
        self.task = task
        self.outfile = outfile

    def __enter__(self):
        with builtins.open(os.path.join(self.task.workdir, self.task.infile), 'r') as fp:
            self.svgstr = fp.read()
        return self

    def write(self):
        # open the output-file (named ".gen.svg" in the workdir)
        with builtins.open(self.outfile, 'w') as fp:
            # write the generated svg-text into the output-file
            fp.write(self.svgstr)

    def replacetext(self):
        for key in self.task.parameters.keys():
            self.svgstr = self.svgstr.replace(key, xmlescape(str(self.task.parameters[key])))

    def transform(self, frame):
        parser = etree.XMLParser(huge_tree=True)
        svg = etree.fromstring(self.svgstr.encode('utf-8'), parser)
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
        self.svgstr = etree.tostring(svg, encoding='unicode')

    def __exit__(self, exception_type, exception_value, traceback):
        pass
