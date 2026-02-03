// Agency Theme JavaScript

(function($) {
    "use strict";

    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: ($($anchor.attr('href')).offset().top - 50)
        }, 1250, 'swing'); // Using 'swing' as 'easeInOutExpo' requires jQuery Easing plugin
        event.preventDefault();
    });

    // Highlight the top nav as scrolling occurs
    $('body').scrollspy({
        target: '.navbar-fixed-top',
        offset: 51 // Adjust this offset based on your navbar height
    });

    // Closes the Responsive Menu on Menu Item Click
    $('.navbar-collapse ul li a:not(.dropdown-toggle)').click(function() {
        $('.navbar-toggle:visible').trigger('click');
    });

    $('#mainNav').affix({
        offset: {
            top: 100
        }
    })

})(jQuery);