def data():
    import requests
    import time
    import datetime

    KNOTS = 0.868976 # number of knots in 1 mph

    #wunderground key: 5f4f6000c4fcf3e7 ---- 500 api calls per day limit: update every 30 mins
    wunderground = requests.get('http://api.wunderground.com/api/5f4f6000c4fcf3e7/conditions/q/CA/San_Diego.json')
    magic_seaweed = requests.get('http://magicseaweed.com/api/94276ac2ca30f6a1e28acaf7c15ea0dc/forecast/?spot_id=663&units=us')

    wu = wunderground.json()
    ms_list = magic_seaweed.json()

    wu

    # get forecast for closest future prediction
    for ii in range(len(ms_list)):
        if ms_list[ii]['timestamp'] - time.time() > 0:
            ms = ms_list[ii]
            break

    primary = ms['swell']['components']['primary']
    secondary = ms['swell']['components']['secondary']
    combined = ms['swell']['components']['combined']
    wind = ms['wind']

    #print "Primary   dir:", primary['direction'],   "h:", primary['height'],    "p:",primary['period']
    #print "Secondary dir:", secondary['direction'], "h:", secondary['height'],  "p:",secondary['period']
    print "Combined dir:", combined['direction'], "h:", combined['height'],  "p:",combined['period']
    print "Wind      dir:", wu['current_observation']['wind_degrees'],  "kts:", float(wu['current_observation']['wind_mph'])*KNOTS,"gust:", float(wu['current_observation']['wind_gust_mph'])*KNOTS

    data = {}
    data['swell'] = {'dir': combined['direction'],
                     'h':combined['height'],
                     'p':combined['period']}
    data['wind'] = {'dir':wu['current_observation']['wind_degrees'],
                    'kts':float(wu['current_observation']['wind_mph'])*KNOTS,
                    'gust':float(wu['current_observation']['wind_gust_mph'])*KNOTS}
    return data

print data()
