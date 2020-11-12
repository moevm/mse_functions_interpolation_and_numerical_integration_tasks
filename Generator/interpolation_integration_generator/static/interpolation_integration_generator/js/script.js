last_degree = document.getElementsByClassName("last-degree")[0];
last_number = document.getElementsByClassName("last-number")[0];
let radios = document.getElementsByName("number");
let degrees = document.getElementsByName("degree");

for (let i = 0; i < radios.length; i++) {
    radios[i].addEventListener("change", function () {
        if (this.value === "3") {
            console.log(1);
            last_degree.style.visibility = "hidden";
            if (degrees[degrees.length - 1].checked === true) {
                degrees[0].checked = true;
            }
        } else {
            console.log(2);
            last_degree.style.visibility = "visible";
        }
    }, 0);
}

for (let i = 0; i < degrees.length; ++i) {
    degrees[i].addEventListener("change", function () {
        if (this.value === "6") {
            console.log(1);
            last_number.style.visibility = "hidden";
            radios[0].checked = true;
        } else {
            console.log(2);
            last_number.style.visibility = "visible";
        }
    }, 0);
}


last_degree.addEventListener("change", function () {
        radios[0].checked = true;
    });
