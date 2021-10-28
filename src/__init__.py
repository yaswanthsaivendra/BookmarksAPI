from flask import Flask, jsonify
import os
from werkzeug.utils import redirect
from src.bookmarks import bookmarks
from src.database import Bookmark, db
from src.auth import auth
from flask_jwt_extended import JWTManager




def create_app(test_config=None):
    app = Flask(__name__,
     instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY")

        )

    else:
        app.config.from_mapping(test_config)

    db.app=app
    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)


    @app.get('/<short_url>')
    def redirect_to_url(short_url):
        bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()

        if bookmark:
            bookmark.visits=bookmark.visits+1
            db.session.commit()
            return redirect(bookmark.url)

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({'error':'Not found'}), 404

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({'error':'Something went wrong, Please try after some time'}), 500




    return app