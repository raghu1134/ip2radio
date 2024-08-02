import requests
import random
import os
from opencage.geocoder import OpenCageGeocode
from bs4 import BeautifulSoup

def load_proxies_from_file(file_path):
    proxies = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
    return proxies

def get_ip_info(ip_address, proxy=None):
    url = f"https://ipinfo.io/{ip_address}/json"
    try:
        if proxy:
            response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=10)
        else:
            response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch IP info{' using proxy ' + proxy if proxy else ''}: {e}")
        return None

def reverse_geocode_location(lat, lon):
    key = 'Open_Cage_Key'  # Replace with your OpenCage API key
    geocoder = OpenCageGeocode(key)
    result = geocoder.reverse_geocode(lat, lon)
    if result:
        full_location = result[0]['formatted']
        # Extract the first word from the location name
        single_word_location = full_location.split(',')[0].split()[0]
        return single_word_location
    return "N/A"

def search_location_on_opencellid(single_word_location):
    base_url = "https://opencellid.org/"
    search_url = f"{base_url}?q={single_word_location.replace(' ', '+')}"
    
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Optionally, you can parse the soup to extract specific information
        # For now, we'll return the search URL as requested
        return search_url
    except requests.RequestException as e:
        print(f"Failed to perform search on OpenCellID: {e}")
        return "N/A"

def show_ip_info():
    use_proxies = input("Do you want to use proxies? (yes/no): ").strip().lower()
    if use_proxies == "yes":
        proxy_file_path = input("Enter the path to the proxy file: ")
        proxies = load_proxies_from_file(proxy_file_path)
    else:
        proxies = None

    ip_address = input("Enter IP address: ")
    if ip_address:
        for attempt in range(5):  # Try up to 5 times
            proxy = random.choice(proxies) if proxies else None
            ip_info = get_ip_info(ip_address, proxy)
            if ip_info:
                location = ip_info.get('loc', 'N/A')
                if location != 'N/A':
                    lat, lon = location.split(',')
                    google_maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
                    single_word_location = reverse_geocode_location(lat, lon)
                    opencellid_search_url = search_location_on_opencellid(single_word_location)
                else:
                    google_maps_link = 'N/A'
                    single_word_location = 'N/A'
                    opencellid_search_url = 'N/A'
                
                info_message = (
                    f"IP: {ip_info.get('ip', 'N/A')}\n"
                    f"Hostname: {ip_info.get('hostname', 'N/A')}\n"
                    f"City: {ip_info.get('city', 'N/A')}\n"
                    f"Region: {ip_info.get('region', 'N/A')}\n"
                    f"Country: {ip_info.get('country', 'N/A')}\n"
                    f"Location: {location}\n"
                    f"Location Name (First Word): {single_word_location}\n"
                    f"Google Maps: {google_maps_link}\n"
                    f"OpenCellID Search URL: {opencellid_search_url}\n"
                    f"Org: {ip_info.get('org', 'N/A')}\n"
                    f"Postal: {ip_info.get('postal', 'N/A')}\n"
                    f"Timezone: {ip_info.get('timezone', 'N/A')}\n"
                    f"ASN: {ip_info.get('asn', {}).get('asn', 'N/A')}\n"
                    f"ASN Name: {ip_info.get('asn', {}).get('name', 'N/A')}\n"
                    f"ASN Domain: {ip_info.get('asn', {}).get('domain', 'N/A')}\n"
                    f"ASN Route: {ip_info.get('asn', {}).get('route', 'N/A')}\n"
                    f"ASN Type: {ip_info.get('asn', {}).get('type', 'N/A')}\n"
                    f"Company Name: {ip_info.get('company', {}).get('name', 'N/A')}\n"
                    f"Company Domain: {ip_info.get('company', {}).get('domain', 'N/A')}\n"
                    f"Company Type: {ip_info.get('company', {}).get('type', 'N/A')}\n"
                    f"Carrier Name: {ip_info.get('carrier', {}).get('name', 'N/A')}\n"
                    f"Carrier MCC: {ip_info.get('carrier', {}).get('mcc', 'N/A')}\n"
                    f"Carrier MNC: {ip_info.get('carrier', {}).get('mnc', 'N/A')}\n"
                    f"VPN: {ip_info.get('privacy', {}).get('vpn', 'N/A')}\n"
                    f"Proxy: {ip_info.get('privacy', {}).get('proxy', 'N/A')}\n"
                    f"Tor: {ip_info.get('privacy', {}).get('tor', 'N/A')}\n"
                    f"Relay: {ip_info.get('privacy', {}).get('relay', 'N/A')}\n"
                    f"Hosting: {ip_info.get('privacy', 'N/A')}\n"
                    f"Abuse Address: {ip_info.get('abuse', {}).get('address', 'N/A')}\n"
                    f"Abuse Country: {ip_info.get('abuse', {}).get('country', 'N/A')}\n"
                    f"Abuse Email: {ip_info.get('abuse', {}).get('email', 'N/A')}\n"
                    f"Abuse Name: {ip_info.get('abuse', 'N/A')}\n"
                    f"Abuse Network: {ip_info.get('abuse', {}).get('network', 'N/A')}\n"
                    f"Abuse Phone: {ip_info.get('abuse', {}).get('phone', 'N/A')}\n"
                )
                
                # Save the output to a .txt file named after the IP address
                with open(f"{ip_address}.txt", "w") as file:
                    file.write(info_message)
                
                print(info_message)
                print(f"Information saved to {ip_address}.txt")
                return
            else:
                print("Retrying with a different proxy...")
        
        print("Failed to retrieve IP information after multiple attempts.")

if __name__ == "__main__":
    show_ip_info()
