class User(object):
    '''
    用户
    '''

    def __init__(self, name, passwd, home):
        self.username = name
        self.home = home
        self.password = passwd


class File(object):
    '''
    普通文件
    '''

    def __init__(self, name):
        self.name = name
        self.status = 0
        self.content = None

    def write(self):
        pass

    def open(self):
        pass


class Folder(object):
    '''
    文件夹
    '''

    def __init__(self, name, father):
        self.name = name    # 文件夹名称
        self.fileList = []  # 普通文件
        self.folderList = []    # 文件夹
        self.fatherFolder = father  # 父目录

    def delete(self, item):
        if isinstance(item, File):
            self.fileList.remove(item)
        else:
            self.folderList.remove(item)

    def show(self):
        i = 0
        for each in self.fileList:
            print(each.name+':-', end="  ")
            i += 1
            if i % 5 == 0:
                print()

        for each in self.folderList:
            print(each.name+':d', end="  ")
            i += 1
            if i % 5 == 0:
                print()

        if i % 5:
            print()

    def getpwd(self):
        '''
        打印出当前目录在目录树中的位置:
        '''
        pwdString = self.name
        upFolder = self.fatherFolder
        while upFolder.name != '/':    # 如果不是根目录继续往上
            # 先拼接
            pwdString = upFolder.name + '/' + pwdString
            upFolder = upFolder.fatherFolder
        pwdString = '/' + pwdString
        return pwdString