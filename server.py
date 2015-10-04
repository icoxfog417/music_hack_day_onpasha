import os
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.escape
import api.photo2song as p2s
from envs import get_env


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


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/photo2song", PhotoToSongHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret=os.environ.get("SECRET_TOKEN", "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"),
            debug=True,
        )
        # xsrf_cookies=True,

        super(Application, self).__init__(handlers, **settings)


def main():
    # tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    port = 8000 if not get_env("port") else int(get_env("port"))
    print("server is running on port {0}".format(port))
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(ex)
