import os
import requests
import json
import sys


def load_names():
    """ use the same formating as in the txt file.
    loading names into a list and returning it"""
    
    with open("names.txt", "r") as f:
        names = f.read().split('\n')

    return names


def parse(streamers, link):
    """checks if the streamer is online
    returns a dict of online streamers"""
    
    streamer_on = {}
    details = {}
    sys.stdout.write("\nparsing streamers\n")
    
    for i in xrange(len(streamers)-1):
        html = requests.get(link %(streamers[i]))
        dump = json.loads(html.text)

        if dump["stream"] != None :
            streamer_on[streamers[i]] = i+1
            details[streamers[i]] = {"viewers": dump["stream"]["viewers"],
                                      "status": dump["stream"]["channel"]["status"].encode("utf-8")}
    return streamer_on, details


def start_livestreamer(streamer, key):
    """starts the stream, default quality is source
        change to your liking"""
    
    if streamer.keys() != None:
        stream_now = "livestreamer https://www.twitch.tv/%s source" %(key)
        os.system(stream_now)


def choose_streamer(streamer, details):
    """choose th streamer by number"""
    
    if not streamer:
        sys.stdout.write("no one online")
    else:
        for k,v in details.iteritems():
            print "[%s] %s %s" %(streamer[k], k, v)

        choice = input("choose the streamer by the number: ")
        key = filter(lambda k: streamer[k] == choice, streamer.keys())

    start_livestreamer(streamer, key[0])


link = "https://api.twitch.tv/kraken/streams/%s"
name_list = load_names()
streamer, details = parse(name_list, link)
choose_streamer(streamer, details)
