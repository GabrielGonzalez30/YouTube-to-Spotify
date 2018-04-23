class Video(object):

    """
    This class models a YouTube video with all the necessary
    information to search through a playlist.
    """
    
    __search_query__ = None
    artist = None

    def __init__(self, video_title):
        self.video_title = video_title
        self.set_search_query(self.video_title)
        self.__parse_artist__()

    def get_search_query(self):
        return self.__search_query__

    def set_search_query(self, sq):
        self.__search_query__ = Video.simplifyTitle(sq)

    @staticmethod
    def simplifyTitle(title):

        #Credit to github user srajangarg for most of this

        if title is "":
            return title

        title = title.replace('"', "")

        import re
        title = re.sub("[\(\[].*?[\)\]]", "", title)

        tobe = ["Official", "OFFICIAL", "Music", "MUSIC", "Video", "VIDEO", "Original", "ORIGINAL", "Audio", "AUDIO", "Lyric", "LYRIC", "Lyrics", "LYRICS", "Out", "OUT", "Now", "NOW"]
        
        for string in tobe:
            title.replace(string, "")

        featuring = ["feat", "ft", "Ft", "Feat", "Featuring", "with", ',', "&"]

        for feat in featuring:
            index = title.find(feat)
            if index is not -1:
                findDash = title.find("-")
                if findDash is not -1 and index < findDash:
                    str1 = title[index:findDash-1]
                    title = title.replace(str1, "")
                else:
                    title = title[:index]
                break

        return title

    def __parse_artist__(self):
        title = self.get_search_query()
        self.artist = title[:title.find("-") - 1]
        
