(function() {
  var left_slided, lock, locked, prepare_details, redirect, reload, right_slided, slide, slideToggle, toggle,
    __slice = [].slice;

  locked = false;

  left_slided = false;

  right_slided = false;

  reload = function() {
    return location.reload();
  };

  redirect = function(route) {
    return window.location = location.protocol + "//" + location.host + "/" + route;
  };

  $(window).scroll(function() {
    return $('.fixed').css("top", Math.max(0, 20 - $(this).scrollTop()));
  });

  slideToggle = function() {
    var div, divs, _i, _len, _results;
    divs = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
    _results = [];
    for (_i = 0, _len = divs.length; _i < _len; _i++) {
      div = divs[_i];
      _results.push($(div).slideToggle(100));
    }
    return _results;
  };

  toggle = function() {
    var div, divs, _i, _len, _results;
    divs = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
    _results = [];
    for (_i = 0, _len = divs.length; _i < _len; _i++) {
      div = divs[_i];
      _results.push($(div).toggle());
    }
    return _results;
  };

  slide = function() {
    var div, divs, _i, _len;
    divs = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
    for (_i = 0, _len = divs.length; _i < _len; _i++) {
      div = divs[_i];
      $(div).animate({
        width: 'toggle'
      }, 100);
    }
    if ($(div).css('display') === 'block') {
      return $(div).css('display', 'table');
    }
  };

  lock = function() {
    var item, items, _i, _len, _results;
    items = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
    _results = [];
    for (_i = 0, _len = items.length; _i < _len; _i++) {
      item = items[_i];
      _results.push($('.' + item).toggleClass(item + '-locked'));
    }
    return _results;
  };

  prepare_details = function(data) {
    var details, info, kanji, meaning;
    details = '<dl>';
    for (kanji in data) {
      info = data[kanji];
      details += "<dt>" + kanji + "</dt>";
      details += '<hr/>';
      details += "" + info.on;
      if (info.kun) {
        details += " | " + info.kun;
      }
      if (info.names) {
        details += " | " + info.names;
      }
      meaning = info.meanings.replace(/[,\s]+$/g, '');
      details += "<br/><span class='meaning'>" + meaning + "</span>";
      details += '</dd>';
    }
    return details += '</dl>';
  };

  $(function() {
    return $('.tooltip').tooltipster({
      theme: '.tooltipster-theme',
      delay: 0,
      speed: 250
    });
  });

  $(function() {
    return $.ajax('/toggled', {
      type: 'GET',
      dataType: 'json',
      success: function(data, textStatus, jqXHR) {
        locked = data.status;
        if (locked) {
          return lock('kanji', 'circle');
        }
      }
    });
  });

  $(function() {
    return $('.circle').mousedown(function(event) {
      switch (event.which) {
        case 1:
          locked = !locked;
          $.ajax('/toggle', {
            type: 'GET'
          });
          lock('kanji', 'circle');
          if ($('.toolbar-right').css('display') === 'table') {
            slide('.toolbar-right');
            right_slided = !right_slided;
          }
          if ($('.toolbar-left').css('display') === 'table') {
            slide('.toolbar-left');
            return left_slided = !left_slided;
          }
          break;
        case 2:
          return location.reload();
      }
    });
  });

  $(function() {
    return $('.kanji').mouseover(function() {
      if ($('.toolbar-top').css('display') === 'none') {
        return slideToggle('.toolbar-top', '.toolbar-bottom');
      }
    });
  });

  $(function() {
    return $('.kanji').mouseout(function() {
      if ($('.toolbar-top').css('display') === 'block' && !locked) {
        return slideToggle('.toolbar-top', '.toolbar-bottom');
      }
    });
  });

  $(function() {
    return $('#roll').click(function() {
      return $.get('/lock');
    });
  });

  $(function() {
    return $('#link').click(function() {
      var kanji;
      kanji = $('.kanji').text().trim();
      return redirect('view/' + kanji);
    });
  });

  $(function() {
    return $('.lookup-button').click(function() {
      var kanji;
      return kanji = $('.kanji').text().trim();
    });
  });

  $(function() {
    return $('#fav').click(function() {
      var kanji;
      kanji = $('.kanji').text().trim();
      return $.ajax('/toggle_favorite/' + kanji, {
        type: 'GET',
        dataType: 'json',
        success: function(data, textStatus, jqXHR) {
          if (data.result === 'fav') {
            $('#fav').removeClass('icon-check');
            $('#fav').addClass('icon-cancel');
            return humane.log("" + kanji + " added to favorites!", {
              timeout: 1000
            });
          } else {
            $('#fav').removeClass('icon-cancel');
            $('#fav').addClass('icon-check');
            return humane.log("" + kanji + " removed from favorites!", {
              timeout: 1000
            });
          }
        }
      });
    });
  });

  $(function() {
    return $('.rad').click(function() {
      var rad;
      rad = $(this).text().trim();
      $('.loader-left').fadeToggle(250);
      return $.ajax('/related/' + rad, {
        type: 'GET',
        dataType: 'json',
        success: function(data, textStatus, jqXHR) {
          var kanji, text, _i, _len;
          text = '<div class="related-kanji">';
          for (_i = 0, _len = data.length; _i < _len; _i++) {
            kanji = data[_i];
            text += '<span class="single-kanji">' + kanji + '</span>';
          }
          text += '</div>';
          if (!right_slided) {
            $('.content-right').html(text);
            slide('.toolbar-right');
            right_slided = !right_slided;
          } else {
            if ($('.toolbar-right').css('display') === 'table') {
              $('.content-right').fadeOut(150, (function() {
                return $(this).html(text).fadeIn(150);
              }));
            }
          }
          return $('.loader-left').fadeToggle(250);
        }
      });
    });
  });

  $(function() {
    return $('.content-right').on('click', '.single-kanji', function() {
      var kanji;
      kanji = $(this).text().trim();
      $('.loader-left').fadeToggle(250);
      return $.ajax('/kanji_info/' + kanji, {
        type: 'GET',
        dataType: 'json',
        success: function(data, textStatus, jqXHR) {
          var details;
          details = prepare_details(data.info);
          if ($('.toolbar-left').css('display') === 'table') {
            $('.content-left').fadeOut(150, (function() {
              return $(this).html(details).fadeIn(150);
            }));
          } else {
            $('.content-left').html(details);
          }
          if (!left_slided) {
            slide('.toolbar-left');
            left_slided = !left_slided;
          }
          return $('.loader-left').fadeToggle(100);
        }
      });
    });
  });

  $(function() {
    return $('ruby').click(function() {
      var term;
      term = $(this).find('rb').text().trim();
      $('.loader-left').fadeToggle(250);
      return $.ajax('/info/' + term, {
        type: 'GET',
        dataType: 'json',
        success: function(data, textStatus, jqXHR) {
          var details, example, key, text, value, _i, _len, _ref;
          if (data.examples.length === 0) {
            humane.log('Ooops, no examples found!', {
              timeout: 2000
            });
            $('.loader-left').fadeToggle(100);
            return;
          }
          text = '<dl>';
          _ref = data.examples;
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            example = _ref[_i];
            for (key in example) {
              value = example[key];
              key = key.replace(term, "<em>" + term + "</em>");
              text += "<dt>" + key + "</dt><dd>" + value + "</dd>";
            }
          }
          text += '</dl>';
          if ($('.toolbar-right').css('display') === 'table') {
            $('.content-right').fadeOut(150, (function() {
              return $(this).html(text).fadeIn(150);
            }));
          } else {
            $('.content-right').html(text);
          }
          if (!right_slided) {
            slide('.toolbar-right');
            right_slided = !right_slided;
          }
          details = prepare_details(data.details);
          if ($('.toolbar-left').css('display') === 'table') {
            $('.content-left').fadeOut(150, (function() {
              return $(this).html(details).fadeIn(150);
            }));
          } else {
            $('.content-left').html(details);
          }
          if (!left_slided) {
            slide('.toolbar-left');
            left_slided = !left_slided;
          }
          return $('.loader-left').fadeToggle(100);
        }
      });
    });
  });

}).call(this);
