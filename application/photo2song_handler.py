import tornado.web
import api.photo2song as p2s


class BaseHandler(tornado.web.RequestHandler):

    def get_image_urls(self):
        image_url = self.get_argument("image_url", default="")
        image_urls = self.get_arguments("image_urls[]")

        if len(image_urls) == 0 and image_url:
            image_urls = [image_url]
        elif self.request.body:
            import json
            body = json.loads(self.request.body.decode("utf-8"))
            if "image_urls" in body:
                image_urls = body["image_urls"]
            elif "image_url" in body:
                image_urls = [body["image_url"]]
        else:
            image_urls = []

        return image_urls


class PhotoToSongHandler(BaseHandler):

    def post(self):
        image_urls = self.get_image_urls()
        result = {}
        try:
            result = p2s.convert(image_urls)
        except Exception as ex:
            print(ex)

        self.write(result)
