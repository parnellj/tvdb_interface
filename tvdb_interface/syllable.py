from pytvdbapi import api
from pytvdbapi import error
from collections import defaultdict
import csv
import time
import sys
import os

wd = os.path.dirname(__file__)

series = {}
csvOutput = []

with open(os.path.join('.', 'shows.csv'), 'rb') as csvfile:
    listreader = csv.reader(csvfile, delimiter=',')
    count = 0
    for row in listreader:
        series[row[0]] = defaultdict(dict)

with open(os.path.join('config', 'api_key.txt'), 'r') as f:
            t = []
            for line in f.readlines():
                t.append(tuple(line[:-1].split(' = ')))
            token = dict(t)
		
db = api.TVDB(token['api_key'])

for a in sorted(series.keys()): print a

for seriesName in sorted(series.keys()):
    print "Downloading " + seriesName
    # I'm sure TVDB can handle it, but just to be courteous...
    #time.sleep(1)

    # Go to next show if there's an error.
    try:
        result = db.search(seriesName, 'en')
    except (error.ConnectionError, error.TVDBNotFoundError, error.TVDBIndexError):
        series[seriesName]['name'] = seriesName + ' Lookup Error!'

    selection = 0

    if len(result) > 1:
        for n, a in enumerate(result): print str(n)+": "+a.SeriesName
        selection = input('select the right one')

    result = result[selection]

    # Append series information to dict
    series[seriesName]['name'] = result.SeriesName
    series[seriesName]['seasons'] = len(result)

    # Special case because some TVDB dates are unicode, others datetime objs
    a = result.FirstAired
    if not isinstance(a, unicode): a.strftime("%m/%d/%Y")
    series[seriesName]['premiere'] = a

    series[seriesName]['runtime'] = result.Runtime
    series[seriesName]['Network'] = result.Network
    series[seriesName]['airday'] = result.Airs_DayOfWeek
    series[seriesName]['airtime'] = result.Airs_Time
    series[seriesName]['genre'] = '|'.join(result.Genre)
    series[seriesName]['status'] = result.Status

    eps = []

    # Compile episode data by season, with melted columns
    for season in result:
        for episode in season:

            air = episode.FirstAired
            print type(air)
            if not isinstance(air, unicode): air = air.strftime("%m/%d/%Y")

            abs = episode.absolute_number
            if isinstance(abs, unicode): abs = ' '

            name = episode.EpisodeName
            if isinstance(name, int): name = str(name)

            epdata = [str(episode.SeasonNumber),
                      str(episode.EpisodeNumber),
                      str(abs),
                      air,
                      name.encode('ascii','ignore')]
            eps.append(epdata)

    # Finally, append episode information to main dict
    series[seriesName]['episodes'] = eps

headings = []
# Prepare CSV line output
for key in sorted(series.keys()):
    show = series[key]
    showOut = []
    outBase = []

    # I wish I knew a more elegant way to scrape headings...
    if len(headings) == 0:
        headings = sorted([a for a in show.keys() if a is not 'episodes'])
        headings += ['season #', 'episode #', 'absolute #',
                     'airdate', 'title']

    # Build all but episode info
    for k in sorted(show.keys()):
        if k is not 'episodes': outBase.append(str(show[k]))

    print [type(a) for a in outBase]

    # Append one line per episode
    for e in show['episodes']:
        o = outBase + [epInfo for epInfo in e[0:5]]
        print [a for a in e[0:5]]
        print [type(a) for a in e[0:5]]
        outString = ','.join(o)
        showOut.append(outString)

    for a in showOut: csvOutput.append(a)

file = open(os.path.join('.', 'list.csv'), 'w')
file.write((','.join(headings)) + '\n')
for a in csvOutput: file.write(a + '\n')
file.close()
