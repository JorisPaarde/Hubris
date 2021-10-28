$( window ).on( "load", function() { 
     $(".landscape-screen").toggleClass( 'd-none', (window.innerHeight < window.innerWidth));
});

window.addEventListener("orientationchange", function() {
    $(".landscape-screen").toggleClass( 'd-none', (window.innerHeight < window.innerWidth) );
    location.reload();
  });