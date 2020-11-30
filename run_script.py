__author__ = "Yifeng Qin"
__class__ = "CS457 Database Management Systems"
__instructor__ = "Dongfang Zhao"
__university__ = "University of Nevada Reno"
__assignment__ = "Project 4"
__date__ = "11/29/20"

import os
import re
import collections
from shutil import copyfile


class RunScript:

    def __init__(self):
        """
        Gets the current working directory and initializes variables
        """
        self.parentDir = os.getcwd()
        self.dbDir = None
        self.currTable = None
        self.data = []
        self.lock = False
        self.lockedTables = []

    def create_database(self, db):
        """
        Joins the parent directory with the entered database name. Checks if the database already exists. If it exists
        already it will print out and error, if not it will create a directory of the database name.
        :param db: string that contains the name of the database
        :return: None
        """
        path = os.path.join(self.parentDir, db)  # joins cwd and db name
        if os.path.exists(path):  # check if path exists
            output = '!Failed to create database ' + db + ' because it already exists'
            print(output)
        else:
            os.mkdir(path)  # creates directory of path
            output = 'Database ' + db + ' created.'
            print(output)

    def drop_database(self, db):
        """
        Joins the parent directory with the entered database. Checks if the database already exists, and will either
        error out or delete that database.
        :param db: string that contains the name of the database
        :return: None
        """
        path = os.path.join(self.parentDir, db)  # check if path exists
        if os.path.exists(path):   # check if path exists
            cmd = 'rm ' + '-rf ' + path  # concatenate command to input
            os.system(cmd)  # runs the command
            output = 'Database ' + db + ' deleted.'
            print(output)
        else:
            output = '!Failed to delete ' + db + ' because it already exists.'
            print(output)

    def use_database(self, db):
        """
        Joins the parent directory with the entered database. Checks if the database already exists, and will either
        error out change the working directory to the database.
        :param db: string that contains the name of the database
        :return: None
        """
        path = os.path.join(self.parentDir, db)  # joins cwd and db name
        if os.path.exists(path):  # check if path exists
            os.chdir(path)  # changes cwd to this path
            self.dbDir = path
            output = 'Using database ' + db + '.'
            print(output)
        else:
            print('Cannot Use Database | Does Not Exist')

    def create_table(self, tbl, inp):
        """
        Gets the path to that table and will check if that already exists. Then if it does not exist, it will change the
        directory and call a helper function to append data to the table.
        :param tbl:
        :param inp: Contains all the data that will be entered into the table
        :return: None
        """
        path = os.path.join(self.dbDir, tbl.upper())  # joins cwd and db name
        if os.path.exists(path):   # check if path exists
            output = '!Failed to create table ' + tbl + ' because it already exists.'
            print(output)
        else:
            os.mknod(path)  # creates file system of path
            self.currTable = tbl.upper()
            out = inp.split(',')
            out = "|".join(out)
            f = open(path, "a")  # opens file
            f.write(out)  # write to file
            f.close()  # close file
            output = 'Table ' + tbl + ' created.'
            print(output)

    def select_all_no_condition(self, table):
        """
        Checks if the table exists and then reads all the data from the file and prints it out.
        :param table: String that contains name of the table
        :return:
        """
        self.data = []
        path = os.path.join(self.dbDir, table)  # joins cwd and db name
        if os.path.exists(path):  # check if path exists
            with open(path) as file_in:  # starts reading from file
                for line in file_in:
                    self.data.append(line.rstrip())
            for line in self.data:  # prints data to terminal
                print(line)
            self.data = []
        else:
            output = '!Failed to query table ' + table + ' because it does not exist.'
            print(output)

    def select_all(self, table, inp):
        """
        Checks if the table exists and then reads all the data from the file and prints it out.
        :param table: String that contains name of the table
        :param inp:
        :return: Check tables first * Notes
        """
        tbls = []
        tbls_alias = []
        cmd = " ".join(inp)
        d = collections.defaultdict(list)

        if 'inner join' in cmd:
            where_idx = inp.index('on')
            new = " ".join(inp[:where_idx])
            new = new.replace(' inner join', ',')
            type = 'inner join'
        elif 'left outer' in cmd:
            where_idx = inp.index('on')
            new = " ".join(inp[:where_idx])
            new = new.replace(' left outer', ',')
            type = 'left outer'
        else:
            where_idx = inp.index('where')
            new = " ".join(inp[:where_idx])
            type = 'equal'

        new = new.split(',')

        for i, t in enumerate(new):
            temp = t.split(' ')  # splits the table names to name and alias
            tbls.append(temp[-2].upper())
            tbls_alias.append(temp[-1])  # stores alias in list
            path = os.path.join(self.dbDir, tbls[i])  # joins cwd and tbl name
            if os.path.exists(path):
                d[tbls_alias[i]] = self.read_all(path)  # stores table data into a dictionary key = alias, value = data
            else:
                print('!Failed to query table ' + table + ' because it does not exist.')
                return
        logic = inp[where_idx + 1:]  # contains the rest of the logic comparisons
        res = self.join_helper(d, logic, tbls_alias, type)  # calls helper to combine tables, returns result
        for line in res:
            print(line)

    def join_helper(self, d, logic, tbls_alias, type):
        """
        Helps the table by separating the values and then determining which function it should call.
        """
        rows = len(d[tbls_alias[1]])  # number of rows in the table
        cols = len(d)  # number of cols in the table
        cols_names = [None] * cols  # initialize list for col names
        cols_id = [0] * cols  # initialize list for col id's
        cols_names[0] = logic[0].split('.')[-1]  # since only two comparisons get the name of the col name
        cols_names[1] = logic[-1].split('.')[-1][:-1]  # since only two comparisons get the name of the col name
        var = ""
        for i, c in enumerate(cols_names):
            cols_id[i] = self.find_idx(d[tbls_alias[i]][0].split(' |'), c)  # gets the col num of the var to compare
            var += d[tbls_alias[i]][0]  # joins the two tables variables together
            if i != cols - 1:
                var += ' |'
        res = [var]  # initialize result with variable names
        if type == 'inner join' or type == 'equal':
            res = self.inner_join(rows, res, d, tbls_alias, cols_id)
        else:
            res = self.outer_join(rows, res, d, tbls_alias, cols_id)

        return res

    @staticmethod
    def inner_join(rows, res, d, tbls_alias, cols_id):
        """
        Will perform the inner join by concatinating all the values that match the logic operation
        """
        for i in range(1, rows):  # compare all the rows and if the variables being compared match join them together
            for j in range(1, rows):
                d1 = d[tbls_alias[0]][i]
                d2 = d[tbls_alias[1]][j]
                if d1.split('|')[cols_id[0]] == d2.split('|')[cols_id[1]]:  # compare variables
                    res.append(d1 + '|' + d2)
        return res

    @staticmethod
    def outer_join(rows, res, d, tbls_alias, cols_id):
        """
        Will perform the inner join by concatinating all the values that match the logic operation
        """
        for i in range(1, rows):  # compare all the rows and if the variables being compared match join them together
            found = False  # determines if they found a match
            for j in range(1, rows):
                d1 = d[tbls_alias[0]][i]  # gets the data in the first table
                d2 = d[tbls_alias[1]][j]  # gets the data in the second table
                if d1.split('|')[cols_id[0]] == d2.split('|')[cols_id[1]]:  # compare variables
                    res.append(d1 + '|' + d2)
                    found = True
            if not found:
                res.append(d[tbls_alias[0]][i] + '|' * len(cols_id))
        return res

    def alter_table(self, tbl, inp):
        """
        Will check if the table exists, if it doesn't exist it will print out an error.
        If it exists it will then append the extra values to the file.
        :param tbl: String containing name of table
        :param inp: string that need to be inputted
        :return: None
        """
        path = os.path.join(self.dbDir, tbl)  # joins cwd and db name
        if os.path.exists(path):  # check if path exists
            out = inp.split(',')  # takes the string a separates all the values by comma's and storing it into a list
            out = "|".join(out)  # joins the list back together into a string with a '|' at value
            f = open(path, "a")  # opens file
            f.write('| ' + out)  # adds '|' to separate existing values and then writes the output string
            f.close()  # close file
            output = 'Table ' + tbl + ' modified.'
            print(output)
        else:
            output = '!Failed to alter table ' + tbl + ' because it does not exist'
            print(output)

    def drop_table(self, tbl):
        """
        Checks if the table exists and if that table exists it will delete that path. If it does not exist
        it will error and print the error message
        :param tbl: string that contains the name of the table
        :return: None
        """
        path = os.path.join(self.dbDir, tbl)  # check if path exists
        if os.path.exists(path):  # check if path exists
            cmd = 'rm ' + '-rf ' + path  # concatenate command to run
            os.system(cmd)  # runs the command
            output = 'Table ' + tbl + ' deleted.'
            print(output)
        else:
            output = '!Failed to delete ' + tbl + ' because it does not exists.'
            print(output)

################################### Additional Assignment 2 Functions  #################################

    def read_all(self, path):
        """
        Checks if the table exists and then reads all the data from the file and prints it out.
        :param path: String that contains path of the table
        :return: None
        """
        self.data = []
        if os.path.exists(path):  # check if path exists
            with open(path) as file_in:  # starts reading from file
                for line in file_in:
                    self.data.append(line.rstrip())
            return self.data
        else:
            output = '!Failed to query table because it does not exist.'
            print(output)

    @staticmethod
    def insert_helper(path, inp):
        """
        Helper that writes the new list of values to the file
        :param path: Path that leads to the table file
        :param inp: the new data that needs to be written to the file
        :return: None
        """
        f = open(path, "a")  # opens file
        f.truncate(0)
        for line in inp:
            out = "|".join(line)
            out += '\n'  # adds the new line
            f.write(out)  # write to file
        f.close()  # close file

    def insert_table(self, table, new_data):
        """
        Takes in the name of the table and inserts the new data to that data.
        :param table: string with name of the tale
        :param new_data: contains the new data that needs to be inserted
        :return: None
        """
        path = os.path.join(self.dbDir, table)
        if os.path.exists(path):  # check if path exists
            res = []
            data = self.read_all(path)  # reads all the current data from the file and stores it in a list
            for line in data:  # reads the lines and splits the data
                res.append(line.split('|'))

            new_data = new_data.split(',')  # splits the data on commas
            res.append(new_data)  # adds the new list to the rest of the data
            self.insert_helper(path, res)  # calls the helper function to print the data to the file
            output = '1 New Record Inserted'
            print(output)
        else:
            output = '!Failed to insert into table ' + table + ' because it does not exist.'
            print(output)

    def update_table(self, table, data):
        """
        Updates specific value if conditions match. Finds the index of the desired variable. Then it changes the
        variable that needs to be changed based on the index of the variable that needs to change.
        :param table: string with name of the table
        :param data: contains the data to update the table
        :return: None
        """
        path = os.path.join(self.dbDir, table)
        if os.path.exists(path):  # check if path exists
            var = data[1]  # gets the specific values that are in the list
            var2 = data[5]
            operation = data[2]
            changeto = data[3]
            change = data[7][:-1]
            new, count = self.update_helper(path, var, var2, operation, change, changeto)  # calls helper func. to get/
            # new data data and count of how many objects were updated
            self.insert_helper(path, new)  # calls helper function to print new data to file
            if count > 1:  # print plural of singular
                output = str(count) + ' Records Modified'
            else:
                output = str(count) + ' Records Modified'
        else:
            output = '!Failed to update table ' + table + ' because it does not exist.'
        print(output)

    def update_helper(self, path, var, var2, operation, change, changeto):
        """
        Helper function that finds all the indexes of the values that need to be change. it will compare those values
        using the operators specified and then update the specific value that matches up the the desired conditions.
        :param path: string that contains the path of the file
        :param var: contains the variable that needs to match
        :param var2: contains the variable that needs to change
        :param operation: the operation that needs to compare the values to satisfy the conditions.
        :param change: The variable that needs to be changed
        :param changeto: The variable that needs to be changed too
        :return:
        """
        data = self.read_all(path)  # reads in all the data from the current file
        res = [[data[0]]]  # creates the final list to be printed to file
        curr = self.read_all_list(data)  # turns all the lines into lists making it a list of lists
        count = 0  # initiates the count for the number of changes
        where_idx = self.find_idx(curr[0], var2)  # finds the index that needs to found
        set_idx = self.find_idx(curr[0], var)  # finds the index that equates to being changed
        if operation == '=':
            operation = '=='

        for line in curr[1:]:
            if operation == '==':
                if eval('line[where_idx]' + operation + 'change'):  # if the variable satisfies the condition to change
                    line[set_idx] = changeto  # changed the desired variable that needs to be changed
                    res.append(line)
                    count += 1
                else:
                    res.append(line)
            elif operation == '!=':  # checks if operation is not equal because of differences in float and strings
                if eval('line[where_idx]' + operation + 'change'):  # if the variable satisfies the condition to change
                    res.append(line)
                else:
                    line[set_idx] = changeto  # changed the desired variable that needs to be changed
                    res.append(line)
                    count += 1
            else:
                if eval('float(line[where_idx])' + operation + 'float(change)'):  # <, > can only compare numbers
                    line[set_idx] = changeto  # changed the desired variable that needs to be changed
                    res.append(line)
                    count += 1
                else:
                    res.append(line)

        return res, count

    def delete_items(self, table, data):
        """
        Takes in the table and deletes the desired rows that satisfy the conditions.
        :param table: string with name of table
        :param data: contains the data and conditions needed to delete a row
        :return: None
        """
        path = os.path.join(self.dbDir, table)
        if os.path.exists(path):  # check if path exists
            where = data[1]
            if data[2] == '=':  # turns it into and '==' to use as an operator
                operation = data[2] + data[2]
            else:
                operation = data[2]
            var = data[3][:-1]
            new, count = self.delete_helper(path, where, operation, var)  # calls helper to get new data and count
            self.insert_helper(path, new)  # calls helper to print new data to file
            if count >= 1:  # determines if singular or plural print
                output = str(count) + " Records Deleted"
            else:
                output = str(count) + " Record Deleted"
        else:
            output = '!Failed to delete items in table ' + table + ' because it does not exist.'
        print(output)

    def delete_helper(self, path, where, operation, var):
        """
        Helper to delete where it find the index of the variable that needs to compared. Then it will compare it with
        the operation specified to determine if that row needs to be deleted.
        :param path: string that has the path of the table
        :param where: the variable that needs to satisfy the condition
        :param operation: the logic operation
        :param var: the variable that needs to match the where to delete the row
        :return: the new list that needs to be printed and the count of the items deleted.
        """
        data = self.read_all(path)  # reads all the data that is stored in the current file
        res = [[data[0]]]  # initiates the new data with variable names
        curr = self.read_all_list(data)  # turns all the lines into a list
        where_idx = self.find_idx(curr[0], where)  # finds the index where the variable that needs to check is
        count = 0
        for line in curr[1:]:
            if operation == '==':  # checks if operation is equal because of differences in float and strings
                if eval('line[where_idx]' + operation + 'var'):  # eval turns string into a logic comparison
                    count += 1
                    continue
                else:
                    res.append(line)
            elif operation == '!=':  # checks if operation is not equal because of differences in float and strings
                if eval('line[where_idx]' + operation + 'var'):
                    res.append(line)
                else:
                    count += 1
            else:  # checks if operation is equal because of differences in float and strings
                if eval('float(line[where_idx])' + operation + 'float(var)'):  # greater or less than operations for num
                    count += 1
                    continue
                else:
                    res.append(line)
        return res, count

    def select_specific(self, var, table, where):
        """
        Selects a specific row depending on the where condition and the variables it wants to see.
        First deletes the the values that depend on the where clause. Then goes through and deltes the columns
        that are not needed to be seen.
        :param var: contains the variable for the where clause
        :param table: contains the name of the table in string
        :param where: contains the string of the conditions that needs to be satisfied
        :return:
        """
        obj = where[1]
        op = where[2]
        w = where[3][:-1]
        path = os.path.join(self.dbDir, table)
        if os.path.exists(path):  # check if path exists
            data = self.read_all(path)
            missing = []
            variables = self.get_curr_var(data[0])
            for i in range(len(var)):
                var[i] = var[i].replace(',', '')  # gets rid of all commas
            for v in variables:
                if v not in var:  # checks if the variable needs to be seen
                    missing.append(v)
            res = self.select_specific_helper(path, missing, obj, op, w)  # calls helper to delete rows and cols
            for line in res:
                print("|".join(line))
        else:
            output = '!Failed to select items in table ' + table + ' because it does not exist.'
            print(output)

    def select_specific_helper(self, path, missing, obj, op, w):
        """
        It will call the delete helper to get rid of rows that don't have the specific value.
        Finds the missing values that are not needed to be displayed. It will delete those columns that are not
        needed.
        :param path: String with Path to the table
        :param missing: Contains the list of values you want
        :param obj: the object that wants to be found
        :param op: the logic operator
        :param w: the values that needs to be compared with the operator
        :return: return the list that needs to be inputted into the file
        """
        res = []
        data, count = self.delete_helper(path, obj, op, w)  # delete specific rows that satisfy condition
        for line in data:
            new = "| ".join(line)
            res.append(new.split('| '))
        for miss in missing:
            where_idx = self.find_idx(res[0], miss)
            for line in res:
                del line[where_idx]  # deletes the column from all the lines
        return res

    def transaction(self):

        print('Transaction starts.')
        self.get_locked()
        path = None
        lock_path = None

        self.lock = True
        while self.lock:
            command = self.get_input()
            command = re.sub(r"[\n\t]*", "", command)  # removes random special characters like tabs
            l = command.split(' ')  # splits the string command into a list based on spaces
            command = command.upper()  # converts the command to all uppercase so it can cover case sensitivity
            size = len(l)  # gets length to handle missing spaces

            if 'UPDATE' in command:
                if size >= 8:  # checks if the minimum amount of variables are present
                    tbl = l[1]
                    if tbl.upper() in self.lockedTables:
                        print('Error: Table ' + l[1] + ' is locked!')
                        return
                    path = os.path.join(self.dbDir, tbl.upper())
                    lock_path = os.path.join(self.dbDir, tbl.upper() + '_LOCK')
                    copyfile(path, lock_path)
                    self.update_table(tbl.upper() + '_LOCK', l[2:])
                else:
                    print('Syntax Error:', command)  # if size does not match there has to be a syntax error with cmd
            elif 'COMMIT' in command:
                self.commit(path, lock_path)
                self.lock = False
            else:
                print('Syntax Error: Not a Update Command | ', command)
        return

    @staticmethod
    def commit(path, lock_path):
        copyfile(lock_path, path)
        os.remove(lock_path)  # deletes the locked path
        print("Transaction committed.")

    @staticmethod
    def read_all_list(data):
        """
        Turns a string into a list
        :param data: Data with strings in list
        :return: return a list with the strings separated into lists
        """
        curr = []
        for line in data:
            curr.append(line.split('|'))
        return curr

    @staticmethod
    def get_curr_var(data):
        """
        Splits the input data and removes commas in list leaving only the variable names
        :param data: List of data from the file
        :return: A new list that contains only the variable names
        """
        res = []
        new = data.split('| ')  # splits into list by '|'
        for var in new:
            s = var.split(' ')  # splits into a list generated by spaces
            s[0] = s[0].replace(',', '')  # removes commas
            res.append(s[0])
        return res

    @staticmethod
    def find_idx(inp, var):
        for i in range(len(inp)):
            if var in inp[i]:
                return i
        return -1

    @staticmethod
    def get_input():
        command = input('Enter Update or Commit Command: ')
        if '--' in command:  # removes comments at end of line
            command = command[:command.index('--')-1]
        return command

    def get_locked(self):
        arr = os.listdir(self.dbDir)
        for tbl in arr:
            if 'LOCK' in tbl:
                self.lockedTables.append(tbl[:-5])

