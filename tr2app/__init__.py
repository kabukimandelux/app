from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm
#from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'etewfwfv87hf29383fzh2nfiwjf32'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Kabuk318@localhost/tr2'
db = SQLAlchemy(app)
#migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category ='info'

WTF_CSRF_TIME_LIMIT= None

from tr2app import routes
