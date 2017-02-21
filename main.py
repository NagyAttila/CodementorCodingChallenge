#Build a simple Yelp-like system: Given a set of restaurant and metadata (coordinates, ratings, opening hours), design and implement the following functionalities without using a database.

#1. Find restaurants within specified radius, given a coordinate
#2. Improve the above function by only returning restaurants that are open given desired dining hour
#3. Improve the above function by sorting the results by average ratings

import numpy as np

class Yelp(object):
    def __init__(self, restaurants, ratings):
        self.restaurants = restaurants
        self.ratings = ratings

    def find(self, coordinates, radius, dining_hour=None, sort_by_rating=False):
        # Returns list of Restaurant within radius.
        #
        #  coordinates: (latitude, longitude)
        #  radius: kilometer in integer
        #  dining_hour: If None, find any restaurant in radius.
        #               Otherwise return list of open restaurants at specified hour.
        #  sort_by_rating: If True, sort result in descending order,
        #                  highest rated first.

        # 1: Find restaurant in radius
        found_restaurants = []
        for restaurant in self.restaurants:

            lat_diff = coordinates[0] - restaurant.latitude
            lon_diff = coordinates[1] - restaurant.longitude
            distance = np.sqrt(lat_diff**2 + lon_diff**2)

            if distance < radius:
                found_restaurants.append(restaurant)

        # 2: Check for openning hours
        if dining_hour != None:
            found_restaurants = filter(lambda r: r.open_hour <= dining_hour and r.close_hour >= dining_hour, self.restaurants)

        # 3: Sort restaurants by ratings
        if sort_by_rating == True:

            restaurant_rating_pairs = []
            for restaurant in self.restaurants:
                for rating in self.ratings:
                    if restaurant.id == rating.restaurant_id and \
                            rating.rating <= 5 and rating.rating >=1:
                        restaurant_rating_pairs.append((restaurant, rating))

            rnr_pairs_sorted = sorted(list(restaurant_rating_pairs), key=lambda rnr: rnr[1].rating)
            found_restaurants = [rnr[0] for rnr in rnr_pairs_sorted]

        return found_restaurants

class Restaurant(object):
    # where open_hour and close_hour is in [0-23]
    def __init__(self, id, name, latitude, longitude, open_hour, close_hour):
        self.id = id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.open_hour = open_hour
        self.close_hour = close_hour

class Rating(object):
    # rating is in [1-5]
    def __init__(self, restaurant_id, rating):
        self.restaurant_id = restaurant_id
        self.rating = rating

def main():

    # 1: Test radius
    restaurants = [Restaurant(0, "test_in_radius", 37.7577, -122.4376, 0, 0)]
    restaurants.append(Restaurant(1, "test_not_in_radius", 40.7577, -122.4376, 0, 0))

    y = Yelp(restaurants, None)
    found_restaurants  = y.find((37.7, -122.6), 1, None, False)
    names = list(map(lambda r: r.name, found_restaurants))
    assert names == ['test_in_radius'], "test_in_radius"


    # 2: Test openning hours
    restaurants = [Restaurant(2, "test_open", 37.7577, -122.4376, 7, 23)]
    restaurants.append(Restaurant(3, "test_not_open", 37.7577, -122.4376, 22, 23))

    y = Yelp(restaurants, None)
    found_restaurants  = y.find((37.7, -122.6), 1, 10, False)
    names = list(map(lambda r: r.name, found_restaurants))
    assert names == ['test_open'], "test_open"

    # 3: Test ratings
    restaurants = [Restaurant(4, "test_ratings_1", 37.7577, -122.4376, 7, 23)]
    restaurants.append(Restaurant(5, "test_ratings_2", 37.7577, -122.4376, 7, 23))
    restaurants.append(Restaurant(6, "test_ratings_3", 37.7577, -122.4376, 7, 23))
    restaurants.append(Restaurant(8, "test_too_high_rating", 37.7577, -122.4376, 7, 23))
    restaurants.append(Restaurant(7, "test_missing_rating", 37.7577, -125.4376, 7, 23))
    ratings = [Rating(4, 3)]
    ratings.append(Rating(5, 1))
    ratings.append(Rating(6, 4))
    ratings.append(Rating(8, 6))

    y = Yelp(restaurants, ratings)
    found_restaurants  = y.find((37.7, -122.6), 1, None, True)
    names = list(map(lambda r: r.name, found_restaurants))
    assert names == ['test_ratings_2', 'test_ratings_1', 'test_ratings_3'], "test_ratings"

    # 4: Test all together
    restaurants = [Restaurant(4, "test_ratings_1", 37.7577, -122.4376, 7, 23)]
    restaurants.append(Restaurant(5, "test_ratings_2", 37.7577, -122.4376, 7, 23))
    restaurants.append(Restaurant(6, "test_ratings_3", 37.7577, -122.4376, 7, 23))
    restaurants.append(Restaurant(7, "test_missing_rating", 37.7577, -125.4376, 7, 23))
    restaurants.append(Restaurant(3, "test_not_open", 37.7577, -122.4376, 22, 23))
    ratings = [Rating(4, 3)]
    ratings.append(Rating(5, 1))
    ratings.append(Rating(6, 4))

    y = Yelp(restaurants, ratings)
    found_restaurants  = y.find((37.7, -122.6), 1, 10, True)
    names = list(map(lambda r: r.name, found_restaurants))
    assert names == ['test_ratings_2', 'test_ratings_1', 'test_ratings_3'], "test_all"

main()
