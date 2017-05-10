$(function() {

    $( "#new_office_block" ).hide();

    $( "#office_id" ).change(function() {
    if ($( this ).val() == "" ) {
        $( "#new_office_block" ).toggle("clip");
    } else {
        $( "#new_office_block" ).hide("clip");
    }
    });

    $(function(){
        $("#select_lang").change(function(){
            this.form.submit();
        });
    });

});
