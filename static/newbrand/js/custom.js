// Smooth scroll for internal links (Navbar → Anchor)
$(function () {
  $('a[href^="#"]').on('click', function (e) {
    var target = $(this.hash);
    if (target.length) {
      e.preventDefault();
      $('html, body').animate({
        scrollTop: target.offset().top - 70
      }, 600);
    }
  });
});
