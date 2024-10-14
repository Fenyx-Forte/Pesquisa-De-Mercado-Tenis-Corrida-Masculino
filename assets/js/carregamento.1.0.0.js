if (document.getElementById("minha-pagina-carregamento")) {
    let seconds = 50;
    const countdownElement = document.getElementById("seconds");
    const timeUnitElement = document.getElementById("time-unit");

    function updateCountdown() {
        if (seconds > 0) {
            seconds--;
            countdownElement.textContent = seconds;
            timeUnitElement.textContent = seconds === 1 ? "segundo" : "segundos";
        }
    }

    setInterval(updateCountdown, 1000);
}
