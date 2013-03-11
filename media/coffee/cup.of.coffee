# States
# TODO: store in session -> get using ajax -> set on page load
locked = false

# Reload page
reload = () ->
  location.reload()

# Do not scroll those elements
$(window).scroll ->
    $('.fixed').css("top", Math.max(0, 20 - $(this).scrollTop()))

# Toggle divs
toggle = (divs...) ->
    $(div).slideToggle(300) for div in divs

## Home page ##

# Lock toolbars, when clicking on kanji
$ -> $('.circle').mousedown( (event) ->
    switch event.which
        # left click
        when 1
            locked = not locked
            # TODO: set session variable
            $('.kanji').toggleClass('kanji-locked')
            $('.circle').toggleClass('circle-locked')
        # scroller click
        when 2
            location.reload()
)

# Toggle top|bottom divs on kanji hover
$ -> $('.kanji').mouseover ->
        if $('.toolbar-top').css('display') == 'none'
            toggle '.toolbar-top', '.toolbar-bottom'

$ -> $('.kanji').mouseout ->
        if $('.toolbar-top').css('display') == 'block' and not locked
            toggle '.toolbar-top', '.toolbar-bottom'

# Roll kanji for today
$ -> $('.roll').click ->
        $.get('/lock')
        reload()

# Update definition on usage hover
$ -> $('ruby').hover ->
    #$('.help').fadeToggle(150)
    #$('#' + this.id + '.definition').fadeToggle(300)
    $('.help').toggle()
    $('#' + this.id + '.definition').toggle()

# TODO: Show similar words, when clicking on kanji usage

## Home page end ##
