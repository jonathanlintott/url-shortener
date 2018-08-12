from application import app, db
from application.models import UrlPair


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'UrlPair': UrlPair}
