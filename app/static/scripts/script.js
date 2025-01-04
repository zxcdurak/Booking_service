let searchButton = document.querySelector(".search_button");
const urlParams = new URLSearchParams(window.location.search);

document.querySelector("#search_button").value= urlParams.get('location');
document.querySelector("#date_from").value = urlParams.get('date_from');
document.querySelector("#date_to").value = urlParams.get('date_to');


searchButton.addEventListener("click", function (e) {
    let date_from_value = document.querySelector("#date_from").value;
    let date_to_value = document.querySelector("#date_to").value;
    let search_value = document.querySelector("#search_button").value;
    window.location.href = `http://127.0.0.1:8000/pages/hotels?location=${search_value}&date_from=${date_from_value}&date_to=${date_to_value}`;
  });