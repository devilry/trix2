from StringIO import StringIO
import collections
import yaml


##############################
# Loading/parsing demo
##############################

data = yaml.load(StringIO("""
title: Hello world
tags:
- inf1000
- oblig1
- arrays
body: |
  ## Hello
  cruel world.

  ## Another heading
  Some more data.
"""))

from pprint import pprint
pprint(data)


#####################################
# Dumping/outputting demo
#####################################

class MarkdownString(object):
    def __init__(self, unicode_object):
        self.unicode_object = unicode_object

    def __unicode__(self):
        return self.unicode_object

    @staticmethod
    def representer(dumper, data):
        """
        YAML representer for MarkdownString.

        We represent MarkdownString as a ``!!str``-tag (I.E.: ``tag:yaml.org,2002:str``),
        with the `literal-scalar style <http://www.yaml.org/spec/1.2/spec.html#id2795688>`_.

        We add it to yaml using::

            import yaml
            yaml.add_representer(MarkdownString, MarkdownString.representer)
        """
        return dumper.represent_scalar(u'tag:yaml.org,2002:str', data.unicode_object, style='|')


def represent_ordereddict(dumper, data):
    value = []
    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)
        value.append((node_key, node_value))
    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)

yaml.add_representer(collections.OrderedDict, represent_ordereddict)


outdata = [
    collections.OrderedDict([
        ('title', 'This is a test'),
        ('tags', ['inf1000', 'oblig1']),
        ('text', MarkdownString(u'Hello\n\ncruel\n\nworld\n'))
    ]),
    collections.OrderedDict([
        ('title', 'This is another test'),
        ('tags', ['inf1000', 'oblig1', 'week2']),
        ('text', MarkdownString(u'## A\nDo something\n\n# B\n\nDo something else.\n')),
        ('solution', MarkdownString(u'```python\ndef test():\n    print "Hello world"\n```'))
    ]),
    collections.OrderedDict([
        ('title', 'A third test'),
        ('tags', ['inf1000', 'oblig2']),
        ('text', MarkdownString(u'Hello world'))
    ]),
]

yaml.add_representer(MarkdownString, MarkdownString.representer)
print yaml.dump(outdata, default_flow_style=False)
