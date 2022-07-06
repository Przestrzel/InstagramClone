from flask 4import Blueprint

bp = Blueprint('errors', __name__)

from app.errors import handlers
