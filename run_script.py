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

    def create_table(self, tbl, inp):
        """
        Gets the path to that table and will check if that already exists. Then if it does not exist, it will change the
        directory and call a helper function to append data to the table.
        :param tbl:
        :param inp: Contains all the data that will be entered into the table
        :return: None
        """
        path = os.path.join(self.dbDir, tbl)  # joins cwd and db name
        if os.path.exists(path):   # check if path exists
            output = '!Failed to create table ' + tbl + ' because it already exists.'
            print(output)
        else:
            os.mknod(path)  # creates file system of path
            out = inp.split(',')
            out = "|".join(out)
            f = open(path, "a")  # opens file
            f.write(out)  # write to file
            f.close()  # close file
            output = 'Table ' + tbl + ' created.'
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
            output = '!Failed to query table ' + table + ' because it does not exist.'
            print(output)

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


# script = RunScript()
#
# # script.create_database('db_1;')
# # #script.drop_database('db_1;')
# script.use_database('db_1;')
# script.create_table(['tbl_1', '(a1', 'int,', 'a2', 'varchar(20));'])
# script.select_all('tbl_1')