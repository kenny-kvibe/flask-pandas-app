'use strict';
!function() {
	const main = (e=undefined) => {
		console.log('Loaded!', e.target);
	};

	document.addEventListener('readystatechange', async e => {
		if (document.readyState != 'complete') return;
		return main(e);
	}, false);
}();