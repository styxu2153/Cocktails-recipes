from application import app, db

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True,  unique=True)
    ingredients = db.Column(db.String(256), index=True)
    need_for_shaker = db.Column(db.Boolean, default=False)
    
    def __init__(self, name: str, ingredients: str, need_for_shaker):
        self.name = name
        self.ingredients = ingredients
        self.need_for_shaker = need_for_shaker
    
    def __repr__(self):
        return '<Recipe {}>'.format(self.name)

class Alcohol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    
    def __repr__(self):
        return '<Alcohol {}>'.format(self.name)
    