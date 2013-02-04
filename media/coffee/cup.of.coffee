# Reload page
reload = () ->
  location.reload()

# Reload page, when clicking on kanji
$ ->
  $('.kanji').click ->
    location.reload()
