"""
 Created by ldh on 19-11-26
"""
from flask import Flask

__author__ = "ldh"

app = Flask(__name__)


# MVC 设计模式里面的 C
@app.route('/hello')  # .route() 其实就是内部调用了 add_url_rule 方法
def hello():
    return 'Hello, World'


# 路由的另一种注册方法, 在基于类的视图情况下使用这个方法
# app.add_url_rule('/hello', view_func=hello)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug='True')
