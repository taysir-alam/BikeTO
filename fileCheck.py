import requests

base_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca"


pack = "bike-share-toronto"

def get_package_metadata(pack):
    url = f"{base_url}/api/3/action/package_show"
    params = {"id": pack}
    response = requests.get(url, params=params)
    return response.json()

def get_resource_data(resource_url):
    response = requests.get(resource_url)
    return response.content

package = get_package_metadata(pack)

resources = {}

for resource in package["result"]["resources"]:
    resource_name = resource["name"]
    resource_url = resource["url"]
    resources[resource_name] = resource_url

for name, url in resources.items():
    print(f"Downloading {name} from {url}")
    data = get_resource_data(url)
    with open(f"{name}.csv", 'wb') as file:
        file.write(data)
    print(f"Saved {name}.csv")

print("All resources have been downloaded and saved.")
