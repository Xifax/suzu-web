# Reload page
reload = () ->
  location.reload()

# Do not scroll those elements
$(window).scroll ->
    $('.fixed').css("top", Math.max(0, 20 - $(this).scrollTop()))

## Home page ##

# Reload page, when clicking on kanji
$ ->
  $('.kanji').click ->
    location.reload()

# Toggle top|bottom divs on kanji hover
$ ->
    $('.kanji').hover ->
        #$('.kanji').mouseover ->
        $('.toolbar-top').slideToggle(300)
        $('.toolbar-bottom').slideToggle(300)

# Roll kanji for today
$ ->
    $('.roll').click ->
        $.get('/lock')
        reload()

## Home page end ##
