from enum import Enum


class MetadataItem:
    """Metadata about one attribute
        attribute: name of attribute
        label:     how to label this attribute in a user interface
        default:   default value for this attribute
        hint:      description of this attribute
    """
    def __init__(self, attr_specification):
        (self.attribute, self.label, self.default, self.hint) = attr_specification

    def __str__(self):
        """Override default method to return string representation"""
        return '(' + ", ".join((self.attribute, self.label, self.default, self.hint)) + ')'


class Metadata(list):
    """List of MetadataItem items about a collection of attributes"""

    empty_meta_item = MetadataItem(('', '', '', ''))

    def __init__(self, specification):
        for attr_spec in specification:
            self.append(MetadataItem(attr_spec))

    @staticmethod
    def value(meta_item, instance):
        if meta_item:
            if hasattr(instance, meta_item.attribute):
                value = getattr(instance, meta_item.attribute)
                if isinstance(value, Enum):
                    return value.name
                elif len(str(value)) > 0:
                    return str(value)
            return meta_item.default
        return ''

    def values(self, instance):
        values = []
        for meta_item in self:
            if hasattr(instance, meta_item.attribute) and len(meta_item.attribute) > 0:
                values.append(getattr(instance, meta_item.attribute))
            else:
                values.append(meta_item.default)
        return values

    def labels(self):
        labels = []
        for meta_item in self:
            labels.append(meta_item.label)
        return labels

    def meta_item_of(self, attribute):
        for meta_item in self:
            if meta_item.attribute == attribute:
                return meta_item
        return Metadata.empty_meta_item

    def label_of(self, attribute):
        return self.meta_item_of(attribute).label

    def default_of(self, attribute):
        return self.meta_item_of(attribute).default

    def hint_of(self, attribute):
        return self.meta_item_of(attribute).hint

    def __str__(self):
        """Override default method to return string representation"""
        return '\n'.join(str(datum) for datum in self)
