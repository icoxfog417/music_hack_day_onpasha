# [Onpasha](http://hacklog.jp/works/3391) API Server

Image to Song API Server

* Convert image to [Gracenote](https://developer.gracenote.com/ja/web-api?language=ja)'s mood by scikit-learn
* Get artists info from [LiveFans](http://www.livefans.jp/)
* Get tracks by mood and artists (Gracenote).
* Get track's lyric by [PetitLyrics](http://petitlyrics.com/)
* Build new Lyric from it.
* Convert lyric to song by [YAMAHA VOCALODUCER](http://jp.yamaha.com/news_release/2013/13102104.html)
* ([Pepper](http://www.softbank.jp/robot/special/pepper/) sings a song)
* (Share songs by [SendGrid](https://sendgrid.kke.co.jp/))

Now, you can here your photo image!

## Setting

Please prepare the `environ.yaml` at the project root.

```
yamaha_key: your_ke
yamaha_ver: your_ke
rekognition_key: your_ke
rekognition_secret: your_ke
gracenote_client_id: your_ke
gracenote_user_id: your_ke
livefan_client_id: your_ke
petitlyrics_auth_key: your_ke
```
