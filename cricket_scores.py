from libqtile.widget import base
import feedparser

class CricketScores(base.ThreadPoolText):

    defaults = [
        ("update_interval", 60, "Update interval for the cricket scores widget"),
        ("format","{scores}","Display format for cricket scores"),
        ("teams",[],"Teams to display scores for"),
        ("separator"," \U0001F3CF ","Text to place between scores"),
        ("no_scores_string","No scores atm","Text to show when there are no scores to show"),
    ]

    def __init__(self, **config):
        super().__init__("", **config)
        self.add_defaults(CricketScores.defaults)

    def poll(self):
        # parse rss feed and get 
        # live matches from title field
        feed = feedparser.parse("http://static.cricinfo.com/rss/livescores.xml")
        scores = []
        for match in feed.entries:
            # filter live matches
            if "*" in match.title:
                scores.append(match.title)

        # remove scores not involving chosen teams
        filtered_scores = []
        for score in scores:
            for team in self.teams:
                if team in score:
                    filtered_scores.append(score)

        # if no scores, show no_scores_string
        if len(filtered_scores) == 0:
            final_scores = self.no_scores_string
        else:
            # form pretty string with separators
            final_scores = ""
            for score in filtered_scores:
                if score != filtered_scores[-1]:
                    final_scores += score + self.separator
                else:
                    final_scores += score

        variables = {
            "scores": final_scores,
        }

        return self.format.format(**variables)
