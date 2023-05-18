$(document).ready(function() {
// jQuery 代码写在这里
    $("#about-btn").click(function(event){
        alert("You clicked the button using jQuery!");
    });
    $("p").hover( function() {
        $(this).css('color', 'red');
        },
         function() {
        $(this).css('color', 'blue');
    });


});