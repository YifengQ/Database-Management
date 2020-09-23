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
        command = command.upper()
        size = len(l)
        if 'CREATE DATABASE' in command:
            if size == 3:
                script.create_database(l[2][:-1])
            else:
                print('Syntax Error', command)
        elif 'DROP DATABASE' in command:
            if size == 3:
                script.drop_database(l[2][:-1])
            else:
                print('Syntax Error', command)
        elif 'DROP TABLE' in command:
            if size == 3:
                script.drop_table(l[2][:-1])
            else:
                print('Syntax Error', command)
        elif 'USE' in command:
            if size == 2:
                script.use_database(l[1][:-1])
            else:
                print('Syntax Error', command)
        elif 'CREATE TABLE' in command:
            if size >= 3:
                script.create_table(l[2:])
            else:
                print('Syntax Error:', command)
        elif 'SELECT * FROM' in command:
            if size == 4:
                script.select_all(l[3][:-1])
            else:
                print('Syntax Error', command)
        elif 'ALTER TABLE' in command:
            if size >= 4:
                script.alter_table(l[2:])
            else:
                print('Syntax Error', command)
        elif '.EXIT' in command:
            return
        else:
            print('Syntax Error | Unknown Command')
            print(command)


run_commands(file.commands)

