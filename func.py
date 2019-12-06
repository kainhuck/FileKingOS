'''
逻辑函数
'''
from utils import Folder, File, User
from config import userGroup, root, userGroup


def checkPass(username, password):
    '''
    检查登录
    '''
    try:
        if userGroup.get(username, None).password == password:
            return userGroup.get(username, None)
        else:
            return False
    except:
        return False


def touch(filename, folder):
    '''
    创建文件
    '''
    if len(filename):
        file = File(filename)
        folder.fileList.append(file)
    else:
        print("文件名为空")


def rm(filename, folder):
    '''
    删除文件（夹）
    '''
    flag = False    # 查找标记
    # 判断删除文件（filename）类型
    # 从folder列表中删除
    for each in folder.fileList:
        if each.name == filename:
            flag = True
            folder.fileList.remove(each)
            break

    for each in folder.folderList:
        if each.name == filename:
            flag = True
            yesOrNo = input("这是一个文件夹，你确定要删除吗[y/n]:")
            if yesOrNo in ('Y', 'y', 'yes', 'Yes'):
                folder.folderList.remove(each)
            elif yesOrNo in ('N', 'n', 'No', 'no'):
                print("已经取消删除")
            else:
                print("未知输入")
            break
    if not flag:
        print("文件不存在")


def cat(filename, folder):
    '''
    展示文件内容
    '''
    # 先在folder中找到名为filename的文件
    for each in folder.fileList:
        if each.name == filename:
            print(each.content)
            break
    else:
        print("没有名为< \033[31m{}\033[0m >的文件, 可以使用命令< \033[31mtouch {}\033[0m >创建".format(
            filename, filename))


def edit(filename, folder):
    '''
    文件编辑
    '''
    # 先找到文件
    for each in folder.fileList:
        if each.name == filename:
            print("\033[30m当前正在编辑 \033[33m{} \033[30m文件，输入< \033[33mexit \033[30m>退出编辑\033[0m".format(
                filename))
            lines = []
            while True:
                line = input()
                if line == 'exit':
                    break
                lines.append(line)
            each.content = '\n'.join(lines)
            print("\n\033[30m编辑结束\033[0m")
            break
    else:
        print("没有名为< \033[31m{}\033[0m >的文件, 可以使用命令< \033[31mtouch {}\033[0m >创建".format(
            filename, filename))


def mkdir(filename, folder):
    '''
    新建文件夹
    '''
    if "/" in filename:
        print("Error: there is '/' in folderName, however it's not allowed")
    elif filename in ('..', '.', '-', '~'):
        print(
            "Error: the name \033[31m{}\033[0m is not allowed".format(filename))
    else:
        if len(filename):
            file = Folder(filename, folder)
            folder.folderList.append(file)
        else:
            print("文件名为空")
    # return folder


def cd(filename, folder, user):
    '''
    切换路径
    '''
    oldFolder = folder  # 保存断点

    folderList = filename.split("/")
    start = folderList[0]  # 开始位置 '' : 根目录; '.' : 当前目录; '..' : 上级目录
    if len(folderList) == 2 and start == '' and folderList[1] != user.username:
        print("不能进入别人的目录")
        return folder
    if start == '':  # 根目录
        folder = root
        if filename != '/':
            for eachFolderName in folderList[1:]:
                for each in folder.folderList:
                    if each.name == eachFolderName:
                        folder = each
                        break
                else:
                    folder = oldFolder
                    print("路径不存在")
                    break
        else:
            folder = oldFolder
            print("不允许进入根目录")
    elif start == '.':  # 当前目录
        for eachFolderName in folderList[1:]:
            for each in folder.folderList:
                if each.name == eachFolderName:
                    folder = each
                    break
            else:
                folder = oldFolder
                print("路径不存在")
                break
    elif start == '..':  # 上级目录
        for eachFolderName in folderList:
            if eachFolderName == '..':
                if folder.fatherFolder.name != '/':
                    folder = folder.fatherFolder
                else:
                    folder = oldFolder
                    print("不允许进入根目录")
                    break
            else:
                for each in folder.folderList:
                    if each.name == eachFolderName:
                        folder = each
                        break
                    else:
                        folder = oldFolder
                        print("路径不存在")

    else:   # 也是当前目录
        for eachFolderName in folderList:
            for each in folder.folderList:
                if each.name == eachFolderName:
                    folder = each
                    break
            else:
                folder = oldFolder
                print("路径不存在")

    return folder


def useradd(username, password):
    '''
    新建用户
    '''
    # 新建用户的本质是在 / 下 创建一个家目录
    # 搜索该用户名是否已经存在
    for each in userGroup.keys():
        if each == username:
            print("该用户名已经存在")
            return

    newUser = User(username, password, Folder(username, root))  # 创建新用户
    root.folderList.append(newUser.home)    # 将新用户家目录添加进根目录
    userGroup[username] = newUser   # 加入组
    print("创建成功")


def chroot(username, password):
    '''
    切换用户
    '''
    for each, value in userGroup.items():
        if each == username:
            if value.password == password:
                # print("success!")
                return value
            else:
                print("Incorrect password")
            break
    else:
        print("该用户不存~")
    return False


# 命令函数对应表
parseCmd = {
    'touch': touch,
    'rm': rm,
    'cat': cat,
    'edit': edit,
    'mkdir': mkdir
}

# 这里的函数操作需要两个参数：


def cp(filename, pwd, folder, user):
    '''
    复制文件
    '''
    if pwd == '/':
        print("不能将文件复制到根目录")
        return
    folderList = pwd.split("/")
    oldFolder = folder
    newname = folderList.pop(-1)    # 最后一个默认是新文件名
    if not len(newname):
        print("目标文件名不能为空")
        return
    if not len(folderList):  # 当前文件夹下
        # 判断重名
        for each in folder.fileList:
            if each.name == newname:
                print("文件重名")
                return

        # 找到要复制的文件
        for each in oldFolder.fileList:
            if each.name == filename:
                # 新建文件
                file = File(newname)
                file.content = each.content
                folder.fileList.append(file)
                break
        else:
            print("文件不存在")

        return

    # 其他情况，
    # 先切换到目标目录
    pwd = pwd[:pwd.rfind(newname)-1]
    if not len(pwd):    # 此时说明在根目录下
        print("不能将文件复制到根目录下")
        return
    folder = cd(pwd, folder, user)
    # 再复制文件
    # 判断重名
    for each in folder.fileList:
        if each.name == newname:
            print("文件重名")
            return

    # 找到要复制的文件
    for each in oldFolder.fileList:
        if each.name == filename:
            # 新建文件
            file = File(newname)
            file.content = each.content
            folder.fileList.append(file)
            break
    else:
        print("文件不存在")

    return


def mv(filename, pwd, folder, user):
    '''
    移动文件
    '''
    if pwd == '/':
        print("不能将文件复制到根目录")
        return
    oldFolder = folder  # 保存断点
    folderList = pwd.split("/")
    newname = folderList.pop(-1)    # 最后一个默认是新文件名
    if not len(newname):
        print("目标文件名不能为空")
        return
    if not len(folderList):  # 当前文件夹下
        # 判断重名
        for each in folder.fileList:
            if each.name == newname:
                print("文件重名")
                return

        # 找到要复制的文件
        for each in oldFolder.fileList:
            if each.name == filename:
                # 新建文件
                file = File(newname)
                file.content = each.content
                folder.fileList.append(file)

                # 删除原文件
                oldFolder.fileList.remove(each)
                break
        else:
            print("文件不存在")

        return

    # 其他情况，
    # 先切换到目标目录
    pwd = pwd[:pwd.rfind(newname)-1]
    if not len(pwd):    # 此时说明在根目录下
        print("不能将文件复制到根目录下")
        return folder
    folder = cd(pwd, folder, user)
    # 再复制文件
    # 判断重名
    for each in folder.fileList:
        if each.name == newname:
            print("文件重名")
            return

    # 找到要复制的文件
    for each in oldFolder.fileList:
        if each.name == filename:
            # 新建文件
            file = File(newname)
            file.content = each.content
            folder.fileList.append(file)
            # 删除原文件
            oldFolder.fileList.remove(each)
            break
    else:
        print("文件不存在")

    return


def usage():
    '''
    使用说明
    '''
    print("""
使用说明：命令  参数

普通文件操作
创建文件：touch <filename>
删除文件：rm <filename>
查看文件：cat <filename>
编辑文件：edit <filename>
复制文件: cp <filename> <pwd>
移动文件: mv <filename> <pwd>

文件夹操作
新建文件夹：mkdir <foldername>
删除文件夹: rm <foldername>
切换文件夹: cd <pwd>

用户操作
新建用户: useradd <username>
切换用户: chroot <username>

其他
当前路径: pwd
查看帮助: help
列出文件: ls
清空屏幕: clear
退出: exit
    """)


def neofetch():
    '''
    打印系统信息
    '''
    print('''
\033[30m  ________ ___  ___  ________  ___  __            ________  ________      
\033[31m |\\  _____\\\\  \\|\\  \\|\\   ____\\|\\  \\|\\  \\         |\\   __  \\|\\   ____\\     
\033[32m \\ \\  \__/\\ \\  \\\\\\  \\ \\  \\___|\\ \\  \\/  /|_       \\ \\  \\|\\  \\ \\  \\___|_    
\033[33m  \\ \\   __\\\\ \\  \\\\\\  \\ \\  \\    \\ \\   ___  \\       \\ \\  \\\\\\  \\ \\_____  \\   
\033[34m   \\ \\  \\_| \\ \\  \\\\\\  \\ \\  \\____\\ \\  \\\\ \\  \\       \\ \\  \\\\\\  \\|____|\\  \\  
\033[35m    \\ \\__\\   \\ \\_______\\ \\_______\\ \\__\\\\ \\__\\       \\ \\_______\\____\\_\\  \\ 
\033[36m     \\|__|    \\|_______|\\|_______|\\|__| \\|__|        \\|_______|\\_________\\
                                                             \\|_________|
\033[32m    OS: \033[34mFKOS
\033[32m    shell: \033[34mkush 1.0
\033[32m    author_: \033[34mkainhuck                                                              
\033[0m                                          
    ''')


if __name__ == "__main__":
    neofetch()
