from os import path
from jinja2 import FileSystemLoader, Environment

template_dir = path.join(path.dirname(__file__), 'templates')

jinja_env = Environment(loader = FileSystemLoader(template_dir))
