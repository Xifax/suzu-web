## Global states ##
locked = false

## Utility methods ##

# Reload page
reload = () ->
  location.reload()

# Do not scroll those elements
$(window).scroll ->
    $('.fixed').css("top", Math.max(0, 20 - $(this).scrollTop()))

# Toggle divs
slideToggle = (divs...) ->
    $(div).slideToggle(150) for div in divs

toggle = (divs...) ->
    $(div).toggle() for div in divs

# Lock|unlock items
lock = (items...) ->
    $('.' + item).toggleClass(item + '-locked') for item in items

## Home page ##

# Check toolbars status on page load
$ -> $.ajax '/toggled',
    type: 'GET'
    dataType: 'json'
    success: (data, textStatus, jqXHR) ->
        locked = data.status
        if locked
            toggle '.toolbar-top', '.toolbar-bottom'
            lock 'kanji', 'circle'

# Lock toolbars, when clicking on kanji
$ -> $('.circle').mousedown( (event) ->
    switch event.which
        # left click
        when 1
            locked = not locked
            $.ajax '/toggle', type: 'GET'
            lock 'kanji', 'circle'
        # scroller click
        when 2
            location.reload()
)

# Toggle top|bottom divs on kanji hover
$ -> $('.kanji').mouseover ->
        if $('.toolbar-top').css('display') == 'none'
            slideToggle '.toolbar-top', '.toolbar-bottom'

$ -> $('.kanji').mouseout ->
        if $('.toolbar-top').css('display') == 'block' and not locked
            slideToggle '.toolbar-top', '.toolbar-bottom'

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
