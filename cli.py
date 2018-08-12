import unittest
import os

from application import app, db
from application.models import UrlPair


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'UrlPair': UrlPair}


@app.cli.command()
def test():
    """Run the unit tests."""
    test_dir = os.path.join('application', 'tests')
    tests = unittest.TestLoader().discover(test_dir)
    unittest.TextTestRunner(verbosity=2).run(tests)
