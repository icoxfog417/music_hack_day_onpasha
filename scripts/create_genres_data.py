def main(path):
    from api import echonest
    e = echonest.Echonest()
    e.download_genres(path)

if __name__ == "__main__":
    import os
    path = os.path.join(os.path.dirname(__file__), "../data/genres.txt")
    main(path)
