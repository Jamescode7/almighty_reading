$(function () {
  // 스크롤 시 .js-scroll-trigger 클래스가 붙은 링크에 대해 부드러운 스크롤 적용
  $('a.js-scroll-trigger[href^="#"]').on("click", function (e) {
    var target = $(this.hash);
    if (target.length) {
      e.preventDefault();
      $("html, body").animate(
        {
          scrollTop: target.offset().top - 70, // 네비게이션 바 높이 만큼 보정
        },
        600
      );
    }
  });
});
