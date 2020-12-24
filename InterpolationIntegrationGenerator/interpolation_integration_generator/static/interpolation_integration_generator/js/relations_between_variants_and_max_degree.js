variants = document.getElementsByName("number_of_variants_in_string");
last_variant = variants[variants.length - 1];

degrees = document.getElementsByName("the_biggest_polynomial_degree");
last_degree = degrees[degrees.length - 1];

for (let i = 0; i < variants.length; i++) {
    variants[i].addEventListener("change", function () {
        if (this.value === "3") {
            last_degree.parentNode.hidden = true;
            if (degrees[degrees.length - 1].checked === true) {
                degrees[0].checked = true;
            }
        } else {
            last_degree.parentNode.hidden = false;
        }
    }, 0);
}

for (let i = 0; i < degrees.length; ++i) {
    degrees[i].addEventListener("change", function () {
        if (this.value === "6") {
            last_variant.parentNode.hidden = true;
            variants[0].checked = true;
        } else {
            last_variant.parentNode.hidden = false;
        }
    }, 0);
}


last_degree.addEventListener("change", function () {
    variants[0].checked = true;
});
