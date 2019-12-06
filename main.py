'''
程序运行文件
'''

from view import *
from func import parseCmd, cd, checkPass, usage, useradd, chroot, cp, mv, neofetch
from config import userGroup
import os
import time

# 常量定义
clearSin = 'cls'    # 清屏命令
user = None  # 当前用户
here = None  # 当前所在文件夹

os.system(clearSin)

# 登录
print("\n  File King Operating System 0.0.1-by-kainhuck \n")

while True:
    username, password = printLogin()
    user = checkPass(username, password)
    if user:
        break

here = user.home

print("Welcome to kush, the shell made by Kainhuck")


def main():
    global here
    global user
    global clearSin
    while True:
        cmd = input("\033[33m{username}\033[30m@\033[31mFKOS \033[30m~\033[36m{time}\033[30m -> \033[34m{pwd} \033[0m> ".format(
            username=user.username, time=str(time.ctime()), pwd=here.getpwd()))
        if len(cmd) == 0:
            continue
        if cmd == 'help':
            usage()
        elif cmd == 'exit':
            print("bye~")
            break
        elif cmd == 'neofetch':
            neofetch()
            continue
        elif cmd == 'ls':
            here.show()
        elif cmd == 'clear':
            os.system(clearSin)
        elif cmd == 'pwd':
            print(here.getpwd())
        else:
            # 这里的命令都有参数
            cmd_list = cmd.split(" ")
            try:
                cmd = cmd_list[0]
                arg = cmd_list[1]
            except:
                print("Incorrect input format!")
                continue

            if cmd == 'cd':
                here = cd(arg, here, user)
            elif cmd == 'useradd':
                password = input("Please input password:")
                checkPas = input("Please repeat your password:")
                if password == checkPas:
                    useradd(arg, password)
                else:
                    print("Incorrect password!")
            elif cmd == 'chroot':
                password = input("Please input password:")
                temp = chroot(arg, password)
                if temp:
                    user = temp  # 更改当前用户
                    here = user.home
                    os.system(clearSin)
                    print("Welcome to kush, the shell made by Kainhuck")
            elif cmd == 'cp':
                try:
                    cp(arg, cmd_list[2], here, user)
                except:
                    print("Incorrect input format!")
            elif cmd == 'mv':
                try:
                    mv(arg, cmd_list[2], here, user)
                except:
                    print("Incorrect input format!")
            else:
                parse = parseCmd.get(cmd, None)
                if parse:
                    parse(arg, here)
                else:
                    print(
                        "The unknown command => \033[31m{}\033[0m".format(cmd))
                    continue


if __name__ == "__main__":
    main()
