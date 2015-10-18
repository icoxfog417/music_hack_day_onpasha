import os
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.escape
from application.photo2song_handler import PhotoToSongHandler
from application.dummy import DummyHandler


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/photo2song", PhotoToSongHandler),
            (r"/photo2songd", DummyHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret=os.environ.get("SECRET_TOKEN", "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"),
            debug=True,
        )
        # xsrf_cookies=True,

        super(Application, self).__init__(handlers, **settings)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", title="title")
