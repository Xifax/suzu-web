## Global states ##
# TODO: refactor!
locked = false
left_slided = false
right_slided = false

## Utility methods ##

# Reload page
reload = () ->
    location.reload()

# Redirect to route
redirect = (route) ->
    window.location = location.protocol + "//" + location.host + "/" + route

# Do not scroll those elements
$(window).scroll ->
    $('.fixed').css("top", Math.max(0, 20 - $(this).scrollTop()))

# Toggle divs
slideToggle = (divs...) ->
    $(div).slideToggle(100) for div in divs

toggle = (divs...) ->
    $(div).toggle() for div in divs

slide = (divs...) ->
    $(div).animate({width:'toggle'}, 100) for div in divs
    if $(div).css('display') == 'block'
        $(div).css('display', 'table')

# Lock|unlock items
lock = (items...) ->
    $('.' + item).toggleClass(item + '-locked') for item in items

# Prepare kanji details
prepare_details = (data) ->
    # Prepare details
    details = '<dl>'
    for kanji, info of data
        # kanji itself
        details += "<dt>#{kanji}</dt>"

        details += '<hr/>'
        # readings
        details += "#{info.on}"
        if info.kun
            details += " | #{info.kun}"
        if info.names
            details += " | #{info.names}"

        # translation (with trimmed ',')
        meaning = info.meanings.replace /[,\s]+$/g, ''
        details += "<br/><span class='meaning'>#{meaning}</span>"
        details += '</dd>'

    details += '</dl>'


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
            if $('.toolbar-right').css('display') == 'table'
                slide '.toolbar-right'
                right_slided = not right_slided

            if $('.toolbar-left').css('display') == 'table'
                slide '.toolbar-left'
                left_slided = not left_slided
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
# TODO: change icon on lock|unlock
$ -> $('#roll').click ->
        $.get('/lock')

# View current kanji
# TODO: copy to clipboard instead
$ -> $('#link').click ->
    # Get kanji
    kanji = $('.kanji').text().trim()
    redirect('view/' + kanji)
    # TODO: show notification

# Lookup examples for kanji
$ -> $('.lookup-button').click ->
    # Get current kanji
    kanji = $('.kanji').text().trim()
    # Display progressbar
    #$('.loader-left').fadeToggle(250)
    # TODO: Lookup examples for kanji


# Show related kanji when clicking on radical
$ -> $('.rad').click ->
    rad = $(this).text().trim()
    # Display progressbar
    $('.loader-left').fadeToggle(250)
    $.ajax '/related/' + rad,
        type: 'GET'
        dataType: 'json'
        success: (data, textStatus, jqXHR) ->
            text = '<div class="related-kanji">'
            # TODO: check if found something
            for kanji in data
                text += '<span class="single-kanji">' + kanji + '</span>'
            text += '</div>'

            if not right_slided
                $('.content-right').html(text)
                slide '.toolbar-right'
                right_slided = not right_slided
            else
                if $('.toolbar-right').css('display') == 'table'
                    $('.content-right').fadeOut(150,
                        (-> $(this).html(text).fadeIn(150))
                    )
            # Hide progressbar
            $('.loader-left').fadeToggle(250)


# Lookup related kanji info on click (single kanji are generated dynamically!)
$ -> $('.content-right').on('click', '.single-kanji', ->
    # Get kanji
    kanji = $(this).text().trim()
    # Display progressbar
    $('.loader-left').fadeToggle(250)
    # Query controller
    $.ajax '/kanji_info/' + kanji,
        type: 'GET'
        dataType: 'json'
        success: (data, textStatus, jqXHR) ->
            # TODO: check if found something
            # Prepare details
            details = prepare_details(data.info)

            # Animate details update
            # TODO: should probably move to separate function too
            if $('.toolbar-left').css('display') == 'table'
                $('.content-left').fadeOut(150,
                    (-> $(this).html(details).fadeIn(150))
                )
            else
                $('.content-left').html(details)

            # Display details toolbar
            if not left_slided
                slide '.toolbar-left'
                left_slided = not left_slided

            # Hide loader
            $('.loader-left').fadeToggle(100)
    )


# Lookup examples in weblio on click
$ -> $('ruby').click ->
    # Get usage text
    term = $(this).find('rb').text().trim()
    # Display progressbar
    $('.loader-left').fadeToggle(250)
    $.ajax '/info/' + term,
        type: 'GET'
        dataType: 'json'
        success: (data, textStatus, jqXHR) ->
            # If nothing is found -> display notification
            if data.examples.length is 0
                humane.log('Ooops, no examples found!',  {timeout: 2000})
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
            if $('.toolbar-right').css('display') == 'table'
                $('.content-right').fadeOut(150,
                    (-> $(this).html(text).fadeIn(150))
                )
            else
                $('.content-right').html(text)

            # Display examples
            if not right_slided
                slide '.toolbar-right'
                right_slided = not right_slided

            # Prepare details
            details = prepare_details(data.details)

            # Animate details update
            if $('.toolbar-left').css('display') == 'table'
                $('.content-left').fadeOut(150,
                    (-> $(this).html(details).fadeIn(150))
                )
            else
                $('.content-left').html(details)

            # Display details toolbar
            if not left_slided
                slide '.toolbar-left'
                left_slided = not left_slided

            # Hide loader
            $('.loader-left').fadeToggle(100)

## Home page end ##
