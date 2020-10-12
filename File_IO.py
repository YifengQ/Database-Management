__author__ = "Yifeng Qin"
__class__ = "CS457 Database Management Systems"
__instructor__ = "Dongfang Zhao"
__university__ = "University of Nevada Reno"
__assignment__ = "Project 1"
__date__ = "9/15/2020"


class FileIO:

    def __init__(self):
        self.commands = []

    def readfile(self, path):
        """
        Opens the script and reads every line and stores it into a list.
        :param path:
        :return: None
        """
        with open(path) as file_in:
            for line in file_in:
                if len(line) != 1 and line[0:2] != '--':
                    self.commands.append(line.rstrip())  # removes newline and special characters






