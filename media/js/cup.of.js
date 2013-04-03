// Generated by CoffeeScript 1.3.3
(function() {
  var left_slided, lock, locked, reload, right_slided, slide, slideToggle, toggle,
    __slice = [].slice;

  locked = false;

  left_slided = false;

  right_slided = false;

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
          if ($('.toolbar-right').css('display') === 'block') {
            slide('.toolbar-right');
            right_slided = !right_slided;
          }
          if ($('.toolbar-left').css('display') === 'block') {
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
    return $('.roll').click(function() {
      $.get('/lock');
      return reload();
    });
  });

  $(function() {
    return $('ruby').click(function() {
      var term;
      term = $(this).find('rb').text().trim();
      $('.loader-left').fadeToggle(250);
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
          $('.loader-left').fadeToggle(100);
          if (!right_slided) {
            slide('.toolbar-right');
            return right_slided = !right_slided;
          }
        }
      });
    });
  });

}).call(this);
