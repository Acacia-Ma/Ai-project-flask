import datetime
DB_DATABASE_NAME="mysql"
DB_DRIVER="pymysql"
DB_USERNAME="root"
DB_PASSWORD=123456
DB_NAME="db"
DB_HOST="localhost"
DB_PORT=3306

#格式："mysql+driver://username:password@host:port/name"
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}".format(DB_DATABASE_NAME,DB_DRIVER,DB_USERNAME,
                                                          DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)
# 配置私钥
JWT_SECRET_KEY = "Acacia_Ma"
# 配置token过期时间
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=5)
# 配置刷新token过期时间
JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(hours=24)