'use strict';

document.addEventListener('DOMContentLoaded', function() {
    if (localStorage.getItem('cookiesAccepted') === 'true') {
        gtag('js', new Date());
        gtag('config', GA_TRACKING_ID, {
            'anonymize_ip': true
        });
        gtag('consent', 'update', {
            'analytics_storage': 'granted'
        });
    } else {
        gtag('consent', 'default', {
            'analytics_storage': 'denied'
        });
    }
});
