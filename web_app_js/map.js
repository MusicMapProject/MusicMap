Plotly.d3.csv('https://github.com/MusicMapProject/MusicMap/blob/master/web_app/predictions', function(err, rows){
    // var YEAR = 2007;
    // var continents = ['Asia', 'Europe', 'Africa', 'Oceania', 'Americas'];
    // var POP_TO_PX_SIZE = 2e5;
    function unpack(rows, key) {
        return rows.map(function(row) { return row[key]; });
    };

    var data = {
            mode: 'markers',
            name: 'Music Map',
            x: unpack(rows, 'prediction_V'),
            y: unpack(rows, 'prediction_A'),
            text: unpack(rows, 'songnames'),
            marker: {
                // sizemode: 'area',
                size: 25,
//                sizeref: POP_TO_PX_SIZE
            }
        };

    var layout = {
        images: {
            opacity: 1,
            layer: "below",
            xref: "x",
            yref: "y",
            sizex: 8,
            sizey: 8,
            source: "http://static.tumblr.com/c7iuapz/0mEnlqrs8/a4e096545ff6937dbf066981adf56ffe.media.700x700.jpg",
            y: 9,
            x: 1,
            sizing: 'contain'
        },
        height: 850,
        width: 850,
        font: dict(color='#CCCCCC'),
        titlefont: dict(color='#CCCCCC', size='14'),
        yaxis: {
            "zeroline": False,
            "title": "Valence",
            "range": [
                1,
                9
            ],
            "ticklen": 1,
            "showgrid": False
        },
        xaxis: {
            "zeroline": False,
            "title": "Arousal",
            "range": [
                1,
                9
            ],
            "ticklen": 1,
            "showgrid": False
        },
        margin: {t: 20},
        hovermode: 'closest'
    };
    Plotly.plot('myDiv', data, layout, {showLink: false});
});