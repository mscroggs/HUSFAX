import os as _os

ceefax_path = _os.path.dirname(_os.path.realpath(__file__))

pages_dir = _os.path.join(ceefax_path, "pages")
with open(_os.path.join(ceefax_path, "VERSION")) as f:
    VERSION = f.read()

NAME = "HUSFAX"

flight_api = "http://example.com/{}{}{}"

title = (
    "--------------yyyyyyyyyy---------yyyyyyyyyy--------yyyyyyyyyy---------\n"
    "--------------yyyyyyyyyy---------yyyyyyyyyy--------yyyyyyyyyy---------\n"
    "--------------yy..yy..yy-----------y.....yy----------y.....yy---------\n"
    "--------------yy..yy..yy-yyyyyyyyy-y..yyyyy-yyyyyyyy-y..yy.yy-yyyyyyyy\n"
    "--------------yy......yy-yyyyyyyyy-y.....yy-yyyyyyyy-y.....yy-yyyyyyyy\n"
    "--------------yy..yy..yy-y..yy..yy-yyyyy.yy-y.....yy-y..yy.yy-y..y..yy\n"
    "--------------yy..yy..yy-y..yy..yy-y.....yy-y..yyyyy-y..yy.yy-y..y..yy\n"
    "--------------yyyyyyyyyy-y..yy..yy-yyyyyyyy-y....yyy-yyyyyyyy-yy...yyy\n"
    "--------------yyyyyyyyyy-y..yy..yy-yyyyyyyy-y..yyyyy-yyyyyyyy-y..y..yy\n"
    "-------------------------y......yy----------y..yyyyy----------y..y..yy\n"
    "-----------------------yyyyyyyyyyy--------yyyyyyyyyy--------yyyyyyyyyy\n"
    "-----------------------yyyyyyyyyyy--------yyyyyyyyyy--------yyyyyyyyyy"
    "").replace(".", "b")


twitter_access_key = None
twitter_access_secret = None
twitter_consumer_key = None
twitter_consumer_secret = None

metoffer_api_key = None
open_weather_api_key = None

twitch_client_id = None

location = [51.5252257441084, -0.134831964969635]

aoc_session = None
football_data_token = None


try:
    from localconfig import *  # noqa: F403, F401
except ImportError:
    pass
