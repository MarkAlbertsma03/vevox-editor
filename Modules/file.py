import json as js
import os
import shutil as sh

cwd = os.getcwd()

class File(object):
    
    def __init__(self, path):
        self.path = path
        self.folder = os.path.dirname(path)
        self.filename = os.path.basename(path)
    
    def __repr__(self):
        return self.path
    
    def rename(self, filename):
        new_path = os.path.join(self.folder, filename)
        os.rename(self.path, new_path)
        self.__init__(new_path)
    
    def move(self, path):
        if self.filename != os.path.basename(path):
            raise ValueError("filename must match its previous one")
        os.rename(self.path, path)
        self.__init__(path)
    
    def move_down(self, folders, create_folders = True):
        if not isinstance(folders, list):
            raise TypeError("folder names can only be in a list")
        new_folder = self.folder
        for folder in folders:
            new_folder = os.path.join(new_folder, folder)
        if not os.path.exists(new_folder) and not create_folders:
            raise FileNotFoundError("directory does not exist")
        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        new_path = os.path.join(new_folder, self.filename)
        os.rename(self.path, new_path)
        self.__init__(new_path)
    
    def move_up(self, amount):
        if not isinstance(amount, int):
            raise TypeError("'amount' must be an integer")
        for x in range(amount):
            self.move(os.path.join(os.path.dirname(self.folder), self.filename))
    
    def exists(self):
        return os.path.exists(self.path)
    
    def delete(self):
        os.remove(self.path)

class Folder(File):
    
    def delete(self):
        sh.rmtree(self.path)

class TXT(File):
    
    def read(self):
        with open(self.path, "r", encoding = "utf-8") as file:
            lines = file.readlines()
        for x in range(len(lines)):
            lines[x] = lines[x][:-1]
        return lines

    def write(self, lines):
        with open(self.path, "w", encoding = "utf-8") as file:
            file.writelines("\n".join(lines))

    def rewrite(self, index, line):
        lines = self.read()
        lines[index - 1] = line
        self.write(lines)

class JSON(File):
    
    def read(self):
        with open(self.path, "r", encoding = "utf-8") as file:
            lines = file.readlines()
        return js.loads(lines[0])
