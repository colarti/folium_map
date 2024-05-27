import folium
import pandas as pd

df = pd.read_csv('./Volcanoes.txt')
df_lat = df['LAT']
df_lon = df['LON']
df_elev = df['ELEV']

latlong = []
# folium requires the lat, long be in a list form
for i, item in enumerate(df_lat):
    latlong.append([df_lat[i], df_lon[i]])

#option2
# for lt, lg in zip(df_lat, df_lon):
#     latlong.append([lt, lg])


# This will center the map
map = folium.Map(location=[21.21637, -157.80597], zoom_start=6)

# Create a FeatureGroup that could be used as a layer
fg = folium.FeatureGroup(name='Volcanoes')
fg2 = folium.FeatureGroup(name='Population')
# Add a point ontop of the background Marker, CircleMarker
for i, coordinates in enumerate(latlong):
    if df.loc[i]['ELEV'] > 4000:
        height_color = 'red'
    elif df.loc[i]['ELEV'] >= 3000:
        height_color = 'blue'
    else:
        height_color = 'green'

    #option 1
    # fg.add_child(folium.Marker(coordinates, popup=f"{df.loc[i]['NAME']}, {df.loc[i]['LOCATION']}, {df.loc[i]['ELEV']}", icon=folium.Icon(color=height_color)))
    fg.add_child(folium.CircleMarker(coordinates, radius=8, popup=f"{df.loc[i]['NAME']}, {df.loc[i]['LOCATION']}, {df.loc[i]['ELEV']}", fill_color=height_color, color='grey', fill_opacity=0.7))
    #option 2 - NOT WORKING
    # iframe = folium.IFrame(html=f'<h4>Volcano Information:</h4><br>Height: {df.loc[i]["ELEV"]} m', width=200, height=100)
    # fg.add_child(folium.Marker(location=coordinates, popup=folium.Popup(iframe), icon=height_color))


# adding a new later for polygon layer (areas)
fg2.add_child(folium.GeoJson(data=open('./world.json', 'r', encoding='utf-8-sig').read(), 
                            style_function=lambda x: {'fillColor':'yellow' 
                                                      if x['properties']['POP2005'] < 10_000_000 
                                                      else 'green' if 20_000_000 > x['properties']['POP2005'] >= 10_000_000 
                                                      else 'red'}))



# Add all of the points to the background/main map
map.add_child(fg)
map.add_child(fg2)

map.add_child(folium.LayerControl())


map.save('map6_withGeoJSON_world.html')



