from application import app, db
from application.models import Recipe, Alcohol

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Recipe': Recipe, 'Alcohol': Alcohol}