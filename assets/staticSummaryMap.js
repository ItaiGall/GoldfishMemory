var initialLocation;
var map;
var marker;
var pagination = document.getElementsByClassName("paginate button is-light");
var table;

window.onpageshow = function(){
    initSumMap();
    getPositions();
    getEnumerator();
};
pagination.onclick = function(){
    initializePage();
};

function initializePage(){
    initSumMap();
    getPositions();
    getEnumerator();
}

function getEnumerator(){
    var start_index = parseInt(document.getElementById("start_index").innerText)-1;
    if(table == null){
        table = document.getElementById("myTable");
    }
    for(var i = 0; i < table.rows.length; i++){
        var index = parseInt(table.rows[i].cells[5].innerText);
        var new_ind = JSON.stringify(index+start_index);
        //new_ind.style.color = ;
        table.rows[i].cells[0].innerHTML = "<a href='{{ ps.get_absolute_url }}'>"+new_ind+"."+"</a>";
    };
}

function getPositions(){
    if(table == null){
        table = document.getElementById("myTable");
    }
    for(var i = 0; i < table.rows.length; i++){
        var mydata = table.rows[i].cells[4].innerText;
        var latLngString = mydata.split(",").map(Number);
        var latlng = {
            lat: parseFloat(latLngString[0]),
            lng: parseFloat(latLngString[1]),
        };
        createMarker(latlng);
    };
};

 function initSumMap() {
    //console.log(initialLocation);
    map = new google.maps.Map(document.getElementById("map"), {
      zoom: 13,
      center: initialLocation,
    });
    //createMarker(initialLocation);
 };

function createMarker(location) {
    const svgMarker = {
        path: "M10.453 14.016l6.563-6.609-1.406-1.406-5.156 5.203-2.063-2.109-1.406 1.406zM12 2.016q2.906 0 4.945 2.039t2.039 4.945q0 1.453-0.727 3.328t-1.758 3.516-2.039 3.070-1.711 2.273l-0.75 0.797q-0.281-0.328-0.75-0.867t-1.688-2.156-2.133-3.141-1.664-3.445-0.75-3.375q0-2.906 2.039-4.945t4.945-2.039z",
        fillColor: "red",
        fillOpacity: 0.8,
        strokeWeight: 0,
        rotation: 0,
        scale: 1,
        anchor: new google.maps.Point(15, 30),
    };
    marker = new google.maps.Marker({
      position: location,
      map: map,
      icon: svgMarker,
    });
};

 if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            initialLocation = {
                lat: parseFloat(position.coords.latitude),
                lng: parseFloat(position.coords.longitude),
                };
        });
    };