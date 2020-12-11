checkboxes = document.getElementsByName('generation_format');
checkboxes[0].disabled = true;

checkboxes[0].addEventListener('change', function () {
    if (checkboxes[0].checked === true) {
        if (checkboxes[1].checked === true) {
            checkboxes[0].disabled = false;
            checkboxes[1].disabled = false;
        } else {
            checkboxes[0].disabled = true;
            checkboxes[1].disabled = false;
        }
    } else {
        if (checkboxes[1].checked === true) {
            checkboxes[0].disabled = false;
            checkboxes[1].disabled = true;
        } else {
            checkboxes[0].disabled = false;
            checkboxes[1].disabled = false;
        }
    }
});

checkboxes[1].addEventListener('change', function () {
    if (checkboxes[1].checked === true) {
        if (checkboxes[1].checked === true) {
            checkboxes[1].disabled = false;
            checkboxes[0].disabled = false;
        } else {
            checkboxes[1].disabled = true;
            checkboxes[0].disabled = false;
        }
    } else {
        if (checkboxes[0].checked === true) {
            checkboxes[1].disabled = false;
            checkboxes[0].disabled = true;
        } else {
            checkboxes[1].disabled = false;
            checkboxes[0].disabled = false;
        }
    }
});
