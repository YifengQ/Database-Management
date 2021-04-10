__author__ = "Yifeng Qin"
__class__ = "CS457 Database Management Systems"
__instructor__ = "Dongfang Zhao"
__university__ = "University of Nevada Reno"
__assignment__ = "Project 4"
__date__ = "11/29/20"

import re
import sys
from run_script import RunScript

# initializes the script and file classes
script = RunScript()


def get_input():
    command = input("Enter Command: ")
    if '--' in command:  # removes comments at end of line
        command = command[:command.index('--')-1]

    return command


def run_commands_inline():

    command = get_input()
    if '.exit' in command:
        print("All Done.")
        return
    else:
        command = re.sub(r"[\n\t]*", "", command)  # removes random special characters like tabs
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
            command = " ".join(l)
            idx = command.index('(')
            var = command[idx:]
            temp = command[:idx].split(' ')
            if size >= 3:  # checks the the minimum amount of arguments are present
                script.create_table(temp[-1], var[1:-2])  # passes in the name of and the sliced variables to input
            else:
                print('Syntax Error:', command)  # if size does not match there has to be a syntax error with cmd
        elif 'SELECT * FROM' in command:
            if size == 4:
                script.select_all_no_condition(l[3].upper()[:-1])
            elif size > 4:  # checks if all arguments are present
                script.select_all(l[3].upper(), l[3:])  # only gets the table name and removes the ';' from the back
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
            command = " ".join(l)
            idx = command.index('(')
            var = command[idx:]
            temp = command[:idx].split(' ')
            if size >= 4:  # checks if all arguments are present
                script.insert_table(temp[-2].upper(), var[1:-2])
            else:
                print('Syntax Error:', command)  # if size does not match there has to be a syntax error with cmd
        elif 'UPDATE' in command:
            if size >= 8:  # checks if the minimum amount of variables are present
                    script.update_table(l[1].upper(), l[2:])
            else:
                print('Syntax Error:', command)  # if size does not match there has to be a syntax error with cmd
        elif 'DELETE' in command:
            if size >= 7:  # checks if the minimum amount of variables are present
                script.delete_items(l[2].upper(), l[3:])
            else:
                print('Syntax Error:', command)  # if size does not match there has to be a syntax error with cmd
        elif 'SELECT' in command:
            if size >= 7:  # checks if the minimum amount of variables are present
                from_idx = l.index('from')
                script.select_specific(l[1:from_idx], l[from_idx+1].upper(), l[from_idx+2:])
            else:
                print('Syntax Error:', command)  # if size does not match there has to be a syntax error with cmd
        elif 'BEGIN TRANSACTION' in command:
            script.transaction()
        elif 'COMMIT' in command:
            print('Transaction abort.')
        elif '.EXIT' in command:
            print('All Done')
            return
        else:  # if the command is not recognised it's and unknown command or there is something wring with the syntax
            print('Syntax Error | Unknown Command')
            print(command)
        run_commands_inline()


run_commands_inline()
