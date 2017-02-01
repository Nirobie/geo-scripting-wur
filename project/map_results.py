import vincent as vincent
from vincent import (Visualization, Scale, DataRef, Data, PropertySet,
                     Axis, ValueRef, MarkRef, MarkProperties, Mark)
import folium, os, json
from folium import Map
from transform_shapefile import *

#==============================================================================
# ##Set the function to mask the pup-up to the polygon
# ##http://nbviewer.jupyter.org/gist/BibMartin/4b9784461d2fa0d89353
#==============================================================================

from branca.utilities import _locations_mirror
from folium.features import *
from folium.features import _locations_tolist
class MultiPolygon(MacroElement):
    """
    !! This is hacked from folium.features.MultiPolyLine !! 
    
    """
    def __init__(self, locations, color=None, weight=None,
                 opacity=None, latlon=True, popup=None):
        super(MultiPolygon, self).__init__()
        self._name = 'MultiPolygon'
        self.data = (_locations_mirror(locations) if not latlon else
                     _locations_tolist(locations))
        self.color = color
        self.weight = weight
        self.opacity = opacity
        if isinstance(popup, text_type) or isinstance(popup, binary_type):
            self.add_children(Popup(popup))
        elif popup is not None:
            self.add_children(popup)

        self._template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.multiPolygon(
                    {{this.data}},
                    {
                        {% if this.color != None %}color: '{{ this.color }}',{% endif %}
                        {% if this.weight != None %}weight: {{ this.weight }},{% endif %}
                        {% if this.opacity != None %}opacity: {{ this.opacity }},{% endif %}
                        });
                {{this._parent.get_name()}}.addLayer({{this.get_name()}});
            {% endmacro %}
            """)  # noqa

    def _get_self_bounds(self):
        """Computes the bounds of the object itself (not including it's children)
        in the form [[lat_min, lon_min], [lat_max, lon_max]]
        """
        bounds = [[None, None], [None, None]]
        for point in iter_points(self.data):
            bounds = [
                [
                    none_min(bounds[0][0], point[0]),
                    none_min(bounds[0][1], point[1]),
                ],
                [
                    none_max(bounds[1][0], point[0]),
                    none_max(bounds[1][1], point[1]),
                ],
            ]
        return bounds

#==============================================================================

##Function to create a map of the results

def create_map(results, cities, statename, time):
    
    #Gets the geoJSON for state and cities
    transformCities(cities)
    transformStates(statename)
    
    ##Creates the pup-up graph for the city results
    for cityid, df in results.iteritems():
        line = vincent.Line(df[['@realDonaldTrump', '@HillaryClinton']])
        line.axis_titles(x='date', y='normalized weighted composite score')
        line.legend(title='Queries')
        line.width=400
        line.height=200
        line.colors(brew='Set1')
        line.to_json('data/'+cityid+time+'.json')

    ##Creates the map 
    m = folium.Map([37.8384948, -95.4708095532], tiles="Mapbox Bright", zoom_start=8, min_zoom=5)
    fg = folium.map.FeatureGroup().add_to(m)
    
    
    geo_json_states = json.load(open('data/us_states/us_states.json'))
    for feature in geo_json_states['features']:
        if time == "before":
            fg.add_child(MultiPolygon(_locations_mirror(feature['geometry']['coordinates']),
                                   color='grey', weight=0, opacity=0.3))
        else:
            fg.add_child(MultiPolygon(_locations_mirror(feature['geometry']['coordinates']),
                                   color='red', weight=0, opacity=0.3))
    
    ##Add the cities layer with pop-up graph  
    geo_json_cities = json.load(open('data/us_cities/us_cities.json'))
    for feature in geo_json_cities['features']:
        
        ##Color of the polygon based on most positive nwcs per week
        places = open('data/' + cities, 'r')
        for line in places:
            attr = line.split(";")
            if attr[0] == feature['properties']['NAME10']:
                city_id = attr[1]
        
        if sum(results[city_id]['@realDonaldTrump']) > sum(results[city_id]['@HillaryClinton']):
            color = 'red'
        else:
            color = 'blue'
      
        fg.add_child(MultiPolygon(
        _locations_mirror(feature['geometry']['coordinates']),
        color=color,
        weight=0,
        opacity=1,
        popup = folium.Popup(max_width=650).add_child(folium.Vega(json.load(open('data/'+city_id+time+'.json')),
                                                                  width=620, height=270)),))

    m.save('sentiment_'+statename+'_'+time+'.html')