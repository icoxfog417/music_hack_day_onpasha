import os
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.escape
from tornado.options import define, options
import machines.photo_mood
from machines.photo_mood.validator import Validator
from api.rekognition import Rekognition
from envs import get_env


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", title="title")


class BaseHandler(tornado.web.RequestHandler):
    MACHINE_SESSION_KEY = "photo_mood"

class PredictionHandler(BaseHandler):

    def post(self):
        image_url = self.get_argument("image_url", default="")
        image_urls = self.get_arguments("image_urls[]")
        rekognizer = Rekognition()

        if len(image_urls) == 0:
            image_urls = [image_url]

        moods = rekognizer.images_to_mood(image_urls)

        # gracenote api


        # get lyric

        # build lyric

        # make mp3 song

        self.write(
            {"mp3_url": ""}
        )


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
            (r"/predict", PredictionHandler),
            (r"/feedback", FeedbackHandler),
        ]

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            xsrf_cookies=True,
            debug=True,
        )

        super(Application, self).__init__(handlers, **settings)


def main():
    # tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    port = int(os.environ.get("PORT", options.port))
    print("server is running on port {0}".format(port))
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(ex)
