/*
* To Top
*/

window.onload = function() {

	var scrollUp = document.getElementById('scrollup');

	scrollUp.onclick = function() {
		window.scrollTo(0,0);
	};

	window.onscroll = function () {
		if ( window.pageYOffset > 0 ) {
			scrollUp.style.display = 'block';
		} else {
			scrollUp.style.display = 'none';
		}
	};
};


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
});


