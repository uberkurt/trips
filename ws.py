from bottle import *
from UberQuery import Query

@get('/trips')
def trips():
    return '''
        <form action="/trips" method="post">
          <p>
            Top-left lat: <input name="tllat" type="text" />
            Top-left lon: <input name="tllon" type="text" />
          </p>
          <p>
            Bottom-right lat: <input name="brlat" type="text" />
            Bottom-right lon: <input name="brlon" type="text" />
          </p>
          <p>
            <input name="start" value="started here" type="submit" />&nbsp;<input name="end" value="ended here" type="submit" />
          </p>
        </form>
    '''

@post('/trips')
def find_trips():
    tllat = request.forms.get('tllat')
    tllon = request.forms.get('tllon')
    brlat = request.forms.get('brlat')
    brlon = request.forms.get('brlon')

    if request.forms.get('end'):
        reqtype = 'end'
    elif request.forms.get('start'):
        return '<p>Sorry, not implemented yet! (Try "ended" functionality)</p>'
    else:
        return '<p>Hmm, not sure what functionality you are after</p>'

    esQuery = Query(tllat, tllon, brlat, brlon, reqtype)
    ret = esQuery.query_stats()
    facets = ret['facets']['farestat']
#    print facets

    return template('<p>You sent the following lat/lon bounding box:</p><p>Top Left lat:{{tllat}} / Top Left lon:{{tllon}}</p><p>Bottom Right lat:{{brlat}} / Bottom Right lon:{{brlon}}</p><p>Here is some analyses of the fares of all trips which {{reqtype}} there:<p><p>Count:{{count}}<br />Min:{{mini}}<br />Max:{{maxi}}<br />Average:{{avg}}</p>',
                    tllat=tllat, tllon=tllon, brlat=brlat, brlon=brlon, reqtype=reqtype,
                    count=facets['count'], mini=facets['min'], maxi=facets['max'], avg=facets['mean'])

run(host='0.0.0.0', port=80)
