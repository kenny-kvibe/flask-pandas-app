'use strict';
!function() {
	function initAlerts() {
		var alertList = Array.from(document.querySelectorAll('.alert'));
		var alerts =  alertList.map(function (element) {
			return new bootstrap.Alert(element);
		});
	}

	function initPopovers() {
		const popoverTriggerList = Array.from(document.querySelectorAll('[data-bs-toggle="popover"]'));
		const popoverList = popoverTriggerList.map(popoverTriggerEl => {
			return new bootstrap.Popover(popoverTriggerEl);
		});
	}

	document.addEventListener('readystatechange', async e => {
		if (document.readyState != 'complete') return;
		initAlerts();
		initPopovers();
	}, false);
}();