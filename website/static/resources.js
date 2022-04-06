//JS script for resource rating modal
var title = "";
var userRating = "";
$(document).ready(function(){
    $(".rating input:radio").attr("checked", false);

    $('.rating input').click(function () {
        $(".rating span").removeClass('checked');
        $(this).parent().addClass('checked');
    });

    $('input:radio').change(
        function(){
        userRating = this.value;
      }); 

    $('.haveNotRead').click(function() {
        $('#ratingModal').modal('hide');
    }) 
    $('.contentLink').click(function() {
        title = this.innerHTML;
        category = this.id;  
        $('#ratingModal').modal('show');
    })
});

function getTitle() {
    $.ajax({
        type: "POST",
        data: {
            'title': title,
            'rating': userRating, 
            'category': category
        }
        });
        return true;
    };
    