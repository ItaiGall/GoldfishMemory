`use strict`;
function refreshTime() {

  const timeDisplay = document.getElementById("time");
  const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour:'numeric', minute:'numeric' };
  const dateString = new Date().toLocaleString("en-GB", options);
  const formattedString = dateString.replace(", ", ",  ");
  timeDisplay.textContent = formattedString;
};
  setInterval(refreshTime, 1500);

window.onpageshow = function(){
    currentYear = new Date().getFullYear();
    if(currentYear > 2022){
        document.getElementById("copyright").innerText = " - " + currentYear;
    }



};