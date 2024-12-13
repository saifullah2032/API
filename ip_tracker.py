import requests
import folium
import webbrowser

def track_ip_location(sender_ip, receiver_ip):
    """Track the IP location and show on the map"""
    
    def get_ip_location(ip):
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        return response.json()
    
    # Get  sender and receiver IPs
    sender_location = get_ip_location(sender_ip)
    receiver_location = get_ip_location(receiver_ip)
    
    m = folium.Map(location=[20, 0], zoom_start=2) 
    
    # Mark sender,receiver location
    if "loc" in sender_location:
        lat, lon = map(float, sender_location["loc"].split(","))
        folium.Marker([lat, lon], popup=f"Sender: {sender_ip}").add_to(m)
    
   
    if "loc" in receiver_location:
        lat, lon = map(float, receiver_location["loc"].split(","))
        folium.Marker([lat, lon], popup=f"Receiver: {receiver_ip}").add_to(m)
    
    # Save map to HTML file
    map_file = "ip_locations_map.html"
    m.save(map_file)
    print(f"IP locations have been mapped and saved as '{map_file}'.")
    
    # Open the map in the default web browser
    webbrowser.open(map_file)
