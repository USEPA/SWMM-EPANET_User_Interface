
class Metadatum:
    """Metadata about one attribute
        attribute: name of attribute in a class
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
    """List of Metadatum items about a collection of attributes"""

    empty_datum = Metadatum(('', '', '', ''))

    def __init__(self, specification):
        for attr_spec in specification:
            self.append(Metadatum(attr_spec))

    def datum_of(self, attribute):
        for datum in self:
            if datum.attribute == attribute:
                return datum
        return Metadata.empty_datum

    def label_of(self, attribute):
        return self.datum_of(attribute).label

    def default_of(self, attribute):
        return self.datum_of(attribute).default

    def hint_of(self, attribute):
        return self.datum_of(attribute).hint

    def __str__(self):
        """Override default method to return string representation"""
        return '\n'.join(str(datum) for datum in self)
