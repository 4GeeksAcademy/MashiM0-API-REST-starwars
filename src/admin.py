import os
from flask_admin import Admin
from models import db, User, People, Planet, PeopleFavorites, PlanetFavorites
from flask_admin.contrib.sqla import ModelView

class UserView(ModelView):
    column_list = ["id","email","password","is_active","people_favorites_associates","planet_favorites_associates"]

class PeopleView(ModelView):
    column_list = ["id","name","height","user_favorite_associates"]

class PlanetView(ModelView):
    column_list = ["id","name","size","user_favorite_associates"]

class PeopleFavoritesView(ModelView):
    column_list = ["id","user_id","user","character_id","character"]

class PlanetFavoritesView(ModelView):
    column_list = ["id","user_id","user","planet_id","planet"]

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(UserView(User, db.session))
    admin.add_view(PeopleView(People, db.session))
    admin.add_view(PlanetView(Planet, db.session))
    admin.add_view(PeopleFavoritesView(PeopleFavorites, db.session))
    admin.add_view(PlanetFavoritesView(PlanetFavorites, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))