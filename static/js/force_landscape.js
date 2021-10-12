$( window ).on( "load", function() {
    if ((window.innerHeight > 100) && (window.innerWidth > 100)){
        $(".landscape-screen").toggleClass( 'd-none', (window.innerHeight < window.innerWidth))
    };
});

window.addEventListener("orientationchange", function() {
    $(".landscape-screen").toggleClass( 'd-none', (window.innerHeight > window.innerWidth) );
  });