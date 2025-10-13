from comunidadeimpressionadora import app, database
#
# with app.app_context():
#     database.create_all()


with app.app_context():
    database.drop_all()
    database.create_all()
    database.session.commit()