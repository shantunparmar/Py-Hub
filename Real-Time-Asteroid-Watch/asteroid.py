#Real time Asteroid Watch by nasa
import requests, time
import webbrowser


today = time.strftime('%Y-%m-%d', time.gmtime())
print("Date: " + today)

#Our JSON request to retrieve data about asteroids approaching planet Earth.
url = "https://api.nasa.gov/neo/rest/v1/feed?start_date=" + today + "&end_date=" + today + "&api_key=DEMO_KEY"

r = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})

my_dict = r.json()


print("Today " + str(my_dict["element_count"]) + " asteroids will be passing close to planet Earth:")

asteroids = my_dict["near_earth_objects"]

f = open('astroidwatch.html','w')
message = "<link rel='stylesheet' type='text/css' href='df_style.css'/><table id='customers'><thead><tr><th>Asteroid Name</th><th>Average Diameter</th><th>Near by Approach Date & Time</th><th>Velocity</th><th>Distance to Earth</th></tr></thead><tbody>"
#Parsing all the JSON data:
for asteroid in asteroids:
    for field in asteroids[asteroid]:
        min_diameter = field["estimated_diameter"]["meters"]["estimated_diameter_min"]
        max_diameter = field["estimated_diameter"]["meters"]["estimated_diameter_min"]
        miss_distance = str(field["close_approach_data"][0]["miss_distance"]["kilometers"])
        as_name = field["name"]
        velocity = str(field["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"])
        diameter = str(round(((min_diameter+max_diameter)/2),2))
        close_approach = field["close_approach_data"][0]["close_approach_date_full"]
        
        message += "<tr><td>"+as_name+"</td><td>"+diameter+"</td><td>"+close_approach+"</td><td>"+velocity+"</td><td>"+miss_distance+"</td><tr>"
          
        f.write(message)
        
        #webbrowser.open_new_tab(filename)
   
        
        if field["is_potentially_hazardous_asteroid"]:   
          print ("This asteroid might be dangerous to planet Earth!")
        else:
          print ("This asteroid is safe")
          
message += "</tbody></html>"
f.close()       
