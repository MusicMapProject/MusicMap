
chrome.runtime.onMessage.addListener(function(request, sender, callback) {
	// alert("Reached Background.js");
    if (request.action == "xhttp") {
    	// alert("send.js");
    	var XHR = ("onload" in new XMLHttpRequest()) ? XMLHttpRequest : XDomainRequest;

        var xhttp = new XHR();
        var method = request.method ? request.method.toUpperCase() : 'GET';

        xhttp.onload = function() {
            callback(xhttp.responseText);
        };

        // xhttp.onerror = function() {
        //     // Do whatever you want on error. Don't forget to invoke the
        //     // callback to clean up the communication port.
        //     callback();
        // };
        xhttp.open(method, request.url, true);
        if (method == 'POST') {
            xhttp.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        }
        xhttp.send(request.data);
        return true; // prevents the callback from being called too early on return
    }
});

// function createPicture(name, id) {
// 	var ImgMusicMap = chrome.extension.getURL(name);
// 	var ImgMusicMap_button = '<img id=' + id + ' src="' + ImgMusicMap + '" style="width: ' + totalWigth + 'px"' + '/>';
// 	return ImgMusicMap_button;
// }


// // random position
// var randomInteger = function() {
// 	var max = totalWigth / 3.5;
// 	var min = -totalWigth / 3.5;
// 	return Math.random() * (max - min) + min;
// }

// // add dots on Map
// var addDot = function() {
// 	var full_id = $(this).attr("data-full-id");
// 	var title = $(this).data("audio");
// 	$('.MusicMap').append('<img class="AudioDot" id="' + full_id + '" data-title="' + title[4] + ' «' + title[3] + '»"></div>');

// 	$('#' + full_id).css({top: centerTop + randomInteger(), left: centerLeft + randomInteger()});
// 	$('#' + full_id).after('<em style="position: absolute"></em>');
// 	$('#' + full_id).next("em").css({top: $('#' + full_id).position().top - 20 + 'px', left: $('#' + full_id).position().left - 20 + 'px'}); 

// 	// play music by click
// 	$(document).on('click', '#' + full_id, function() {
//         $("[data-full-id$='"+full_id+"']").click();
//     });

//     // animate 
//     $('#' + full_id).hover(function () {
//     	$(this).next("em").stop(true, true).animate({opacity: "show"}, 'slow');
// 		var hoverText = $(this).data("title");
// 		$(this).next("em").text(hoverText);
// 		$(this).animate({height: '30', width: '30'}, 500);
//     }, function () {
// 		$(this).animate({height: '20', width: '20'}, 500);
// 		$(this).next("em").stop(true, true).animate({opacity: "hide"}, 'slow');
//     });
// }

// // create Map
// var createMap = function() {
// 	centerTop = $('.MusicMap').position().top  + totalWigth / 2;
// 	centerLeft = $('.MusicMap').position().left  + totalWigth / 2;

// 	var img = createPicture("imagesApp/background.png", "backgroundMusicMap");
// 	$('.MusicMap').append(img);
// 	// $('.MusicMap').hide().animate({opacity: "show"}, 'fast');
// 	$('.audio_row').each(addDot);	
// }

// // create image MusicMap
// var img = createPicture("imagesApp/MusicMap.jpg", "ImgMusicMap");
// $('._audio_page_content_block').before(img);
    
// $('#ImgMusicMap').click(function() {
// 	// detete image MusicMap
// 	$('#ImgMusicMap').remove();

// 	//create new div MusicMap
// 	var newDiv = '<div class="MusicMap"></div>';
// 	$('._audio_page_content_block').before(newDiv);

//     // create slider image
// 	var img = createPicture("imagesApp/wolf.jpg", "slideImg");
// 	$('.MusicMap').append(img);
// 	$('#slideImg').hide().slideDown(1500);
	
// 	// Create Map
// 	$('#slideImg').animate({opacity: "hide"}, 2000, createMap);
  
// })


 //  var XHR = ("onload" in new XMLHttpRequest()) ? XMLHttpRequest : XDomainRequest;

 //  var xhr = new XHR();

 //  // (2) запрос на другой домен :)
 //  xhr.open('GET', 'http://gpu-external01.i.smailru.net:85/', true);

 //  alert("sdgsdg");
 //  xhr.onload = function() {
 //    alert( this.responseText );
 //  }

 //  xhr.onerror = function() {
	// alert( 'Ошибка ' + this.status );
 //  }

	// xhr.send();
// });

// alert("kekekekek")
//   if ( $( this ).height() > 100) {
//     $( this ).addClass( "bigImg" );
//   }
//   var XHR = ("onload" in new XMLHttpRequest()) ? XMLHttpRequest : XDomainRequest;

//   var xhr = new XHR();

//   // (2) запрос на другой домен :)
//   xhr.open('POST', 'http://gpu-external01.i.smailru.net:85/', true);

//   alert("sdgsdg");
//   xhr.onload = function() {
//     alert( this.responseText );
//   }

//   xhr.onerror = function() {
// 	alert( 'Ошибка ' + this.status );
//   }

// 	xhr.send("спешим туда, где ждет беда");





// var XHR = ("onload" in new XMLHttpRequest()) ? XMLHttpRequest : XDomainRequest;

// var xhr = new XHR();

// // (2) запрос на другой домен :)
// xhr.open('GET', 'http://gpu-external01.i.smailru.net:85/', true);

// alert("sdgsdg");
// xhr.onload = function() {
//   alert( this.responseText );
// }

// xhr.onerror = function() {
//   alert( 'Ошибка ' + this.status );
// }

// xhr.send();