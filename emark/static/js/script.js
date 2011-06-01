$("table").delegate('td','mouseover mouseleave click', function(e) {
  if (e.type == 'mouseover') {
    $(this).parent().children().addClass("table_hover");
  }
  else if (e.type == 'click') {
    window.location = $(this).parent().find('a').attr("href");
  }
  else {
    $(this).parent().children().removeClass("table_hover");
  }
});
