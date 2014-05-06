soc_comp_final
==============

final project for social computing

## On Ubuntu


We are using pip + venv so, make sure you run

    sudo apt-get install python-virtualenv python-pip git build-essential python-setuptools python-dev

and for the numpy & scipy dependencies

    sudo apt-get install libblas-dev liblapack-dev gfortran

and then to install the dependencies

    virtualenv --no-site-packages venv
    source venv/bin/activate
    pip install -r requirements.txt

## Included Files

    capital_word.py

Pulls out capitalized words and compares them against a list of cities.

----

    cooccurrence.py

Creates visualizations of bigrams that occur across tweets. This is often suited for small numbers of tweets. Useful for sampling data to get familiar with it.

----

    Json to csv - ALL.py

Writes a csv file from Twitter JSON.

    Json to csv - NoRetweets.py

Removes newlines from tweets, and filters out Retweets.

----

    requirements.txt

Used by pip to install necessary dependencies (documented above for ubuntu)

----

    spit_data.py

Used for testing tweets against distributed architecture (see [Firesuit](http://github.com/peterklipfel/firesuit)). Reads tweets from csv and sends a request to the given domain.

----

    terms_increasing_in_frequency.py

Finds words that have frequency spikes.

----

    tweet_word_classifier.py

Finds important words by using tagged bigrams.

----

    word_count.py

Finds overall word frequencies in tweet set

----

    worldCities.py

Parses text file of world cities into a csv that is used in other files.
