SECRET_KEY = "alura"

SQLALCHEMY_DATABASE_URI = \
    'mysql+mysqlconnector://{usuario}:{senha}@{servidor}/{database}'.format(
        usuario='root',
        senha='admin',
        servidor='127.0.0.1',
        database='jogoteca'
    )
