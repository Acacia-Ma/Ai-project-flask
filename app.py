from App import create_app

# 启动APP
app = create_app()
#FBV是什么？函数视图
#CBV是什么？类视图

if __name__ == '__main__':
    app.run()
