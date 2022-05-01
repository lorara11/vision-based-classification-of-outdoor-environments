from google_maps_client import GoogleMapsClient
from restbai_client import RestbAiClient


maps_client = GoogleMapsClient()
restbai_client = RestbAiClient()

url = maps_client.get_static_image_url(location="Chagrin Falls, OH")

print(url)
print('Type of zone:',restbai_client.type_of_zone(url))
print('Building exterior style:',restbai_client.building_exterior_style(url))
print('Natural light:',restbai_client.natural_light(url))  # Not well optimized for exteriors, result is usually False
print('Condition score:',restbai_client.condition(url))
print('Image caption:',restbai_client.image_caption(url))
