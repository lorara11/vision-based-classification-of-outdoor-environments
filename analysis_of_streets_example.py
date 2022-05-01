"""We perform vision-based predictions on two different streets in Barcelona, and save the predictions and 
classifications in dataframes in order to compare both streets."""

import pandas as pd

from google_maps_client import GoogleMapsClient
from restbai_client import RestbAiClient


def analyze_address(address):
    """Given an address, makes vision-based predictions and classifications of the type of zone 
    that surrounds the address, the styles of the exterior of buildings, a score of the condition 
    between 1.0 and 6.0, a bool that represents the significant presence of natural light. It also
    includes an image caption.

    :param address: The address from which to analyze the image
    :type address: str
    :return: Predictions and classifications
    :rtype: dict
    """
    data_dict = {}

    # Get the url for the static Street View image
    url = maps_client.get_static_image_url(location=address)
    data_dict['street_view_image_url'] = url
    print(url)
    
    # Get a list of predicted types of zones, that builds up to more than 80% of confidence
    type_of_zone_predictions = restbai_client.type_of_zone(url)
    type_of_zones_80pct_confidence = []

    total_confidence = 0.0
    for zone, confidence in type_of_zone_predictions:
        if total_confidence >= 0.8:
            break
        type_of_zones_80pct_confidence.append(zone)
        total_confidence += confidence
    
    # Format the list as a pretty string, to add it to the resulting dataframe
    zones_pretty_string = ', '.join([zone.replace('_', ' ') for zone in type_of_zones_80pct_confidence])
    data_dict['types_of_zones_80pct_confidence'] = zones_pretty_string

    # Get a list of predicted exterior styles of the buildings, that builds up to more than 80% of confidence
    building_style_predictions = restbai_client.type_of_zone(url)
    building_styles_80pct_confidence = []

    total_confidence = 0.0
    for style, confidence in building_style_predictions:
        if total_confidence >= 0.8:
            break
        building_styles_80pct_confidence.append(style)
        total_confidence += confidence
    
    # Format the list as a pretty string, to add it to the resulting dataframe
    styles_pretty_string = ', '.join([zone.replace('_', ' ') for zone in building_styles_80pct_confidence])
    data_dict['building_styles_80pct_confidence'] = styles_pretty_string

    # Get the condition score
    condition_score = restbai_client.condition(url)
    data_dict['condition_score'] = condition_score

    # Get the bool that represents the presence of natural light
    # This seems to not be well optimized for exteriors, as the result is False too often
    natural_light = restbai_client.natural_light(url)
    data_dict['natural_light'] = natural_light

    # Get the auto-generated image caption (kind of more experimental data, for now)
    image_caption = restbai_client.image_caption(url)
    data_dict['image_caption'] = image_caption

    return data_dict


maps_client = GoogleMapsClient()
restbai_client = RestbAiClient()

# It is possible to automate the extraction of lists of addresses using APIs, or engineer the data ourselves 
# by reverse geocoding. For this prototype and testing, this automation is still not included.
addresses_av_tibidabo = [str(i)+' Av. del Tibidabo, Barcelona, Catalunya' for i in range(1,38)]

# List of dictionaries which will become a dataframe
data = []

for address in addresses_av_tibidabo:
    # Dictionary which will become a row in the dataframe
    data_dict = analyze_address(address)
    data.append(data_dict)

df = pd.DataFrame(data)
df.to_csv('Tibidabo_Avenue_Barcelona.csv', sep=';')
print(df)


addresses_st_aribau = [str(i)+" Carrer d'Aribau, Barcelona, Catalunya" for i in range(160,191)]
# List of dictionaries which will become a dataframe
data = []

for address in addresses_st_aribau:
    # Dictionary which will become a row in the dataframe
    data_dict = analyze_address(address)
    data.append(data_dict)

df = pd.DataFrame(data)
df.to_csv('Aribau_Street_Barcelona.csv', sep=';')
print(df)