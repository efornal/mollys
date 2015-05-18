$(function() {
    $( "#new_office_block" ).hide();
    $( "#office_id" ).change(function() {
    if ($( this ).val() == "0") {
        $( "#new_office_block" ).toggle("clip");
    } else {
        $( "#new_office_block" ).hide("clip");
    }
  });
});
