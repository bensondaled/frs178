var csvdata;

var map = d3.geomap.choropleth()
    .geofile('/d3/d3-geomap/topojson/countries/USA.json')
    .projection(d3.geo.albersUsa)
    .duration(1000)
    .column('sentiment')
    .unitId('fips')
    .scale(1000)
    .legend(true);


function loadMap() {

    d3.csv('/data/data.csv', function(error, data) {
        csvdata = data;
        d3.select('#map')
        .datum(csvdata)
        .call(map.draw, map);
    });

}

function updateMap() {

    d3.csv('/data/data.csv', function(error, data) {
        csvdata = data;
        map.data = csvdata;
        map.column('sentiment').update();
        console.log(csvdata[1]['sentiment']);
        
    });

    setTimeout(updateMap, 5000); // update time
}

loadMap();
updateMap();
