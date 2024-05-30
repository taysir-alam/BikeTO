import requests as req
import pandas as pd
import folium 

#commented out sample from city of toronto api
# Toronto Open Data is stored in a CKAN instance. It's APIs are documented here:
# https://docs.ckan.org/en/latest/api/

# To hit our API, you'll be making requests to:
base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"

# Datasets are called "packages". Each package can contain many "resources"
# To retrieve the metadata for this package and its resources, use the package name in this page's URL:
"""
url = base_url + "/api/3/action/package_show"
params = { "id": "bike-share-toronto"}
package = req.get(url, params = params).json()

# To get resource data:
for idx, resource in enumerate(package["result"]["resources"]):

       # To get metadata for non datastore_active resources:
       if not resource["datastore_active"]:
           url = base_url + "/api/3/action/resource_show?id=" + resource["id"]
           resource_metadata = req.get(url).json()
           print(resource_metadata)
           # From here, you can use the "url" attribute to download this file
"""

pack = "bike-share-to"

def get_package_metadata(pack):
      url = f"{base_url}/api/3/action/package_show"
      params = {"id":pack}
      response = req.get(url, params=params)
      return response.json()

def get_resource_data(resource_url):
      response = req.get(resource_url)
      return response.content

package = get_package_metadata(pack)

station_data = None
trip_data = None

for resource in pack["result"]["resource"]:
      if "station" in resource["name"].lower() or "station" in resource["description"].lower():
            station_data = resource["url"]

      if "trip" in resource["name"].lower() or "trip" in resource["description"].lower():
            trip_data = resource["url"]      

if not station_data or not trip_data:
      raise ValueError("this metadata might not have station or trip stats")

stations = get_resource_data(station_data)
trip = get_resource_data(trip_data)

with open('stations.csv','wb') as file:
      file.write(stations)

with open('trips.csv','wb') as file:
      file.write(trip)

stations_df = pd.read_csv('stations.csv')
trip_df = pd.read_csv('trip.csv')

station_usage = trip_df['Start Station'].value_counts().reset_index()
station_usage.columns = ['station_name','trip_count']

stations_df = stations_df.merge(station_usage, how='left', left_on='station_name', right_on='station_name')
stations_df['trip_count'] = stations_df['trip_count'].fillna(0)

m = folium.Map(location=[43.65107, -79.347015], zoom_start=12)

for _, row in stations_df.iterrows():
    folium.CircleMarker(
        location=[row['Latitude'], row['Longitude']],
        radius=5 + row['trip_count'] / 1000,  
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.6,
        popup=f"{row['station_name']}: {row['trip_count']} trips"
    ).add_to(m)


m.save('bike_share_map.html')