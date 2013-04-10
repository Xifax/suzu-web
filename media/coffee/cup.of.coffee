## Global states ##
locked = false
# TODO: refactor!
left_slided = false
right_slided = false

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

slide = (divs...) ->
    $(div).animate({width:'toggle'}, 150) for div in divs

# Lock|unlock items
lock = (items...) ->
    $('.' + item).toggleClass(item + '-locked') for item in items

## Home page ##

# Initialize tooltips
$ -> $('.tooltip').tooltipster({
    theme: '.tooltipster-theme',
    delay: 0,
    speed: 250,
    #animation: 'swing',
})

# Check toolbars status on page load
$ -> $.ajax '/toggled',
    type: 'GET'
    dataType: 'json'
    success: (data, textStatus, jqXHR) ->
        locked = data.status
        if locked
            lock 'kanji', 'circle'

# Lock toolbars, when clicking on kanji
$ -> $('.circle').mousedown( (event) ->
    switch event.which
        # left click
        when 1
            locked = not locked
            $.ajax '/toggle', type: 'GET'
            lock 'kanji', 'circle'

            # TODO: refactor!
            # TODO: fix error, when no popup on click
            if $('.toolbar-right').css('display') == 'block'
                slide '.toolbar-right'
                right_slided = not right_slided

            if $('.toolbar-left').css('display') == 'block'
                slide '.toolbar-left'
                left_slided = not left_slided
        # scroller click
        when 2
            location.reload()
)

# Toggle top|bottom divs on kanji hover
# TODO: fix when on page refresh no toolbars is shown
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

# Lookup examples in weblio on click
# TODO: show compound decomposition in left tab?
$ -> $('ruby').click ->
    # Get usage text
    term = $(this).find('rb').text().trim()
    # Display progressbar
    $('.loader-left').fadeToggle(250)
    # TODO: may perform one request, instead of a two!
    $.ajax '/info/' + term,
    #$.ajax '/examples/' + term,
        type: 'GET'
        dataType: 'json'
        success: (data, textStatus, jqXHR) ->
            # If nothing is found -> display notification
            if data.examples.length is 0
                humane.log('Ooops, no examples found!',  { timeout: 2000})
                $('.loader-left').fadeToggle(100)
                return

            # Prepare examples
            text = '<dl>'
            for example in data.examples
                for key, value of example
                    key = key.replace term, "<em>#{term}</em>"
                    text += "<dt>#{key}</dt><dd>#{value}</dd>"
            text += '</dl>'

            # Animate content updated
            if $('.toolbar-right').css('display') == 'block'
                $('.toolbar-right').fadeOut(150,
                    (-> $(this).html(text).fadeIn(150) )
                )
            else
                $('.toolbar-right').html(text)

            # Display examples
            if not right_slided
                slide '.toolbar-right'
                right_slided = not right_slided

            # Prepare details
            details = '<dl>'
            for kanji, info of data.details
                # kanji itself
                details += "<dt>#{kanji}</dt>"

                # readings
                details += "#{info.on}"
                if info.kun
                    details += " | #{info.kun}"
                if info.names
                    details += " | #{info.names}"

                # translation
                details += "<br/>#{info.meanings}"
                details += '</dd>'
                details += '<hr/>'

            details += '</dl>'

            # Animate details update
            if $('.toolbar-left').css('display') == 'block'
                $('.toolbar-left').fadeOut(150,
                    (-> $(this).html(details).fadeIn(150) )
                )
            else
                $('.toolbar-left').html(details)

            # Display details toolbar
            if not left_slided
                slide '.toolbar-left'
                left_slided = not left_slided

            # Hide loader
            $('.loader-left').fadeToggle(100)

## Home page end ##
