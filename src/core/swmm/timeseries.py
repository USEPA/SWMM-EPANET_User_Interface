from core.inputfile import Section


class TimeSeries(Section):
    """One time series from the TIMESERIES section"""

    field_format = "{:16}\t{:10}\t{:10}\t{:10}"

    def __init__(self, new_text=None):
        Section.__init__(self)

        self.name = ""
        """name of timeseries"""

        self.file = ""
        """file name if timeseries read from file"""

        self.dates = []
        """List of Dates"""

        self.times = []
        """List of Times"""

        self.values = []
        """List of Values"""

        if new_text:
            self.set_text(new_text)

    def get_text(self):
        text_list = []

        if self.comment:
            text_list.append(self.comment)

        if self.file:
            text_list.append(self.name + "\tFILE\t" + self.file)
        else:
            for step in zip(self.dates, self.times, self.values):
                text_list.append(self.field_format.format(self.name, step[0], step[1], step[2]))
        return '\n'.join(text_list)

    @staticmethod
    def is_date(test_string):
        if len(test_string) > 5:
            check_split = test_string.strip().split('/')
            if len(check_split) != 3:
                check_split = test_string.strip().split('-')
            if len(check_split) == 3 and ''.join(check_split).isdigit() and \
               int(check_split[0]) > 0 and int(check_split[0]) <= 12 and \
               int(check_split[1]) > 0 and int(check_split[1]) <= 31 and \
               int(check_split[2]) > 0 and int(check_split[2]) <= 3000:
                return True
        return False

    def set_text(self, new_text):
        self.__init__()
        needs_date = 1
        needs_time = 2
        needs_value = 3
        for line in new_text.splitlines():
            self.set_comment_check_section(line)
            try:
                fields = line.split()
                if len(fields) > 1:
                    if self.name:
                        if self.name != fields[0]:
                            raise ValueError("TimeSeries.set_text: Different Timeseries names " +
                                             self.name + ', ' + fields[0])
                    else:
                        self.name = fields[0]
                    if fields[1].upper() == "FILE":
                        self.file = ' '.join(fields[2:])
                    else:
                        state = needs_date
                        next_field = 1
                        while next_field < len(fields):
                            if state == needs_date:
                                if TimeSeries.is_date(fields[next_field]):
                                    self.dates.append(fields[next_field])
                                    next_field += 1
                                    if next_field == len(fields):
                                        break
                                else:
                                    self.dates.append('')
                                state = needs_time

                            if state == needs_time:
                                self.times.append(fields[next_field])
                                next_field += 1
                                if next_field == len(fields):
                                    break
                                state = needs_value

                            if state == needs_value:
                                self.values.append(fields[next_field])
                                next_field += 1
                                state = needs_date

                        if (len(self.dates) != len(self.times)) or (len(self.times) != len(self.values)):
                            raise ValueError("TimeSeries.set_text: Different lengths:" "\nDates = " + str(len(self.dates)) + "\nTimes = " + str(len(self.times)) + "\nValues = " + str(len(self.values)))
            except Exception as ex:
                raise ValueError("Could not set timeseries from line: " + line + '\n' + str(ex))
