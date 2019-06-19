import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    # structure: first a os defined variable, thereafter a backup (used local dev)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'NmP$UfnNl43933gvWbAI$Vy30nJ4Pw^X*UKfgsq11#Lzo@SizA@'
    # this is a development key
    SQLALCHEMY_DATABASE_URI =  os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False # no warnings for all changes
    SQLALCHEMY_ECHO = False # shows all SQL translations
    # settings not present => no mail (as there are no backup values)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = []