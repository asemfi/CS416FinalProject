# Create your views here.
from _datetime import datetime
import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.http import JsonResponse


def ticketmaster(request):
    print('in ticketmaster')
    # if the request method is a post
    if request.method == 'POST':
        print('inside post')
        # get the search term and location
        search_term = request.POST.get('search-term')
        city = request.POST.get('city')

        # Check if either search_term or city is empty
        if not search_term or not city:
            # Set up an error message using Django's message utility to inform the user

            # has city but no search_term
            if city: messages.info(request, 'Search term cannot be empty. Please enter a search term.')
            # has search_term but no city
            elif search_term: messages.info(request, 'City cannot be empty. Please enter a city.')
            # has neither
            else: messages.info(request, 'Both keyword and city are required fields.')

            # redirect user to the index page
            return redirect('ticketmaster')
            # Add code to handle or display the error_message as needed.

        # call get_event_search function() to get the data from the API
        event_search_result = get_event_search(search_term, city)
        # print(event_search_result)

        # If the request to fetch data from ticketmaster was unsuccessful or returned None
        if event_search_result is None:
            # Set up an error message using Django's message utility to inform the user
            messages.info(request, 'The server encountered an issue while fetching data. Please try again later.')
            # redirect user to the index page
            return redirect('ticketmaster')

        else:
            print("Else Block")
            # print the response for testing purpose (open "Run" at the bottom to see what is printed)
            if '_embedded' in event_search_result and event_search_result['_embedded']:
                events = event_search_result['_embedded']['events']

                # Initialize an empty list to store user data
                event_list = []

                # Iterate through each user in the 'events' list coming from the api
                # Rather than directly passing the "events" array to the template,
                # the following approach allows server-side processing and formatting of specific data (e.g., date).
                # So, the template only needs to plug in the preprocessed information.
                for item in events:
                    event = {}
                    event_id = item['id']
                    event_name = item['name']
                    event_link = item['url']
                    event_img_url = item['images'][1]['url']
                    # make sure image stored is large to ensure quality
                    for image in item['images']:
                        if image['url'].lower().find("large") != -1 :
                            event_img_url = image['url']

                    # Adding error handling for potential missing keys
                    if 'dates' in item and 'start' in item['dates'] and 'dateTime' in item['dates']['start']:
                        event_date = item['dates']['start']['dateTime']
                        # Convert the string to a datetime object
                        date_object = datetime.strptime(event_date, "%Y-%m-%dT%H:%M:%SZ")

                        # Format the datetime object into the desired readable format
                        formatted_date = date_object.strftime("%a %b %d %Y")

                        event_time = item['dates']['start']['localTime']

                        # Check for the presence of time data and format it
                        if event_time:
                            try:
                                time_obj = datetime.strptime(event_time,
                                                             "%H:%M:%S")  # Assuming time is in HH:MM:SS format
                                formatted_time = time_obj.strftime("%I:%M %p")  # Format time as desired
                                event_time = formatted_time
                            except ValueError:
                                # Handle cases where the time format is unexpected
                                event_time = 'N/A'


                    else:
                        # Handle missing or unexpected data, set a default value or skip this item
                        event_date = 'N/A'  # Set a default value
                        event_time = 'N/A'  # set a default value

                    event_venue_name = item['_embedded']['venues'][0]['name']
                    event_address = item['_embedded']['venues'][0]['address']['line1']
                    event_state = item['_embedded']['venues'][0]['state']['name']
                    event_city = item['_embedded']['venues'][0]['city']['name']
                    event_city_state = event_city + ' , ' + event_state
                    # Create a new dictionary to store event details
                    event_details = {
                        'event_id': event_id,
                        'event_name': event_name,
                        'event_link': event_link,
                        'event_img_url': event_img_url,
                        'event_venue_name': event_venue_name,
                        'event_time': formatted_time,
                        'event_date': formatted_date,
                        'event_address': event_address,
                        'event_city_state': event_city_state

                    }
                    event_list.append(event_details)

                print('printing event_list')
                print(event_list)
                # Create a context dictionary with the event_list and render the 'index.html' template
                context = {'events': event_list}
                return render(request, 'ticketmaster.html', context)


            else:
                messages.info(request, 'NO RESULT FOUND.')
                # redirect user to the index page
                return redirect('ticketmaster')








    # all other cases, just render the page without sending/passing any context to the template
    print('return without post or get')
    return render(request, 'ticketmaster.html')


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

            return json_response
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network issues, timeouts)
        print(f"Request failed: {e}")

        # Return None to indicate failure
        return None
