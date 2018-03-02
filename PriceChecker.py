import ebaysdk
import datetime
import sys

#import plotly.plotly as py
import plotly as py
import plotly.graph_objs as go
import pandas as pd


from ebaysdk.finding import Connection as finding

searchstring = sys.argv[1]

api = finding(siteid='EBAY-US', appid='ClaudeAm-PokemonT-PRD-85d705b3d-fceb8191', config_file=None)

#api.execute('findItemsAdvanced', {
api.execute('findCompletedItems', {
    'keywords': [searchstring + ' -psa -PL -flash -online -digital -playset -(4) -(2) -(3) -3x -x3 -2x -x2 -4x -x4 -lot -bundle -prerelease -sealed -china -fake -collection -set'],
    'categoryId' : '2611',
    'itemFilter': [
#        {'name': 'Condition', 'value': 'New'},
        {'name': 'Currency', 'value': 'USD'},
        {'name': 'ListedIn', 'value': 'EBAY-US'},
        {'name': 'LocatedIn', 'value': 'US'},
#        {'name': 'FreeShippingOnly', 'value': 'true'},
        {'name': 'SoldItemsOnly', 'value': 'true'}
#        {'name': 'ListingType', 'value': 'FixedPrice'}
#        {'name': 'MinPrice', 'value': '200', 'paramName': 'Currency', 'paramValue': 'GBP'},
#        {'name': 'MaxPrice', 'value': '400', 'paramName': 'Currency', 'paramValue': 'GBP'}
    ],
    'paginationInput': {
        'entriesPerPage': '200',
        'pageNumber': '1'
    },
    'sortOrder': 'EndTimeSoonest'
})

dictstr = api.response.dict()

#resultsdict = {}
resultslist = []


#DEBUG
#for item in dictstr['searchResult']['item']:
#    for k, v in item.iteritems():
#        print k, v

for item in dictstr['searchResult']['item']:
    # print "ItemID: %s" % item['itemId']
    # print "Title: %s" % item['title']
    if item['shippingInfo']['shippingType'] != 'Calculated' and item['shippingInfo']['shippingType'] != 'FreePickup':

        price = float(item['sellingStatus']['convertedCurrentPrice']['value'])
        shipping = float(item['shippingInfo']['shippingServiceCost']['value'])
        totalcost = price + shipping
        saledate = item['listingInfo']['endTime'][:item['listingInfo']['endTime'].find('T')]
        saledatetime = item['listingInfo']['endTime']

        dt_saledatetime = datetime.datetime.strptime(saledatetime, '%Y-%m-%dT%H:%M:%S.000Z')

        print str.format(saledate) + ' ' + str(totalcost)
        resultslist.append((dt_saledatetime, totalcost))
        #resultsdict.update({datetime.datetime.strptime(saledatetime, '%Y-%m-%dT%H:%M:%S.000Z'): totalcost})

        #print "Date: %s" % saledate
        #print "Price: %s" % price
        #print "Shipping Cost: %s" % shipping
        #print "Total Cost: %s" % totalcost


df = pd.DataFrame(resultslist, columns=['Date', 'Price'])

#df = pd.DataFrame.from_dict(resultsdict, orient="index")
#df.columns = ['Price']
#print df


layout = dict(title = searchstring + ' Price History',
              xaxis = dict(title = 'Date'),
              yaxis = dict(title = 'All-In Prince'),
              )


data = [go.Scatter(
          x=df.Date,
          y=df.Price,
          mode = 'lines+markers',
          name = searchstring + ' Price History')]


fig = dict(data=data, layout=layout)
py.offline.plot(fig)

# py.offline.plot(data)


    #print "CategoryID: %s" % item['primaryCategory']['categoryId']
    #print "ItemID: %s" % item['itemId'].value
    #print "Title: %s" % item['title'].value
    #print "CategoryID: %s" % item['primaryCategory']['categoryId'].value

#for item in dictstr['searchResult']['item']:
#    for k, v in item.iteritems():
#        print k, v
