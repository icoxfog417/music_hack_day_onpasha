import os
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.escape
import api.photo2song as p2s
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


class BaseHandler(tornado.web.RequestHandler):
    MACHINE_SESSION_KEY = "photo_mood"


class PhotoToSongHandler(BaseHandler):

    def post(self):
        image_url = self.get_argument("image_url", default="")
        image_urls = self.get_arguments("image_urls[]")

        if len(image_urls) == 0:
            image_urls = [image_url]

        result = {}
        try:
            result = p2s.convert(image_urls)
        except Exception as ex:
            print(ex)

        self.write(result)
