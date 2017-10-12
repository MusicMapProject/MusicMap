Plotly.d3.csv('/data/preprocess_data_our_audio/predictions', function(err, rows){
    function unpack(rows, key) {
        console.log(rows[0][key])
        return rows.map(function(row) { return row[key]; });
    };

    var data = {
            type: 'scatter',
            mode: 'markers',
            name: 'Music Map',
            x: unpack(rows, 'prediction_V'),
            y: unpack(rows, 'prediction_A'),
            text: unpack(rows, 'songnames'),
            marker: {
                size: 25,
                opacity: 0.8,
                color: "#ffba00"
            }
        };

    var layout = {
        images: [{
            opacity: 1,
            xref: "x",
            yref: "y",
            sizex: 8,
            sizey: 8,
            layer: "below",

            source: "http://static.tumblr.com/c7iuapz/0mEnlqrs8/a4e096545ff6937dbf066981adf56ffe.media.700x700.jpg",
            y: 9,
            x: 1,
            sizing: 'stretch'
        }],
        height: 850,
        width: 850,
        font: {
            color:'#CCCCCC'
        },
        titlefont: {
            color: '#CCCCCC', 
            size: '14',
            },
        yaxis: {
            "zeroline": false,
            "title": "Valence",
            "range": [
                1,
                9
            ],
            "ticklen": 1,
            "showgrid": false
        },
        xaxis: {
            "zeroline": false,
            "title": "Arousal",
            "range": [
                1,
                9
            ],
            "ticklen": 1,
            "showgrid": false
        },
        margin: {t: 20},
        hovermode: 'closest'
    };

    Plotly.plot('myDiv', [data], layout
                // , {showLink: false}
               );
});