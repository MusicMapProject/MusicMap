<head>
<!-- Includes the necessary CSS and Javascript libraries for full customization -->
<script type="text/javascript" src="js/SSUhtml5Audio.js"></script>
<link rel="stylesheet" type="text/css" href="css/SSUhtml5audio.css"/>
</head>
<audio id="song" ontimeupdate="updateTime()">
<source src="path/to/audio.mp3" type="audio/mp3"/>
  Your browser does not support the audio tag.
</audio>
<!-- Div that plays song, onclick calls the javascript play function and passes the
id of the audio tag with the appropriate song -->
<div id="songPlay" onclick="play('song')">Play</div>
<!-- Div that pauses the song when clicked.  Calls the pause button when clicked. -->
<div id="songPause" onclick="pause()">Pause</div>
<!-- Div that switches rather or not to play or pause the song based off of song state -->
<div id="songPlayPause" onclick="playPause('song')">PlayPause</div>
<!-- Div that stops the song when clicked -->
<div id="songStop" onclick="stopSong()">Stop</div>
<!-- Div that updates with current song time while playing -->
<div id="songTime">0:00 / 0:00</div>
<div id="volumeUp" onclick="changeVolume(10, 'up')">Plus</div><br>
<div id="volumeDown" onclick="changeVolume(10, 'down')">Minus</div>
<!-- Volume Meter sets the new volume on click.  The Volume Status div is embedded inside so it can grow
within bounds to simulate percentage feel -->
<div id="volumeMeter" onclick="setNewVolume(this,event)"><div id="volumeStatus"></div></div>
<span id="volumeThirty" onclick="volumeUpdate(30)">VOLUME 30</span>
<span id="volumeSixty" onclick="volumeUpdate(60)">VOLUME 60</span>
<span id="volumeNinety" onclick="volumeUpdate(90)">VOLUME 90</span>
<!-- Song Slider tracks progress on song time change, if you click it sets the distance into the song
based on the percentage of where was clicked -->
<div id="songSlider" onclick="setSongPosition(this,event)"><div id="trackProgress"></div></div>
