

$(document).ready(function(){ // function disables search/submit button when the input form is not filled
(function() {
    $('form > input').keyup(function() {

        var empty = false;  // if input form empty
        $('form > input').each(function() {
            if ($(this).val() == '') {
                empty = true;
            }
        });

        if (empty) {
            $('#register').attr('disabled', 'disabled'); // disable is empty
        } else {
            $('#register').removeAttr('disabled'); // remove dissable attribute is input filled 
        }
    });
})()
});