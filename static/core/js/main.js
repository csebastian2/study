setCarouselHeight('#features-carousel');

function setCarouselHeight(id)
{
    var slideHeight = [];
    $(id+' .item').each(function()
    {
        slideHeight.push($(this).height());
    });

    max = Math.max.apply(null, slideHeight);

    $(id+' .carousel-content').each(function()
    {
        $(this).css('height',max+'px');
    });
}
