import pandas
import geopandas
import matplotlib.pyplot as plot

data = pandas.read_csv('test cases/small/test_10_equal.csv')
data.columns = ['Index', 'Latitude', 'Longitude', 'Type', 'Quantity', 'Loss']
columns_dropped = ['Index', 'Quantity', 'Loss']
data.drop(columns_dropped, inplace=True, axis=1)

geometry = geopandas.points_from_xy(data.Longitude, data.Latitude)
geodata = geopandas.GeoDataFrame(data[['Latitude', 'Longitude', 'Type']], geometry=geometry)

map = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
data.Type.unique()

figure, axis = plot.subplots(figsize=(10,8))
map.plot(ax=axis, alpha=0.4, color='grey')
geodata.plot(column='Type', ax=axis, legend=True)
plot.title('Waste Cleaning')

plot.show()