import os

def load_html(name):
    filepath = os.path.join(os.path.dirname(__file__), '..', 'fixtures', name + '.html')
    with open(filepath, 'r') as f:
        html = f.read()

    return html