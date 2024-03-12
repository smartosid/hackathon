

import nltk

from flask import Flask, request, render_template
try:
    from googlesearch import search
except ImportError:
    print("No module named 'googlesearch' found")
app = Flask(__name__)

# Predefined lists of locations, occasions, male pronouns, female pronouns, places, objects, and delivery terms
locations = [
    "New York", "Paris", "London", "Tokyo", "Sydney",
    "Los Angeles", "Rome", "Berlin", "Beijing", "Dubai",
    "Toronto", "Mumbai", "Rio de Janeiro", "Cape Town", "Singapore",
    "Bangkok", "Barcelona", "Moscow", "Amsterdam", "Delhi", "Mumbai", "kolkata","Chennai", "Bangalore",
    "Hyderabad", "Ahmedabad", "Pune", "Jaipur", "Lucknow"]

occasions = ["wedding", "party", "birthday", "anniversary", "graduation", "holiday", "baby shower", "engagement", "retirement",
             "Diwali", "Holi", "Navratri", "Raksha Bandhan", "Durga Puja", "Pongal", "Eid", "Ganesh Chaturthi", "Onam", "Karva Chauth",
             "housewarming", "promotion", "farewell", "reunion", "Valentine's Day", "Christmas", "New Year's Eve", "Halloween"]

male_pronouns = ["he", "him", "his", "himself", "his own", "he's", "his", "gentleman", "sir", "man", "boy", "dude"]

female_pronouns = ["she", "her", "hers", "herself", "her own", "she's", "lady", "madam", "miss", "woman", "girl"]

places = ["beach", "mall", "school", "park", "restaurant", "cinema", "library", "hospital", "gym", "zoo"]

objects = ["mobile", "earphones", "laptop", "watch", "sunglasses", "camera", "book", "umbrella", "backpack", "shoes",
           "coffee mug", "umbrella", "notebook", "sweater", "umbrella", "sunscreen", "satchel", "scooter", "headset", "gaming console",
           "guitar", "bicycle", "headphones", "wallet", "perfume", "water bottle", "sneakers", "jewelry", "tablet", "speaker"]

delivery = ["today", "tomorrow", "this week", "this month","amazon","flipkart","instagram","snapchat","shaadi"]

def find_places_occasions_and_gender(sentence):
    # Tokenize the input sentence
    words = nltk.word_tokenize(sentence)

    # Convert both the input words and the lists of locations, occasions, male pronouns, female pronouns, places, objects, and delivery terms to lowercase
    lower_words = [word.lower() for word in words]
    lower_locations = [loc.lower() for loc in locations]
    lower_occasions = [occ.lower() for occ in occasions]
    lower_male_pronouns = [pronoun.lower() for pronoun in male_pronouns]
    lower_female_pronouns = [pronoun.lower() for pronoun in female_pronouns]
    lower_places = [place.lower() for place in places]
    lower_objects = [obj.lower() for obj in objects]
    lower_delivery = [term.lower() for term in delivery]

    # Check each word if it's a location, occasion, male pronoun, female pronoun, place, object, or delivery term (case-insensitive)
    found_locations = [word for word in lower_words if word in lower_locations]
    found_occasions = [word for word in lower_words if word in lower_occasions]
    found_male_pronouns = [word for word in lower_words if word in lower_male_pronouns]
    found_female_pronouns = [word for word in lower_words if word in lower_female_pronouns]
    found_places = [word for word in lower_words if word in lower_places]
    found_objects = [word for word in lower_words if word in lower_objects]
    found_delivery = [word for word in lower_words if word in lower_delivery]

    return found_locations, found_occasions, found_male_pronouns, found_female_pronouns, found_places, found_objects, found_delivery


@app.route('/')
def index():
    return render_template('chatbot.html')
@app.route('/results', methods=['POST'])
def results():
    sentence = request.form['sentence']
    found_locations, found_occasions, found_male_pronouns, found_female_pronouns, found_places, found_objects, found_delivery = find_places_occasions_and_gender(sentence)

    # Concatenate all the found elements into a single string
    result_string = ' '.join(found_locations + found_occasions + found_male_pronouns + found_female_pronouns + found_places + found_objects + found_delivery)

    # Print the result string
    print("Results:", result_string)

    query = "ecommerce+" + result_string + "+shopping"
    links = []
    try:
        output = search(query, num=10, stop=10)
        for result in output:
            links.append(result)
            print(result)
    except Exception as e:
        print("ERROR FACED:", e)

    return render_template('result.html', links=links)


if __name__ == '__main__':
    app.run(debug=True)