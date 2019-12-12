$(document).ready(function() {

  var email

  $("#register").click(function(e) {
    console.log("register button clicked");
    email = document.getElementById("email").value;
    var password = document.getElementById("password").value;

		var ename = email.split("@")[0];

    console.log(email);
    console.log(password);

		var ename = {"ename": ename};
		console.log(ename);

		$.ajax({
    type: "POST",
    contentType: "application/json; charset=utf-8",
    url: "/partyinput",
    data: JSON.stringify({
      ename
    }),
    success: [],
    dataType: "json"
  }).done(function() {
		console.log("register done") // for some reason this .done part isn't working atm
    window.location.replace("/partyinput"); // on done, redirect page to /partyinput
  });

		window.location.replace("/partyinput"); // force changing page to /partyinput

    e.preventDefault();
  });


	// on id="group_me" button click, do this function
  $("#group_me").click(function(e) {
    console.log("group me button clicked");
		// grabbing values from form id's (id="startloc", etc)
		var firstname = document.getElementById("firstname").value;
		var lastname = document.getElementById("lastname").value;
		var start = document.getElementById("start").value;
		var end = document.getElementById("end").value;
    // var startloc = document.getElementById("startloc").value;
    var endloc = document.getElementById("endloc").value;
		var latitude = endloc.split(",")[0].slice(1, -1)
		var longitude = endloc.split(",")[1].slice(1, -1)
    var hour = document.getElementById("hour").value;
    var minute = document.getElementById("minute").value;
    var am_pm = document.getElementById("am_pm").value;
		var time = hour + ":" + minute + am_pm

		// console.log("start:", start);
		// console.log("end:", end);

    if (end == "") {
      alert('Please enter a destination location.');
    } else {
			var data = {
				"firstname": firstname,
				"lastname": lastname,
				"start": start,
				"end": end.toUpperCase(),
				// "startloc": startloc,
				"latitude": parseFloat(latitude),
				"longitude": parseFloat(longitude),
				"endloc": endloc,
				"hour": parseFloat(hour),
				"minute": parseFloat(minute),
				"am_pm": am_pm,
				"time": time
			};

	    console.log(data);

			// open groups.json file and save a new row

			// fs is a module of nodejs to interact with file system
			// we specify the file name and the stringified JSON object
			// as well as a callback to handle a possible error
			// fs.writeFile('groups.json', JSON.stringify(data), (err) => {
			//   if (err) throw err
			//   console.log('The file has been saved!')
			// })

			// post request to flask /partyinput url, sending data variable above
			$.ajax({
	    type: "POST",
	    contentType: "application/json; charset=utf-8",
	    url: "/grouping",
	    data: JSON.stringify({
	      data
	    }),
	    // success: window.location.replace("/partyinfo"),
      success: alert("Please wait for your walking party to be found."),
	    dataType: "json"
	  }).done(function() {
      alert("Please wait for your walking party to be found.")
	    // window.location.replace("/partyinfo"); // on done, redirect page to homepage (index) // not sure why this not working atm
	  });
		}

		// window.location.replace("/pickaparty"); // force changing page to /pickaparty

    e.preventDefault();
  });


  // var logged_str = "You are logged in as " + email
  // document.getElementById("logged_in_as").innerHTML = logged_str

});

function group_table(data) {
  var table = document.getElementById("table");

	console.log("inside group_table function!");

  for (let i of Object.keys(data)) {
		console.log("data i:", i)
    var row = table.insertRow(-1); // inserts to bottom

    var num = row.insertCell(0);
    var leaving_time = row.insertCell(1);
    var starting_point = row.insertCell(2);
    var destination_area = row.insertCell(3);
    var choose_button = row.insertCell(4);

    // row.id = ;
    num.setAttribute("class", "num");
    leaving_time.setAttribute("class", "leaving_time");
		starting_point.setAttribute("class", "starting_point");
		destination_area.setAttribute("class", "destination_area");
		choose_button.setAttribute("class", "choose_button");

    // num.innerHTML = '<b>' + "NUMBER CODE HERE" + '</b>';
    leaving_time.innerHTML = data[i]["time"]; // replace this with group time after running kNN code
    starting_point.innerHTML = data[i]["start"] // replace this with group start loc after running kNN code
    destination_area.innerHTML = data[i]["end"]; // replace this with group end loc after running kNN code
    choose_button.innerHTML = '<input id="submit" type="button" value="Select" class="search-submit btn btn-primary">'
  };
};


/////// template js //////


(function($) {

  'use strict';

  // bootstrap dropdown hover

  // loader
  var loader = function() {
    setTimeout(function() {
      if ($('#loader').length > 0) {
        $('#loader').removeClass('show');
      }
    }, 1);
  };
  loader();

  // Stellar
  // $(window).stellar({
  //   responsive: false,
  //   parallaxBackgrounds: true,
  //   parallaxElements: true,
  //   horizontalScrolling: false,
  //   hideDistantElements: false,
  //   scrollProperty: 'scroll'
  // });


  $('nav .dropdown').hover(function() {
    var $this = $(this);
    $this.addClass('show');
    $this.find('> a').attr('aria-expanded', true);
    $this.find('.dropdown-menu').addClass('show');
  }, function() {
    var $this = $(this);
    $this.removeClass('show');
    $this.find('> a').attr('aria-expanded', false);
    $this.find('.dropdown-menu').removeClass('show');
  });


  $('#dropdown04').on('show.bs.dropdown', function() {
    console.log('show');
  });



  // home slider
  // $('.home-slider').owlCarousel({
  //   loop: true,
  //   autoplay: true,
  //   margin: 10,
  //   animateOut: 'fadeOut',
  //   animateIn: 'fadeIn',
  //   nav: true,
  //   autoplayHoverPause: true,
  //   items: 1,
  //   navText: ["<span class='ion-chevron-left'></span>", "<span class='ion-chevron-right'></span>"],
  //   responsive: {
  //     0: {
  //       items: 1,
  //       nav: false
  //     },
  //     600: {
  //       items: 1,
  //       nav: false
  //     },
  //     1000: {
  //       items: 1,
  //       nav: true
  //     }
  //   }
  // });

  // owl carousel
  // var majorCarousel = $('.js-carousel-1');
  // majorCarousel.owlCarousel({
  //   loop: true,
  //   autoplay: false,
  //   stagePadding: 0,
  //   margin: 10,
  //   animateOut: 'fadeOut',
  //   animateIn: 'fadeIn',
  //   nav: false,
  //   dots: false,
  //   autoplayHoverPause: false,
  //   items: 3,
  //   responsive: {
  //     0: {
  //       items: 1,
  //       nav: false
  //     },
  //     600: {
  //       items: 2,
  //       nav: false
  //     },
  //     1000: {
  //       items: 3,
  //       nav: true,
  //       loop: false
  //     }
  //   }
  // });

  // cusotm owl navigation events
  // $('.custom-next').click(function(event) {
  //   event.preventDefault();
  //   // majorCarousel.trigger('owl.next');
  //   majorCarousel.trigger('next.owl.carousel');
	//
  // })
  // $('.custom-prev').click(function(event) {
  //   event.preventDefault();
  //   // majorCarousel.trigger('owl.prev');
  //   majorCarousel.trigger('prev.owl.carousel');
  // })

  // owl carousel
  // var major2Carousel = $('.js-carousel-2');
  // major2Carousel.owlCarousel({
  //   loop: true,
  //   autoplay: true,
  //   stagePadding: 7,
  //   margin: 20,
  //   animateOut: 'fadeOut',
  //   animateIn: 'fadeIn',
  //   nav: false,
  //   autoplayHoverPause: true,
  //   items: 4,
  //   navText: ["<span class='ion-chevron-left'></span>", "<span class='ion-chevron-right'></span>"],
  //   responsive: {
  //     0: {
  //       items: 1,
  //       nav: false
  //     },
  //     600: {
  //       items: 3,
  //       nav: false
  //     },
  //     1000: {
  //       items: 4,
  //       nav: true,
  //       loop: false
  //     }
  //   }
  // });




  var contentWayPoint = function() {
    var i = 0;
    $('.element-animate').waypoint(function(direction) {

      if (direction === 'down' && !$(this.element).hasClass('element-animated')) {

        i++;

        $(this.element).addClass('item-animate');
        setTimeout(function() {

          $('body .element-animate.item-animate').each(function(k) {
            var el = $(this);
            setTimeout(function() {
              var effect = el.data('animate-effect');
              if (effect === 'fadeIn') {
                el.addClass('fadeIn element-animated');
              } else if (effect === 'fadeInLeft') {
                el.addClass('fadeInLeft element-animated');
              } else if (effect === 'fadeInRight') {
                el.addClass('fadeInRight element-animated');
              } else {
                el.addClass('fadeInUp element-animated');
              }
              el.removeClass('item-animate');
            }, k * 100);
          });

        }, 100);

      }

    }, {
      offset: '95%'
    });
  };
  contentWayPoint();


  $('.nonloop-block-11').owlCarousel({
    center: false,
    items: 1,
    loop: false,
    stagePadding: 10,
    margin: 0,
    nav: true,
    navText: ['<span class="ion-android-arrow-back">', '<span class="ion-android-arrow-forward">'],
    responsive: {
      600: {
        margin: 20,
        stagePadding: 10,
        items: 2
      },
      800: {
        margin: 20,
        stagePadding: 10,
        items: 2
      },
      1000: {
        margin: 20,
        stagePadding: 10,
        items: 3
      },
      1900: {
        margin: 20,
        stagePadding: 200,
        items: 4
      }
    }
  });


  // var counter = function() {
	//
  //   $('#section-counter').waypoint(function(direction) {
	//
  //     if (direction === 'down' && !$(this.element).hasClass('element-animated')) {
	//
  //       var comma_separator_number_step = $.animateNumber.numberStepFactories.separator(',')
  //       $('.number').each(function() {
  //         var $this = $(this),
  //           num = $this.data('number');
  //         console.log(num);
  //         $this.animateNumber({
  //           number: num,
  //           numberStep: comma_separator_number_step
  //         }, 7000);
  //       });
	//
  //     }
	//
  //   }, {
  //     offset: '95%'
  //   });
	//
  // }
  // counter();

  // $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
  //   disableOn: 700,
  //   type: 'iframe',
  //   mainClass: 'mfp-fade',
  //   removalDelay: 160,
  //   preloader: false,
	//
  //   fixedContentPos: false
  // });



})(jQuery);
