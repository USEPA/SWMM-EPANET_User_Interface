class ParseData:
    @staticmethod
    def intTryParse(value):
        try:
            if isinstance(value, int):
                return value, True
            else:
                if str(value):
                    return int(value), True
                else:
                    return None, False
        except ValueError:
            return value, False

    @staticmethod
    def floatTryParse(value):
        try:
            if isinstance(value, float):
                return value, True
            else:
                if str(value):
                    return float(value), True
                else:
                    return None, False
        except ValueError:
            return value, False