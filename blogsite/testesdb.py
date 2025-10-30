from blogsite import app, database
#
# with app.app_context():
#     database.create_all()


# with app.app_context():
#     database.drop_all()
#     database.create_all()
#     database.session.commit()


# with app.app_context():
#     usuario = Usuario.query.first()
#     if usuario:
#         token = usuario.reset_senha()
#         print(f"Token: {token}")
#
#         usuario_verificado = Usuario.verificacao_reset_token(token)
#         print(f"Usuário verificado: {usuario_verificado}")