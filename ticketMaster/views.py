# Create your views here.


import requests
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse


def ticketmaster(request):
    context = {'name': 'Fuad'}
    # for test
    cityName = 'Hartford'
    searchTerm = 'Music'

    get_event_search(searchTerm, cityName)
    return render(request, 'event-search.html', context)


# def get_event_search():
#     try:
#         # Construct the URL with parameters
#         url = "https://app.ticketmaster.com/discovery/v2/events.json?apikey=9Zjc7b0W1ArKnBk1v0TfA8C8P5FSA8Ng"
#
#         # The query parameters will be appended to the url such as https://randomuser.me/api/?results=5&gender=female&nat=us
#
#         # Send a GET request to the specified URL with parameters
#         response = requests.get(url)
#
#         # Raise an exception for 4xx and 5xx status codes
#         response.raise_for_status()
#
#         # Parse the JSON data from the response
#         data = response.json()
#         print(data)
#
#         # Return the parsed data
#         return data
#     except requests.exceptions.RequestException as e:
#         # Handle request exceptions (e.g., network issues, timeouts)
#         print(f"Request failed: {e}")
#
#         # Return None to indicate failure
#         return None


def get_event_search(search_term, city_name, ):
    try:
        api_url = "https://app.ticketmaster.com/discovery/v2/events.json"
        api_key = "9Zjc7b0W1ArKnBk1v0TfA8C8P5FSA8Ng"

        params = {
            'apikey': api_key,
            'city': city_name,
            'keyword': search_term,
            'classificationName': search_term,
            'countrycode': 'US',
            'sort': 'date,asc'
        }

        response = requests.get(api_url, params=params)

        response.raise_for_status()

        if response.status_code == 200:
            json_response = response.json()
            # Parse the response or perform other operations here
            events = []
            # parsing all data --needs to find date and time
            for item in json_response['_embedded']['events']:
                event = {}
                event['eventName'] = item['name']
                event['eventLink'] = item['url']
                event['imgURL'] = item['images'][1]['url']
                # event['eventDate'] = item['dates']['start']['dateTime']
                # event['eventTime'] = item['dates']['start']['localTime']
                event['venueName'] = item['_embedded']['venues'][0]['name']
                event['address'] = item['_embedded']['venues'][0]['address']['line1']
                event['venueState'] = item['_embedded']['venues'][0]['state']['name']
                event['venueCity'] = item['_embedded']['venues'][0]['city']['name']
                event['venueCityState'] = event['venueCity'] + ' , ' + event['venueState']
                events.append(event)
            print(events)
            # You can return the JSON response or process it further
            # print(json_response)
            return JsonResponse(json_response)
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network issues, timeouts)
        print(f"Request failed: {e}")

        # Return None to indicate failure
        return None
