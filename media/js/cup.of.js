// Generated by CoffeeScript 1.3.3
(function() {
  var lock, locked, reload, slide, slideToggle, slided, toggle,
    __slice = [].slice;

  locked = false;

  slided = false;

  reload = function() {
    return location.reload();
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
      _results.push($(div).slideToggle(150));
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
    var div, divs, _i, _len, _results;
    divs = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
    _results = [];
    for (_i = 0, _len = divs.length; _i < _len; _i++) {
      div = divs[_i];
      _results.push($(div).animate({
        width: 'toggle'
      }, 150));
    }
    return _results;
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

  $(function() {
    return $.ajax('/toggled', {
      type: 'GET',
      dataType: 'json',
      success: function(data, textStatus, jqXHR) {
        locked = data.status;
        if (locked) {
          toggle('.toolbar-top', '.toolbar-bottom');
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
          if ($('.toolbar-right').css('display') === 'block') {
            slide('.toolbar-right');
            return slided = !slided;
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
    return $('.roll').click(function() {
      $.get('/lock');
      return reload();
    });
  });

  $(function() {
    return $('ruby').hover(function() {
      $('.rads').fadeToggle(100);
      return $('#' + this.id + '.definition').fadeToggle(100);
    });
  });

  $(function() {
    return $('ruby').click(function() {
      var term;
      term = $(this).find('rb').text().trim();
      $('.loader').fadeToggle(250);
      return $.ajax('/examples/' + term, {
        type: 'GET',
        dataType: 'json',
        success: function(data, textStatus, jqXHR) {
          var example, key, text, value, _i, _len, _ref;
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
          $('.toolbar-right').html(text);
          $('.loader').fadeToggle(100);
          if (!slided) {
            slide('.toolbar-right');
            return slided = !slided;
          }
        }
      });
    });
  });

}).call(this);
