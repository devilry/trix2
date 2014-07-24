import collections
import yaml


class MarkdownString(object):
    """
    Used to mark unicode strings as Markdown for the YAML serializer.

    This is just so we can dump them using the literal-scalar style.

    """
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
        """
        return dumper.represent_scalar(u'tag:yaml.org,2002:str', data.unicode_object, style='|')

yaml.SafeDumper.add_representer(MarkdownString, MarkdownString.representer)


class YamlMapOrderedDict(collections.OrderedDict):
    """
    A subclass of ``collections.OrderedDict`` that we have
    a registered yaml f
    """

    @staticmethod
    def representer(dumper, data):
        """
        YAML representer for YamlMapOrderedDict.
        """
        value = []
        for item_key, item_value in data.items():
            node_key = dumper.represent_data(item_key)
            node_value = dumper.represent_data(item_value)
            value.append((node_key, node_value))
        return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)

yaml.SafeDumper.add_representer(YamlMapOrderedDict, YamlMapOrderedDict.representer)


def serialize(assignments):
    """
    Serialize an iterable of assignments.

    Params:
        assignments (iterable): Iterable of :class:`trix.trix_core.models.Assignment` objects
    """
    serializable_assignments = []
    for assignment in assignments:
        serializable_assignment = YamlMapOrderedDict([
            ('id', assignment.id),
            ('title', assignment.title),
            ('tags', [tag.tag for tag in assignment.tags.all()]),
            ('text', MarkdownString(assignment.text)),
        ])
        if assignment.solution:
            serializable_assignment['solution'] = MarkdownString(assignment.solution)
        serializable_assignments.append(serializable_assignment)
    return yaml.safe_dump_all(serializable_assignments)
