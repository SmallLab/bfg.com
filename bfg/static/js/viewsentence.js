/*
 * Owl Carousel
 */
$(document).ready(function() {
	var plugins = {
		owl: $(".owl-carousel")
	};

	if (plugins.owl.length) {
		var i;
		for (i = 0; i < plugins.owl.length; i++) {
			var c = $(plugins.owl[i]), responsive = {};
			var aliaces = ["-", "-xs-", "-sm-", "-md-", "-lg-", "-xl-"], values = [0, 480, 768, 992, 1200, 1800], j, k;
			for (j = 0; j < values.length; j++) {
				responsive[values[j]] = {};
				for (k = j; k >= -1; k--) {
					if (!responsive[values[j]]["items"] && c.attr("data" + aliaces[k] + "items")) {
						responsive[values[j]]["items"] = k < 0 ? 1 : parseInt(c.attr("data" + aliaces[k] + "items"));
					}
					if (!responsive[values[j]]["stagePadding"] && responsive[values[j]]["stagePadding"] !== 0 && c.attr("data" + aliaces[k] + "stage-padding")) {
						responsive[values[j]]["stagePadding"] = k < 0 ? 0 : parseInt(c.attr("data" + aliaces[k] + "stage-padding"));
					}
					if (!responsive[values[j]]["margin"] && responsive[values[j]]["margin"] !== 0 && c.attr("data" + aliaces[k] + "margin")) {
						responsive[values[j]]["margin"] = k < 0 ? 30 : parseInt(c.attr("data" + aliaces[k] + "margin"));
					}
				}
			}
			c.owlCarousel({
				autoplay: c.attr("data-autoplay") === "true",
				loop: c.attr("data-loop") !== "false",
				items: 1,
				dotsContainer: c.attr("data-pagination-class") || false,
				navContainer: c.attr("data-navigation-class") || false,
				mouseDrag: c.attr("data-mouse-drag") !== "false",
				nav: c.attr("data-nav") === "true",
				dots: c.attr("data-dots") === "true",
				dotsEach: c.attr("data-dots-each") ? parseInt(c.attr("data-dots-each")) : false,
				animateIn: c.attr('data-animation-in') ? c.attr('data-animation-in') : 'slide',
				animateOut: c.attr('data-animation-out') ? c.attr('data-animation-out') : false,
				responsive: responsive,
				navText: []
			});
		}
	}

	$('[data-toggle="tooltip"]').tooltip()
});

/**
 * Show phone number
 */
$('#phone_views').click(function (e) {
          $.get(
              "/sentence/showphone/",
              {
                  id_sentence: data_sentence.id_sentence,
              },
              onAjaxSuccess
            );
            function onAjaxSuccess(data)
            {
                if (data.status){
                  $('#phone_show').text(data.phone);
                  $('#phone_views').text('');
                }
            }
            e.preventDefault();
  });

/*
* Show map
* */
$('#map_google').click(function (e) {
    var map;
    var geocoder;
    //Resize Google map
    $(function() {
        var $modal = $('#myModalMap'), $map = $('#map_div');
        $modal.on('shown.bs.modal', function () {
            google.maps.event.trigger($map[0], 'resize');
        });
    });

    function geocodeAddress(geocoder, resultsMap) {
        var address = data_sentence.adress;
        geocoder.geocode({'address': address}, function(results, status) {
            if (status === 'OK') {
                resultsMap.setCenter(results[0].geometry.location);
                var marker = new google.maps.Marker({
                    map: resultsMap,
                    position: results[0].geometry.location
                });
            } else {
                alert('Возможно не верный адрес!');
            }
        });
    };

    function initMap() {
        geocoder = new google.maps.Geocoder();
        var uluru = {lat: -34.397, lng: 150.644};
        map = new google.maps.Map(document.getElementById('map_div'), {
                        zoom: 18,
                        center: uluru
                    });
        geocodeAddress(geocoder, map);
        $('#myModalMap').modal('show');
      };
    initMap();
    e.preventDefault();
});

$(document).on('click', '[data-toggle="lightbox"]', function(event) {
                event.preventDefault();
                $(this).ekkoLightbox({alwaysShowClose: true});
            });