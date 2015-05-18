$(function() {
    $( "#obs" ).hide();
    $( "#office_id" ).change(function() {
    if ($( this ).val() == "0") {
        $( "#obs" ).toggle("clip");
    } else {
        $( "#obs" ).hide("clip");
    }
  });
});
