__author__ = "Yifeng Qin"
__class__ = "CS457 Database Management Systems"
__instructor__ = "Dongfang Zhao"
__university__ = "University of Nevada Reno"
__assignment__ = "Project 1"
__date__ = "9/15/2020"

from File_IO import FileIO
from run_script import RunScript

# initializes the script and file classes
script = RunScript()
file = FileIO()
# the location to place the test script
file.readfile("Script/PA1_test.sql")


def run_commands(commands):
    """
    Takes in list of commands and determines which function it correlates too.
    It will splice the commands to get rid of special characters
    :param commands: list of commands
    :return: None
    """
    for command in commands:
        l = command.split(' ')
        if 'CREATE DATABASE' in command:
            script.create_database(l[2][:-1])
        elif 'DROP DATABASE' in command:
            script.drop_database(l[2][:-1])
        elif 'USE' in command:
            script.use_database(l[1][:-1])
        elif 'CREATE TABLE' in command:
            script.create_table(l[2:])
        elif 'SELECT * FROM' in command:
            script.select_all(l[3][:-1])
        elif '.EXIT' in command:
            return


run_commands(file.commands)

