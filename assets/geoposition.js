var trackId;
var MyParkSpot;
var latitude = 0;
var longitude = 0;
var map;
var timestamp;
var MyAddress;
var PS_ID;
var marker;
var geocoder;
var infowindow;
var flag;
var myString;

//Function from Django documentation
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

function ButtonToggle() {
    var recordButton = document.getElementById("recordPark");
       if (recordButton.value === "Start parking here") {
                recordButton.value = "Stop parking here";
                clearTracking();
                myString = getContentString(1);
                marker.setDraggable(false);
                infowindow.setContent('<div id="bodyContent">' + myString +"</div>");
                infowindow.open(map, marker);
                saveSpotToDB();
                //in case that data is saved in local storage
                /*.then(response => window.localStorage.setItem
                ('my_ps', encodeURI(JSON.stringify({ "lat": latitude, "lng": longitude, "address": MyAddress, "id": PS_ID }))));*/
                //console.log("Fixed");
       } else {
            if (window.confirm("Do wish to log the moment you left the last recorded parking spot?")) {
                finalizeSpotinDB().then(response => initVars());
                console.log("Released");
            } else {
                console.log("");
            };
            recordButton.value = "Start parking here";
            myString = getContentString(0);
            //in case that data was saved in local storage
            //localStorage.clear();
            trackMe();
       };
};

function saveSpotToDB(){
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    if (timestamp == null) {
        timestamp = new Date().toUTCString();
    }
    var obj = {"latitude": latitude, "longitude": longitude, "timestamp": timestamp, "MyAddress": MyAddress, "timezone": timezone };
    var myJSON = JSON.stringify(obj);
    return $.ajax({
        type:"POST",
        dataType: "json",
        url:"ps/create_ps/",
        data:{
            "myJSON": myJSON,
            csrfmiddlewaretoken: getCookie('csrftoken'),
        },
        success: function (data) {
            PS_ID = data['id'];
            console.log(data['status']);
        },
        error: function(status, error) {
            console.log("error: "+error+", "+ status);
        }
    });
};

function finalizeSpotinDB(){
    timestamp = new Date().toUTCString();
    var obj = { "timestamp": timestamp, "record_to_be_closed": PS_ID };
    var myJSON2 = JSON.stringify(obj);
    return $.ajax({
        type:"POST",
        dataType: "json",
        url:"ps/finalize_ps/",
        data:{
            "myJSON2": myJSON2,
        },
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        success: function (data) {
            console.log(data['status']);
        },
        error: function(status, error) {
            console.log("error: "+error+", "+ status);
        }
    });
};

function trackMe() {
    options = {
        timeout: 30000,
        maximumAge: 20000,
    };
    trackId = navigator.geolocation.watchPosition(showPosition, showError, options);
};

function clearTracking() {
    if (trackId) {
            navigator.geolocation.clearWatch(trackId);
            trackId = null;
    }
};

function initVars() {
    latitude = 0;
    longitude = 0;
    MyParkSpot = null;
    MyAddress = null;
    timestamp = null;
    PS_ID = 0;
    document.getElementById("location").innerHTML = "...";
}

function showPosition(position) {
  if (position.coords.latitude != latitude || position.coords.longitude != longitude) {
      latitude = position.coords.latitude;
      longitude = position.coords.longitude;

      MyParkSpot = {
        lat: parseFloat(latitude),
        lng: parseFloat(longitude),
      };

      timestamp = new Date(position.timestamp).toUTCString();

      if (map == null) {
        flag = 0;
        showMap(MyParkSpot, flag);
      } else {
        setMarker();
        };
  };
};

function getContentString(flag){
   var contentString = "<p>Your current parking spot is adjacent to<br>" +
   "<b>" + MyAddress + "</b></p>" + "<p><b>** You can drag the marker for corrections **</b></p>";
    if (flag ==1){
        contentString = "<p>Your current parking spot is adjacent to<br>" +
        "<b>" + MyAddress + "</b></p>";
    };
    return contentString;
}

function showMap(MyParkSpot, flag) {
    if(flag == 1) {
        map = new google.maps.Map(document.getElementById("map"), {
            zoom: 17,
            center: MyParkSpot,
        });
        marker = new google.maps.Marker({
            position: MyParkSpot,
            map: map,
        });
        infowindow = new google.maps.InfoWindow();
        myString = getContentString(1);
        infowindow.setContent('<div id="bodyContent">' + myString +"</div>");
        infowindow.open(map, marker);
        document.getElementById("location").innerHTML = "<b>"+MyAddress+"</b>";
        if (geocoder == null) {
            geocoder = new google.maps.Geocoder();
        }
    } else {
        map = new google.maps.Map(document.getElementById("map"), {
            zoom: 17,
            center: MyParkSpot,
        });
        geocoder = new google.maps.Geocoder();
        infowindow = new google.maps.InfoWindow();
        setMarker();
    }
};

function setMarker(){
    //create new marker only if necessary or set the old one
    if (marker) {
       marker.setOptions({
            position: MyParkSpot,
            opacity: 0.7,
            label: "P",
            draggable: true,
            animation: google.maps.Animation.DROP,
            map: map,
       });
       //geocodeLatLng(map);
    } else {
      marker = new google.maps.Marker({
            position: MyParkSpot,
            opacity: 0.7,
            label: "P",
            draggable: true,
            animation: google.maps.Animation.DROP,
            map: map,
          });
      };
      //add listeners for moving events
      google.maps.event.addListener(map, "click", (event) => {
            latitude = parseFloat(event.latLng.lat());
            longitude = parseFloat(event.latLng.lng());
            MyParkSpot = {
                lat: latitude,
                lng: longitude,
            };
            map.panTo(MyParkSpot);
            marker.setPosition(MyParkSpot);
            geocodeLatLng(map);
      });

      google.maps.event.addListener(marker, 'dragend', function() {
            latitude = marker.getPosition().lat();
		    longitude = marker.getPosition().lng();
		    MyParkSpot = {
                lat: latitude,
                lng: longitude,
            };
            //console.log(MyParkSpot);
            geocodeLatLng(map);
      });
    //finally
    geocodeLatLng(map);
};

function geocodeLatLng(map) {
  geocoder
    .geocode({ location: MyParkSpot })
    .then((response) => {
      if (response.results[0]) {
        MyAddress = response.results[0].formatted_address;
        myString = getContentString(0);
        infowindow.setContent('<div id="bodyContent">' + myString +"</div>");
        infowindow.open(map, marker);
        document.getElementById("location").innerHTML = "<b>"+MyAddress+"</b>";
        //console.log(MyAddress);
        } else {
        window.alert("No results found");
        }
    }).catch((e) => window.alert("Geocoder failed due to: " + e));
};

function showError(error) {
  switch(error.code) {
    case error.PERMISSION_DENIED:
      alert("User denied the request for Geolocation.");
      break;
    case error.POSITION_UNAVAILABLE:
      alert("Location information is unavailable.");
      break;
    case error.TIMEOUT:
      alert("The request to get user location timed out.");
      break;
    case error.UNKNOWN_ERROR:
      alert("An unknown error occurred.");
      break;
  }
};

function init() {
  /* #Version if current session is stored URI encoded in local storage of browser
  if (localStorage.length > 0) {
        document.getElementById("recordPark").value = "Stop parking here";
        const intermediate = Object.values(JSON.parse(decodeURI(window.localStorage.getItem('my_ps'))));
        latitude = parseFloat(intermediate[0]);
        longitude = parseFloat(intermediate[1]);
        MyParkSpot = {
            lat: parseFloat(intermediate[0]),
            lng: parseFloat(intermediate[1]),
        };
        console.log(MyParkSpot);
        MyAddress = intermediate[2];
        PS_ID = parseInt(intermediate[3]);
        myString = getContentString(1);
        flag = 1;
        showMap(MyParkSpot, flag);
  }else{ */
    open_session_content = document.getElementById("open_session").innerHTML;
    if(open_session_content != ""){
        document.getElementById("recordPark").value = "Stop parking here";
        var raw_data = JSON.parse(open_session_content);
        latitude = parseFloat(raw_data[0]["fields"]["my_latitude"]);
        longitude = parseFloat(raw_data[0]["fields"]["my_longitude"]);
        MyAddress = raw_data[0]["fields"]["my_address"];
        MyParkSpot = {
                lat: latitude,
                lng: longitude,
            };
        PS_ID = parseInt(raw_data[0]["pk"]);
        myString = getContentString(1);
        flag = 1;
        showMap(MyParkSpot, flag);
    }else{
      if (navigator.geolocation) {
        trackMe();
      } else {
        alert("Geolocation is not supported by this browser.");
      }
     };
};