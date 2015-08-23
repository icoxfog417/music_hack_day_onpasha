from api.rekognition import Rekognition
from api.gracenote import Gracenote
from api.livefans import LiveFans
from api.petitlyrics import Petitlyrics
from api.yamaha import Yamaha


def convert(image_urls):
    r_ = Rekognition()
    g_ = Gracenote()
    l_ = LiveFans()
    p_ = Petitlyrics()
    y_ = Yamaha()

    # analyze moode
    moods = r_.images_to_mood(image_urls)

    # choose artists
    artists = l_.get_live_artists(5)

    # gracenote api
    # todo: parallel process by mood
    mood = max(moods, key=moods.get)
    tracks = g_.get_artists_mood_tracks(artists, mood)

    # get and build lyric
    song = []
    count = 0
    for t in tracks:
        lyrics = p_.track_to_lyrics(t, offset=count, limit=2)
        if len(lyrics) > 0:
            for l in lyrics:
                song.append(l)
            count += 1

    # make mp3 song
    song = song[:4]
    mp3_url = y_.create_song(song)

    result = {
        "mp3_url": mp3_url,
        "moods": moods,
        "artists": artists,
        "tracks": tracks,
        "lyric": song
    }

    return result
