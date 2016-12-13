class ParseData:
    @staticmethod
    def intTryParse(value):
        try:
            return int(value), True
        except ValueError:
            return value, False

    @staticmethod
    def floatTryParse(value):
        try:
            return float(value), True
        except ValueError:
            return value, False