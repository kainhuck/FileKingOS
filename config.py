'''
项目配置文件
'''

from utils import Folder, User

# 根目录
root = Folder('/', '/')

rootUser = User('root', '1', Folder('root', root))
root.folderList.append(rootUser.home)

userGroup = {
    rootUser.username: rootUser
}

