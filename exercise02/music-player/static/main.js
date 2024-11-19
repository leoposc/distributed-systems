let current_song = 0;
let audio = null;
let duration = 0;
let playing = false;
let play_pause_btn = document.getElementById("play");
let grey_slider = document.getElementById("greyslider");
let fillbar = document.getElementById("fillbar");
let audio_slider = document.getElementById("slider");
let slider_nob = document.getElementById("slider-nob");
let currentPos, newPos, startPos = 0;

function setSong(index) {

    if (audio) {
        audio.pause();
    }

    const url = window.location.origin + '/play/' + songs[index];
    audio = new Audio(url);
    audio.addEventListener("loadeddata", () => {
        audio.controls = true;
        duration = audio.duration;
        document.getElementById("song-name").innerHTML = songs[index].title;
        document.getElementById("artist-name").innerHTML = songs[index].artist;
        document.getElementById("duration").innerHTML = convertTime(duration);
    })

    audio.play();
    play_pause_btn.innerHTML = '<i class="fas fa-solid fa-pause"></i>';
    playing = true;

    // Listen for when the song ends
    audio.addEventListener("ended", () => {
        nextSong();
    })
}

function nextSong() {
    audio.pause();
    if (current_song + 1 == songs.length) {
        current_song = 0;
    } else {
        current_song++;
    }
    setSong(current_song);

    // if it was playing then automatically play the next song
    if (playing) {
        audio.play();
        setSeeker();
    } else {
        fillbar.style.width = 0;
        slider_nob.style.left = 0;
    }
}

function prevSong() {
    audio.pause();

    if (current_song == 0) {
        current_song = songs.length - 1;
    } else {
        current_song--;
    }
    setSong(current_song);

    // if it was playing then automatically play the next song
    if (playing) {
        audio.play();
        setSeeker();
    } else {
        fillbar.style.width = 0;
        slider_nob.style.left = 0;
    }

}


function updateSeeker() {
    document.getElementById("timeplayed").innerHTML = convertTime(audio.currentTime);
    let percentage = (audio.currentTime / duration * 100).toFixed(1);
    fillbar.style.width = percentage + "%";
    slider_nob.style.left = (audio.currentTime / duration * grey_slider.clientWidth).toFixed(1) + "px";
}

function setSeeker() {
    audio.addEventListener("timeupdate", updateSeeker);
}







// Convert time to minutes and seconds so you can dislplay on page
function convertTime(time) {
    // time is already in seconds so there is no need to calculate secinds
    let secs = Math.floor(time);
    let mins = Math.floor(secs / 60);

    secs = secs % 60;
    mins = mins % 60;

    return mins.toString().padStart(2, '0') + ":" + secs.toString().padStart(2, '0')
}

// This function tracks the seeker
function moveObj(e) {
    // calculate the new position
    newPos = startPos - e.clientX;

    // with each move we also want to update the start X and Y
    startPos = e.clientX;

    // set the element's new position:
    if ((slider_nob.offsetLeft - newPos) >= 0 && (slider_nob.offsetLeft - newPos) <= grey_slider.clientWidth - slider_nob.clientWidth) {

        slider_nob.style.left = (slider_nob.offsetLeft - newPos) + "px";
        let percentage = ((slider_nob.offsetLeft - newPos) / (grey_slider.clientWidth - slider_nob.clientWidth) * 100).toFixed(1);
        fillbar.style.width = percentage + "%";

        audio.currentTime = (percentage / 100) * duration;

    }
}

play_pause_btn.addEventListener("click", () => {
    if (!playing) {
        audio.play();
        play_pause_btn.innerHTML = '<i class="fas fa-solid fa-pause"></i>';
        playing = true;
    } else {
        audio.pause();
        play_pause_btn.innerHTML = '<i class="fas fa-solid fa-play"></i>';
        playing = false;
    }
    setSeeker();
})

function searchSongs() {
    const query = document.getElementById('search-input').value;
    console.log(query);
    fetch(`/search/${query}`)
        .catch(error => console.error('Error:', error));
    console.log('searched');
}






// mousedown event occurs when a user presses the mouse button on an event
slider_nob.addEventListener("mousedown", (e) => {
    e.preventDefault();
    audio.removeEventListener("timeupdate", updateSeeker);

    // Get the starting position of the cursor
    startPos = e.clientX;

    // mousemove event occurs when a user moves their mouse
    document.addEventListener("mousemove", moveObj);

    // mouseup occurs when a user releases the mouse button
    document.addEventListener("mouseup", () => {
        document.removeEventListener("mousemove", moveObj);
        audio.addEventListener("timeupdate", updateSeeker);
    })
})


// setSong(current_song);

