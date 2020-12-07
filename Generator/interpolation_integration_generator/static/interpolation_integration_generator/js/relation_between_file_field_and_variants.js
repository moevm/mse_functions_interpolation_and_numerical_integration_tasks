let variants_type = document.getElementsByName('variants_type');

for (let i = 0; i < variants_type.length; i++) {
    variants_type[i].addEventListener('change', function () {
        if (this.value === 'digits') {
            document.getElementById('id_number_of_variants').disabled = false
            document.getElementById('id_number_of_variants').required = true
            document.getElementById('id_file_with_surnames').disabled = true
            document.getElementById('id_file_with_surnames').required = false
        } else if (this.value === 'surnames') {
            document.getElementById('id_number_of_variants').disabled = true
            document.getElementById('id_number_of_variants').required = false
            document.getElementById('id_file_with_surnames').disabled = false
            document.getElementById('id_file_with_surnames').required = true

        }
    });
}
