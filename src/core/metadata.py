from enum import Enum


class MetadataItem:
    """Metadata about an attribute.
        attribute:     attribute name in the python object
        input_name:    how this item is named at the start of the line in an input file, blank if not named this way.
        label:         how to label this attribute in a user interface
        default:       default value for this attribute
        units_english: units label when using English units
        units_metric:  units label when using Metric units
        hint:          description to display when editing this attribute
    """
    def __init__(self, attr_specification):
        self.attribute     = self.__value_from_list(attr_specification, 0)
        self.input_name    = self.__value_from_list(attr_specification, 1)
        self.label         = self.__value_from_list(attr_specification, 2)
        self.default       = self.__value_from_list(attr_specification, 3)
        self.units_english = self.__value_from_list(attr_specification, 4)
        self.units_metric  = self.__value_from_list(attr_specification, 5)
        self.hint          = self.__value_from_list(attr_specification, 6)

    @staticmethod
    def __value_from_list(values, index):
        """Return values[index] or if values is not that long, return empty string"""
        if len(values) > index:
            return values[index]
        else:
            return ''

    def __str__(self):
        """Override default method to return string representation"""
        return '(' + ", ".join((self.attribute,
                                self.label,
                                self.input_name,
                                self.default,
                                self.units_english,
                                self.units_metric,
                                self.hint)) + ')'


class Metadata(list):
    """List of MetadataItem items about a set of attributes.
    Useful when populating a form for editing these attributes."""

    empty_meta_item = MetadataItem(())  # a blank MetadataItem to use when one is not found

    def __init__(self, specification):
        list.__init__(self)
        for attr_spec in specification:
            self.append(MetadataItem(attr_spec))

    @staticmethod
    def value(meta_item, instance):
        if meta_item:
            if hasattr(instance, meta_item.attribute):
                value = getattr(instance, meta_item.attribute)
                if isinstance(value, Enum):
                    return value     # return the whole enum type to populate combo box in editor
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
