$('#likes').click(function(){
 var catid;
 catid = $(this).attr("data-catid");
 $.get('/rango/like/',{category_id: catid},function(data){
    $('#like_count').html(data);
    $('#likes').hide();
 });


});


$('#suggestion').keyup(function(){
    var qurey;
    qurey = $(this).val();
    $.get('/rango/suggest/',{suggestion:qurey},function(data){
        $('#cats').html(data);
    });

});