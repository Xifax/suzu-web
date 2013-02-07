# Reload page
reload = () ->
  location.reload()

# Reload page, when clicking on kanji
$ ->
  $('.kanji').click ->
    location.reload()

# Do not scroll those elements
$(window).scroll ->
    $('.fixed').css("top", Math.max(0, 20 - $(this).scrollTop()))
