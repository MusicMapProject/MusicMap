if (document.URL.includes("gpu-external01.i.smailru.net")) {
chrome.runtime.sendMessage({
    method: 'POST',
    action: 'xhttp',
    url: 'http://gpu-external01.i.smailru.net:86/auth',
    data: window.location.hash.substr(1)
    }, function(responseText) {
		var user_id = document.URL.match( /user_id=\d+/i )[0].match( /\d+/i )[0];
		console.log(user_id);
        window.location.replace("https://vk.com/audios".concat(user_id));
		// alert(responseText);
        // Callback function to deal with the response
    });
}

// move music down
$('._audio_page_content_block').offset({top : 110});

var totalWigth = $('#page_body').width();
var centerTop;
var centerLeft;

function createPicture(name, id) {
	var ImgMusicMap = chrome.extension.getURL(name);
	var ImgMusicMap_button = '<img id=' + id + ' src="' + ImgMusicMap + '" style="width: ' + totalWigth + 'px;"' + '/>';
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


jQuery.fn.sortElements = (function(){
 
    var sort = [].sort;
 
    return function(comparator, getSortable) {
 
        getSortable = getSortable || function(){return this;};
 
        var placements = this.map(function(){
 
            var sortElement = getSortable.call(this),
                parentNode = sortElement.parentNode,
 
                // Since the element itself will change position, we have
                // to have some way of storing its original position in
                // the DOM. The easiest way is to have a 'flag' node:
                nextSibling = parentNode.insertBefore(
                    document.createTextNode(''),
                    sortElement.nextSibling
                );
 
            return function() {
 
                if (parentNode === this) {
                    throw new Error(
                        "You can't sort elements if any one is a descendant of another."
                    );
                }
 
                // Insert before flag:
                parentNode.insertBefore(this, nextSibling)
                $(parentNode).hide().fadeIn(180);
                // $(parentNode).slideToggle();
                // Remove flag:
                parentNode.removeChild(nextSibling);
 
            };
 
        });


 
        return sort.call(this, comparator).each(function(i){
            placements[i].call(getSortable.call(this));
        });
 
    };
 
})();

// add dots on Map
var addDot = function() {
	var full_id = $(this).attr("data-full-id");
	var title = $(this).data("audio");

    // $('#' + full_id).css({top: centerTop + randomInteger(), left: centerLeft + randomInteger()});
    if (full_id in predicts) {
    	$('.MusicMap').append('<img class="AudioDot" id="' + full_id + '" data-title="' + title[4] + ' «' + title[3] + '»"></div>');
	    $('#' + full_id).css({top: centerTop - (predicts[full_id][0] - 5) * totalWigth / 2 / 5, left: centerLeft + (predicts[full_id][1] - 5) * totalWigth / 2 / 5});
	    $('#' + full_id).after('<em style="position: absolute"></em>');
	    $('#' + full_id).next("em").css({top: $('#' + full_id).position().top - 20 + 'px', left: $('#' + full_id).position().left - 20 + 'px'}); 

	    // play music by click
	    $(document).on('click', '#' + full_id, function() {
            /*
            var ownerId = $('.audio_row').first().attr("data-full-id").split('_')[0];
            var path = '/mnt/ssd/musicmap_data/predict/' + ownerId

            var arr = document.getElementsByTagName('script');
            var userId = arr[1].innerHTML.match(/id: (\d+)/)[1];

            var audio_id = full_id.split('_')[1];

			chrome.runtime.sendMessage({
        		method: 'GET',
        		action: 'xhttp',
        		url: 'http://gpu-external01.i.smailru.net:86/playlist?user_id='
                    .concat(userId).concat('&predict=').concat(path).concat('&audio_id=').concat(audio_id)
        	}, function(playlist_id) {
                var actualCode = "getAudioPlayer().playPlaylist(vk.id.toString(), "
                	    .concat(playlist_id).concat(", '', '');");
	            var script = document.createElement('script');
    	        script.textContent = actualCode;
        	    (document.head||document.documentElement).appendChild(script);
            	script.remove();
        	});
            */


	        $("[data-full-id$='"+full_id+"']").click();

	        var sorted_fullid_list = fullid_sorted[full_id];
	        $('.audio_row').sortElements(function(a, b){
				// console.log($(a).attr('data-full-id'))
				// console.log(sorted_fullid_list.indexOf($(a).attr('data-full-id')))
				a_ = sorted_fullid_list.indexOf($(a).attr('data-full-id'))
				b_ = sorted_fullid_list.indexOf($(b).attr('data-full-id'))

				if (a_ === -1) {
					if (b_ !== -1) {
						console.log("kek")
						return 1
					}
				}

				if (b_ === -1) {
					if (a_ !== -1) {
						console.log("kek1")
						return -1
					}
				}

				return sorted_fullid_list.indexOf($(a).attr('data-full-id')) > sorted_fullid_list.indexOf($(b).attr('data-full-id')) ? 1 : -1;
			});
			
	    });

	    // animate 
	    $('#' + full_id).hover(function () {
	        $(this).next("em").stop(true, true).animate({opacity: "show"}, 'slow');
	        var hoverText = $(this).data("title");
	        $(this).next("em").text(hoverText);
	        $(this).animate({height: '25', width: '25'}, 500);
	    }, function () {
	        $(this).animate({height: '15', width: '15'}, 500);
	        $(this).next("em").stop(true, true).animate({opacity: "hide"}, 'slow');
	    });
	}
}

// create Map
var createMap = function() {

	centerTop = $('.MusicMap').position().top  + totalWigth * 0.75 / 2;
	centerLeft = $('.MusicMap').position().left  + totalWigth / 2;

	// var img = createPicture("imagesApp/background6.png", "backgroundMusicMap");
	// $('.MusicMap').append(img);
	// $('.MusicMap').hide().animate({opacity: "show"});
	$('#backgroundMusicMap').animate({opacity: "show"});
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

	var img = createPicture("imagesApp/background6.png", "backgroundMusicMap");
	$('.MusicMap').append(img);
	$('#backgroundMusicMap').hide()

    // create slider image
	img = createPicture("imagesApp/wolf.jpg", "slideImg");
	$('.MusicMap').append(img);
	$('#slideImg').hide().slideDown(1500);
	
	// Create Map
	$('#slideImg').animate({opacity: "hide"}, 1000, createMap);
  
})

function getCsv(filename, is_sort) {
    chrome.runtime.sendMessage({
    method: 'GET',
    action: 'xhttp',
    url: filename,
    }, function(data) {
        // console.log(data);
        if (is_sort === false) {
        	processData(data);
        	// alert("get csv")
        } else {
        	processSortData(data)
        	// alert("get sorted csv")
        }
        

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

var fullid_sorted = {}; 
function processSortData(allText) {
    var allTextLines = allText.split(/\r\n|\n/);
    var headers = allTextLines[0].split(',');

    for (var i=1; i<allTextLines.length; i++) {
        var data = allTextLines[i].split(',');
        fullid_sorted[data[0]] = data
    }
}

var userId = $('.audio_row').first().attr("data-full-id").split('_')[0];

getCsv('http://gpu-external01.i.smailru.net:86/mnt/ssd/musicmap_data/predict/' + userId, false);
getCsv('http://gpu-external01.i.smailru.net:86/mnt/ssd/musicmap_data/predict/' + userId + "_sorted", true);

console.log(predicts);

/*
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
		    // Callback function to deal with the response
		});
	}
})
*/