import os
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.escape
from tornado.options import define, options
from machines.photo_mood.validator import Validator
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


class FeedbackHandler(BaseHandler):

    def post(self):
        data = self.get_arguments("data[]")
        result = ""

        feedback = Validator.validate_feedback(data)
        if len(feedback) > 0:
            MachineLoader.feedback(machines.photo_mood, feedback)
        else:
            result = "feedback format is wrong."

        resp = {"result": result}
        self.write(resp)


class Application(tornado.web.Application):

    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/photo2song", PhotoToSongHandler),
            (r"/feedback", FeedbackHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
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
