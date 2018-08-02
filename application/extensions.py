from application.models.system_user import SysUser

if __name__ == '__main__':
    # print(SysUser.verify('test', '123'))
    email = 'test@fgg{}.com.{}'
    mail_body = '''
            <h3>亲爱的用户：</h3>
            <p>请您在24小时之内点击下面的链接修改登录密码</p>
            <p><a href="http://127.0.0.1:8080/sysadmin/password_change?sid={}" %(reset_link)>http://127.0.0.1:8080/sysadmin/password_change?sid={}</a></p>
            <p>若链接点击无效，请复制链接到浏览器地址栏打开</p>
            <p>若您未申请密码修改，请忽略此邮件</p>
            '''

    print(mail_body.format('qq', 163))