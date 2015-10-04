# [Onpasha](http://hacklog.jp/works/3391) API Server

Onpasha converts image to song.

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

![architecture](./architecture.png)

* Recognize the image by [Bluemix Vision Recognizer](http://visual-recognition-demo.mybluemix.net/)
* Convert image to echonest's mood by machine learning ([scikit-learn](http://scikit-learn.org/))
* Search tracks by mood by [echonest](http://developer.echonest.com/)
* Get track's preview url or some information from [Spotify](https://developer.spotify.com/)
* ([Pepper](http://www.softbank.jp/robot/special/pepper/) sings a song)
* (Share songs by [SendGrid](https://sendgrid.kke.co.jp/))

Now, you can listen your photo image!

## Setting

Please prepare the `environ.yaml` at the project root.

```
vision_recognize_user: your_username
vision_recognize_pass: your_password
echonest_api_key: your_key
spotify_client_id : your_client_id
spotify_client_secret : your_client_secret
```

And `SECRET_TOKEN` to encrypt coolie.
