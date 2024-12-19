let dateStr = "{% now 'Y-d-m' %}T{% now 'H:i:s' %}Z";
let serverDate = Date.parse(dateStr);
let now = Date.now();
let diffTime = Math.abs(serverDate - now);
let diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
let date = new Date(diffDays < 1 ? now : serverDate);
$("#year").text(date.getFullYear());