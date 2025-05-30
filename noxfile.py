import nox


# Test on django 5.2, EOL April 2028
@nox.session(python=['3.10', '3.11', '3.12', '3.13'])
def test520(session):
    session.install('django>=5.2,<6.0')
    session.install('-e', '.')
    session.run('./runtests.py', external=True)
