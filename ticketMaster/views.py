# Create your views here.
import urllib
from _datetime import datetime
import requests
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.http import JsonResponse, Http404
from django.urls import reverse, NoReverseMatch
from django.utils import timezone

from .models import Event, Comment, SavedEvent
from .forms import *


def ticketmaster(request):
    # if the request method is a post
    if request.method == 'POST':
        # get the search term and location
        search_term = request.POST.get('search-term')
        city = request.POST.get('city')

        # Check if either search_term or city is empty
        if not search_term or not city:
            # Set up an error message using Django's message utility to inform the user

            # has city but no search_term
            if city:
                messages.info(request, 'Search term cannot be empty. Please enter a search term.')
            # has search_term but no city
            elif search_term:
                messages.info(request, 'City cannot be empty. Please enter a city.')
            # has neither
            else:
                messages.info(request, 'Both keyword and city are required fields.')

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

                # testing search results
                returned_result = len(events)
                print(returned_result)

                # Initialize an empty list to store user data
                event_list = []

                # check current user
                current_user = request.user

                # Iterate through each user in the 'events' list coming from the api
                # Rather than directly passing the "events" array to the template,
                # the following approach allows server-side processing and formatting of specific data (e.g., date).
                # So, the template only needs to plug in the preprocessed information.
                for item in events:
                    event_id = item['id']

                    event_name = item['name']
                    event_link = item['url']
                    event_img_url = item['images'][1]['url']
                    # make sure image stored is large to ensure quality
                    for image in item['images']:
                        if image['url'].lower().find("large") != -1:
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
                    # Concatenate the address, city, and state to form the query parameter for Google Maps
                    address_for_google_maps = f"{event_address}, {event_city_state}"

                    # Encode the address to be URL-safe
                    encoded_address = urllib.parse.quote(address_for_google_maps)

                    google_map = "https://www.google.com/maps/search/?api=1&query=" + encoded_address
                    print(google_map)

                    # Create a new dictionary to store event details
                    event_details = {
                        'event_id': event_id,
                        'eventName': event_name,
                        'eventLink': event_link,
                        'imageLink': event_img_url,
                        'venue': event_venue_name,
                        'localDate': formatted_date,
                        'localTime': formatted_time,
                        'address': event_address,
                        'cityState': event_city_state,
                        'googleMap': google_map

                    }

                    # check if event is in event table
                    #   if not, add it
                    if not Event.objects.filter(event_id=event_id).exists():
                        event_details['localDate'] = date_object
                        event_details['localTime'] = time_obj
                        # Create a new row using the create method
                        Event.objects.create(**event_details)

                    event_details['localDate'] = formatted_date
                    event_details['localTime'] = formatted_time

                    if current_user.is_authenticated:
                        saved = is_saved(event_id, current_user)
                        print('user authenticated')
                    else:
                        saved = None
                        print('not authenticated')

                    event_details['favoriteEvent'] = saved
                    print('favorite event? ')
                    print(saved)
                    event_list.append(event_details)

                print('printing event_list')
                print(event_list)
                # Create a context dictionary with the event_list and render the 'index.html' template
                context = {'events': event_list,
                           'returned_result': returned_result}
                return render(request, 'ticketmaster.html', context)


            else:
                messages.info(request, 'NO RESULT FOUND.')
                # redirect user to the index page
                return redirect('ticketmaster')

    # all other cases, just render the page without sending/passing any context to the template
    print('return without post or get')
    return render(request, 'ticketmaster.html')


def view_event(request, event_id):
    # Get the event based on its id
    current_user = request.user
    try:
        event = Event.objects.get(event_id=event_id)
        print("Event found:", event)
    except Event.DoesNotExist:
        print("Event does not exist.")
        return render(request, 'ticketmaster.html')

    # get array of comments
    comment_list = get_comment_array(event_id)

    # get user's comment
    if current_user.is_authenticated:
        already_commented = get_comment(event_id, current_user)
        saved = is_saved(event_id, current_user)
    else:
        already_commented = None
        saved = None

    context = {
        'event_id': event_id,
        'eventName': event.eventName,
        'eventLink': event.eventLink,
        'imageLink': event.imageLink,
        'venue': event.venue,
        'localDate': event.localDate.strftime("%a %b %d %Y"),
        'localTime': event.localTime.strftime("%I:%M %p"),
        'address': event.address,
        'cityState': event.cityState,
        'comments': comment_list,
        'commentExists': already_commented,
        'commentInfo': {
            'userRating': 0,
            'userComment': '',
            'favoriteEvent': saved
        }
    }

    if already_commented:
        context['commentInfo']['userRating'] = already_commented.starRating
        context['commentInfo']['userComment'] = already_commented.comment

    return render(request, 'eventview.html', context)


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


def delete_comment(request, event_id):
    comment = Comment.objects.get(eventID__event_id=event_id, user=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment.delete()
            return redirect(reverse('view_event', kwargs={'event_id': event_id}))

    return redirect('ticketmaster')


def update_comment(request, event_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            user = request.user
            star_rating = form.cleaned_data['starRating']
            comment_text = form.cleaned_data['comment']
            success = update_comment_content(event_id, user, star_rating, comment_text)

            if success:
                return redirect(reverse('view_event', kwargs={'event_id': event_id}))

    return redirect('ticketmaster')


def create_comment(request, event_id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            e_id = Event.objects.get(event_id=event_id).id
            user = request.user.id
            star_rating = form.cleaned_data['starRating']
            comment_text = form.cleaned_data['comment']
            comment = Comment(eventID_id=e_id, user_id=user, starRating=star_rating, comment=comment_text)
            comment.full_clean()
            comment.save()
            return redirect(reverse('view_event', kwargs={'event_id': event_id}))

    return redirect('ticketmaster')


def get_comment(event_id, user):
    try:
        comment = Comment.objects.get(eventID__event_id=event_id, user=user)
        return comment
    except Comment.DoesNotExist:
        # when event has no comment from user
        return None


def get_comment_array(event_id):
    try:
        comments = Comment.objects.filter(eventID__event_id=event_id)
        return comments
    except Comment.DoesNotExist:
        # when event has no comments
        return None


def is_saved(event_id, user):
    try:
        return SavedEvent.objects.get(eventID__event_id=event_id, user=user)
    except SavedEvent.DoesNotExist:
        # when event has no comments
        return None


def update_comment_content(event_id, user, rating, comment):
    try:
        # Get the comment based on the event id
        user_comment = get_comment(event_id, user)
        user_comment.comment = comment
        user_comment.starRating = rating
        # Save the changes to the database
        user_comment.save()
        return comment

    except Comment.DoesNotExist:
        return None


def toggle_save(request, event_id, source):
    e_id = Event.objects.get(event_id=event_id).id
    user = request.user.id
    saved = is_saved(event_id, user)

    if saved:
        saved.delete()
    else:
        new_save = SavedEvent(eventID_id=e_id, user_id=user)
        new_save.full_clean()
        new_save.save()

    if source == 'view_event':
        return redirect(reverse('view_event', kwargs={'event_id': event_id}))
    elif source == 'ticketmaster':
        return JsonResponse({'status': 'success'})
    else:
        raise Http404("Invalid source parameter")
