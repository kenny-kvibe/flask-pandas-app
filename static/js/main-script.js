'use strict';
!function() {
	function initAlerts() {
		var alertList = Array.from(document.querySelectorAll('.alert'));
		var alerts =  alertList.map(function (element) {
			return new window.bootstrap.Alert(element);
		});
	}

	function initPopovers() {
		const popoverTriggerList = Array.from(document.querySelectorAll('[data-bs-toggle="popover"]'));
		const popoverList = popoverTriggerList.map(popoverTriggerEl => {
			return new window.bootstrap.Popover(popoverTriggerEl);
		});
	}

	function initTheme() {
		const body = document.querySelector('#body');
		const themeBtn = document.querySelector('#theme-button');

		function toggleTheme() {
			if (window.sessionStorage.getItem('theme-name') == 'dark') {
				body.classList.remove('dark-theme');
				window.sessionStorage.setItem('theme-name', 'light');
			} else if (window.sessionStorage.getItem('theme-name') == 'light') {
				body.classList.add('dark-theme');
				window.sessionStorage.setItem('theme-name', 'dark');
			}
		}

		themeBtn.addEventListener('click', toggleTheme, false);
		if (window.sessionStorage.getItem('theme-name') == null) {
			window.sessionStorage.setItem('theme-name', 'light');
		}
		if (window.sessionStorage.getItem('theme-name') == 'dark') {
			body.classList.add('dark-theme');
		} else if (window.sessionStorage.getItem('theme-name') == 'light') {
			body.classList.remove('dark-theme');
		}
	}

	document.addEventListener('readystatechange', async e => {
		if (document.readyState != 'complete') return;
		if (window.bootstrap != null) {
			initAlerts();
			initPopovers();
		}
		initTheme();
	}, false);
}();