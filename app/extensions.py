from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flasgger import Swagger

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
swagger = Swagger()