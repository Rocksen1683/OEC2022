import pandas
import geopandas
import folium
import webbrowser
import matplotlib.pyplot as plot


def map(file_name):

    data = pandas.read_csv(file_name)
    data.columns = ['Index', 'Latitude', 'Longitude', 'Type', 'Quantity', 'Loss']

    geometry = geopandas.points_from_xy(data.Longitude, data.Latitude)
    geodata = geopandas.GeoDataFrame(data[['Latitude', 'Longitude', 'Type', 'Quantity', 'Loss', 'Index']], geometry=geometry)

    map = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    data.Type.unique()

    figure, axis = plot.subplots(figsize=(10,8))
    map.plot(ax=axis, alpha=0.4, color='grey')
    geodata.plot(column='Type', ax=axis, legend=True)

    graph = folium.Map(location = [0.000, 0.000], tiles='Stamen Terrain', zoom_start = 2)

    geometry_list = [[point.xy[1][0], point.xy[0][0]] for point in geodata.geometry]
    count = 0

    folium.map.Marker(
        geometry_list[0], 
        icon=folium.features.DivIcon(
            icon_size=(250,36),
            icon_anchor=(0,0),
            html='<button style="font-size: 16pt">Starting Point</button>',
            )
        ).add_to(graph)
    
    folium.map.Marker(
        geometry_list[-1], 
        icon=folium.features.DivIcon(
            icon_size=(250,36),
            icon_anchor=(0,0),
            html='<button style="font-size: 16pt">Ending Point</button>',
            )
        ).add_to(graph)

    folium.map.Marker(
        [-6, -170], 
        icon=folium.features.DivIcon(
            icon_size=(100,10),
            icon_anchor=(0,0),
            html="<img src='legend.png' height=100px></img>",
            )
        ).add_to(graph)

    for coordinates in geometry_list:
        if geodata.Type[count] == "waste":
            type_color = "green"
        elif geodata.Type[count] == "local_sorting_facility":
            type_color = "blue"
        elif geodata.Type[count] == "regional_sorting_facility":
            type_color = "purple"
        else:
            type_color = "red"
        
        graph.add_child(folium.Marker(location = coordinates,
                                popup =
                                "Index: " + str(geodata.Index[count]) + '<br>' +
                                "Type: " + str(geodata.Type[count]) + '<br>' +
                                "Quantity: " + str(geodata.Quantity[count]) + '<br>'
                                "Loss: " + str(geodata.Loss[count]) + '<br>'
                                "Coordinates: " + str(geodata.Latitude[count]) + str(geodata.Longitude[count]),
                                icon = folium.Icon(color = "%s" % type_color)))
        count += 1

    for each in geometry_list:
        folium.Marker(each).add_to(graph)
    folium.PolyLine(geometry_list, color="red", weight=4, opacity=1).add_to(graph)

    graph.save("map.html")
    webbrowser.open("map.html")