__author__ = "Yifeng Qin"
__class__ = "CS457 Database Management Systems"
__instructor__ = "Dongfang Zhao"
__university__ = "University of Nevada Reno"
__assignment__ = "Project 1"
__date__ = "9/15/2020"

import re
import sys
from run_script import RunScript

# initializes the script and file classes
script = RunScript()


# def read_file():
#     """
#     Opens the file with standard input, and reads every line and checks if it is a valid command to be
#     appended to the list
#     :return: Returns a List of the Commands
#     """
#     commands = []
#     for line in sys.stdin:
#         if line == '\r\n' or line[0:2] == '--':  # checks if it is a empty new line or it starts with '--'
#             continue
#         else:
#             commands.append(line.rstrip())  # removes newline and special characters from line to append to list
#
#     return commands

def read_file():
    """
    Opens the file with standard input, and reads every line and checks if it is a valid command to be
    appended to the list
    :return: Returns a List of the Commands
    """
    with open("PA2_test.sql") as file_in:
        commands = []
        temp = []
        for line in file_in:
            if line == '\r\n' or line == '\n' or line[0:2] == '--':  # checks if it is a relevant line to read
                continue
            else:
                if ';' not in line:
                    temp.append(line.rstrip()+' ')
                else:
                    temp = "".join(temp)
                    line = re.sub(r"[\n\t]*", "", line)
                    commands.append(temp + line.rstrip())  # removes newline and special characters from line to append to list
                    temp = []
    return commands

def run_commands():
    """
    Calls the helper function read_file to get all the valid commands from the file. It will run through the list and
    splice the commands to get rid of special characters.
    :return: None
    """
    commands = read_file()  # calls helper function to initialize to list commands
    for command in commands:
        l = command.split(' ')  # splits the string command into a list based on spaces
        command = command.upper()  # converts the command to all uppercase so it can cover case sensitivity
        size = len(l)  # gets length to handle missing spaces
        if 'CREATE DATABASE' in command:
            if size == 3:  # checks if all arguments are present
                script.create_database(l[2][:-1].upper())  # only gets the database name and removes the ';' from the back
            else:
                print('Syntax Error:', command)  # if size does not match there has to be a syntax error with cmd
        elif 'DROP DATABASE' in command:
            if size == 3:  # checks if all arguments are present
                script.drop_database(l[2][:-1].upper())   # only gets the database name and removes the ';' from the back
            else:
                print('Syntax Error:', command)  # if size does not match there has to be a syntax error with cmd
        elif 'DROP TABLE' in command:
            if size == 3:  # checks if all arguments are present
                script.drop_table(l[2][:-1].upper())   # only gets the database name and removes the ';' from the back
            else:
                print('Syntax Error:', command)  # if size does not match there has to be a syntax error with cmd
        elif 'USE' in command:
            if size == 2:  # checks if all arguments are present
                script.use_database(l[1][:-1].upper())   # only gets the database name and removes the ';' from the back
            else:
                print('Syntax Error:', command)  # if size does not match there has to be a syntax error with cmd
        elif 'CREATE TABLE' in command:
            if size >= 3:  # checks the the minimum amount of arguments are present
                command = " ".join(l[3:])  # gets all the variables after the table name and converts it into a string
                command = command[1:-2]  # then slice off the beginning '(' and the ');' at the end
                script.create_table(l[2].upper(), command)  # passes in the name of the table and the sliced variables to input
            else:
                print('Syntax Error:', command)  # if size does not match there has to be a syntax error with cmd
        elif 'SELECT * FROM' in command:
            if size == 4:  # checks if all arguments are present
                script.select_all(l[3][:-1].upper()) # only gets the table name and removes the ';' from the back
            else:
                print('Syntax Error:', command)  # if size does not match there has to be a syntax error with cmd
        elif 'ALTER TABLE' in command:
            if size >= 4:  # checks if all arguments are present
                command = " ".join(l[4:])  # gets all the variables after the table name and converts it into a string
                command = command[:-1]  # removes the ';' from the back of string
                script.alter_table(l[2].upper(), command)  # passes in the name of table and sting of variables
            else:
                print('Syntax Error:', command)  # if size does not match there has to be a syntax error with cmd
        elif 'INSERT' in command:
            script.insert_table(l[2].upper(), l[3:])
        elif 'UPDATE' in command:
            script.update_table(l[1].upper(), l[2:])
            #print(command)
        elif 'DELETE' in command:
            script.delete_items(l[2].upper(), l[3:])
        elif 'SELECT' in command:
            from_idx = l.index('from')
            script.select_specific(l[1:from_idx], l[from_idx+1].upper(), l[from_idx+2:])
        elif '.EXIT' in command:
            print('All Done')
            return
        else:  # if the command is not recognised it's and unknown command or there is something wring with the syntax
            print('Syntax Error | Unknown Command')
            print(command)


run_commands()
