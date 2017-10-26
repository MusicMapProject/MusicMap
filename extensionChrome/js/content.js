// move music down
$('._audio_page_content_block').offset({top : 110});

var totalWigth = $('#page_body').width();
var centerTop;
var centerLeft;

function createPicture(name, id) {
	var ImgMusicMap = chrome.extension.getURL(name);
	var ImgMusicMap_button = '<img id=' + id + ' src="' + ImgMusicMap + '" style="width: ' + totalWigth + 'px"' + '/>';
	return ImgMusicMap_button;
};

window.onscroll = function() {
	$('._audio_friends_list_content').removeClass('audio_friends_fixed');

};


// random position
var randomInteger = function() {
	var max = totalWigth / 3.5;
	var min = -totalWigth / 3.5;
	return Math.random() * (max - min) + min;
}

// add dots on Map
var addDot = function() {
	var full_id = $(this).attr("data-full-id");
	var title = $(this).data("audio");

    // $('#' + full_id).css({top: centerTop + randomInteger(), left: centerLeft + randomInteger()});
    if (full_id in predicts) {
    	$('.MusicMap').append('<img class="AudioDot" id="' + full_id + '" data-title="' + title[4] + ' «' + title[3] + '»"></div>');
	    $('#' + full_id).css({top: centerTop - (predicts[full_id][0] - 5) * totalWigth / 2 / 4, left: centerLeft + (predicts[full_id][1] - 5) * totalWigth / 2 / 4});
	    $('#' + full_id).after('<em style="position: absolute"></em>');
	    $('#' + full_id).next("em").css({top: $('#' + full_id).position().top - 20 + 'px', left: $('#' + full_id).position().left - 20 + 'px'}); 

	    // play music by click
	    $(document).on('click', '#' + full_id, function() {
	        $("[data-full-id$='"+full_id+"']").click();
	    });

	    // animate 
	    $('#' + full_id).hover(function () {
	        $(this).next("em").stop(true, true).animate({opacity: "show"}, 'slow');
	        var hoverText = $(this).data("title");
	        $(this).next("em").text(hoverText);
	        $(this).animate({height: '30', width: '30'}, 500);
	    }, function () {
	        $(this).animate({height: '20', width: '20'}, 500);
	        $(this).next("em").stop(true, true).animate({opacity: "hide"}, 'slow');
	    });
	}
}

// create Map
var createMap = function() {
	centerTop = $('.MusicMap').position().top  + totalWigth / 2;
	centerLeft = $('.MusicMap').position().left  + totalWigth / 2;

	var img = createPicture("imagesApp/background6.png", "backgroundMusicMap");
	$('.MusicMap').append(img);
	// $('.MusicMap').hide().animate({opacity: "show"}, 'fast');
	$('.audio_row').each(addDot);	
}

// create image MusicMap
var img = createPicture("imagesApp/MusicMap.jpg", "ImgMusicMap");

$('._audio_page_content_block').before(img);
    
$('#ImgMusicMap').click(function() {
	// detete image MusicMap
	$('#ImgMusicMap').remove();

	//create new div MusicMap
	var newDiv = '<div class="MusicMap"></div>';
	$('._audio_page_content_block').before(newDiv);

    // create slider image
	var img = createPicture("imagesApp/wolf.jpg", "slideImg");
	$('.MusicMap').append(img);
	$('#slideImg').hide().slideDown(1500);
	
	// Create Map
	$('#slideImg').animate({opacity: "hide"}, 1000, createMap);
  
})

function getCsv(filename) {
    chrome.runtime.sendMessage({
    method: 'GET',
    action: 'xhttp',
    url: filename,
    }, function(data) {
        // console.log(data);
        processData(data);
    });
};

var predicts = {}; 
function processData(allText) {
    var allTextLines = allText.split(/\r\n|\n/);
    var headers = allTextLines[0].split(',');

    for (var i=1; i<allTextLines.length; i++) {
        var data = allTextLines[i].split(',');
        if (data.length == 3) {

            var id = data[0];
            var v = parseFloat(data[1]);
            var a = parseFloat(data[2]);
            predicts[id] = [v, a];
        }
    }
}

var userId = $('.audio_row').first().attr("data-full-id").split('_')[0];

getCsv('http://gpu-external01.i.smailru.net:86/mnt/ssd/musicmap_data/predict_tmp/' + userId);
console.log(predicts);


$("#document").ready(function() {
  // alert("kekekekek")
  if ( $( this ).height() > 100) {
    $( this ).addClass( "bigImg" );
  }

  // alert(musicPosts.length)
  for (var j = 0; j < musicPosts.length; j += 1) {
	  chrome.runtime.sendMessage({
	    method: 'POST',
	    action: 'xhttp',
	    url: 'http://gpu-external01.i.smailru.net:86/',
	    data: musicPosts[j]
		}, function(responseText) {
		    // alert(responseText);
		    /*Callback function to deal with the response*/
		});
	}
})