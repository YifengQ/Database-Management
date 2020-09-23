__author__ = "Yifeng Qin"
__class__ = "CS457 Database Management Systems"
__instructor__ = "Dongfang Zhao"
__university__ = "University of Nevada Reno"
__assignment__ = "Project 1"
__date__ = "9/15/2020"

import os


class RunScript:

    def __init__(self):
        """
        Gets the current working directory and initializes variables
        """
        self.parentDir = os.getcwd()
        self.dbDir = None
        self.data = []

    def create_database(self, db):
        """
        Joins the parent directory with the entered database. Checks if the database already exists, and will either
        error out or create that database.
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

    def create_table(self, inp):
        """
        Gets the path to that table and will check if that already exists. Then if it does not exist, it will change the
        directory and call a helper function to append data to the table.
        :param inp: Contains all the data that will be entered into the table
        :return: None
        """
        tbl = inp[0]
        path = os.path.join(self.dbDir, tbl)  # joins cwd and db name
        if os.path.exists(path):   # check if path exists
            output = '!Failed to create table ' + tbl + ' because it already exists.'
            print(output)
        else:
            os.mknod(path)  # creates file system of path
            output = 'Table ' + tbl + ' created.'
            self.tbl_helper(inp, path)  # calls helper to write to table
            print(output)

    def select_all(self, table):
        """
        Checks if the table exists and then reads all the data from the file and prints it out.
        :param table: String that contains name of the table
        :return:
        """
        path = os.path.join(self.dbDir, table)  # joins cwd and db name
        if os.path.exists(path):  # check if path exists
            with open(path) as file_in:  # starts reading from file
                for line in file_in:
                    self.data.append(line.rstrip())
            for line in self.data:  # prints data to terminal
                print(line)
            self.data = []
        else:
            output = '!Failed to query table ' + table + 'because it does not exist.'
            print(output)

    #  "a" - Append
    #  "w" - Write

    def tbl_helper(self, inp, path):
        """
        Gets the path to the table and opens it to be written too. Then it will splice the data so the extra character
        from the raw input are not there.
        :param inp: The variables that need to be written
        :param path: String with table path
        :return: None
        """
        f = open(path, "a")  # opens file
        var = []
        for i in range(1, len(inp), 2):
            if i == 1:  # has different extra character at beginning
                var.append(inp[i][1:] + ' | ' + inp[i+1][:-1])  # splice off extra characters,concatenate back together
            elif i == len(inp) - 2:  # has different extra character at end
                var.append(inp[i] + ' | ' + inp[i + 1][:-2])
            else:
                var.append(inp[i] + ' | ' + inp[i+1][:-1])
        f.write(str(var))  # write to file
        f.close()  # close file

    def alter_table(self, inp):

        tbl = inp[0]
        var = inp[1:]
        path = os.path.join(self.dbDir, tbl)  # joins cwd and db name
        if os.path.exists(path):  # check if path exists
            f = open(path, "a")  # opens file
            f.write(str(var))
            f.close()  # close file
            output = 'Table ' + tbl + ' modified.'
            print(output)
        else:
            output = '!Failed to alter table ' + tbl + ' because it does not exist'
            print(output)

    def drop_table(self, tbl):
        path = os.path.join(self.dbDir, tbl)  # check if path exists
        if os.path.exists(path):  # check if path exists
            cmd = 'rm ' + '-rf ' + path  # concatenate command to run
            os.system(cmd)  # runs the command
            output = 'Table ' + tbl + ' deleted.'
            print(output)
        else:
            output = '!Failed to delete ' + tbl + ' because it does not exists.'
            print(output)


# script = RunScript()
#
# # script.create_database('db_1;')
# # #script.drop_database('db_1;')
# script.use_database('db_1;')
# script.create_table(['tbl_1', '(a1', 'int,', 'a2', 'varchar(20));'])
# script.select_all('tbl_1')