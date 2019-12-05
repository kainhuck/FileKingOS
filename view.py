'''
视图
'''

def printLogin():
    '''
    打印登录界面
    '''
    username = input("FKOS login: ")
    password = input("Password: ")

    return username, password

if __name__ == "__main__":
    printLogin()