
//  From https://stackoverflow.com/questions/20606225/how-to-disable-chrome-from-opening-up-new-window-and-tabs/42599815#42599815
//  It's bad if chrome opens 1000 pages when exploring, we like to keep one page.

/* Define helper functions */
var processAnchor = function(a) {
    //if (a.hasAttribute('target')) {
    //    a.removeAttribute('target');
    //}
    a.setAttribute('target', '_self');
};

/* Define the observer for watching over inserted elements */
var insertedObserver = new MutationObserver(function(mutations) {
    mutations.forEach(function(m) {
        var inserted = [].slice.call(m.addedNodes);
        while (inserted.length > 0) {
            var elem = inserted.shift();
            [].slice.call(elem.children || []).forEach(function(el) {
                inserted.push(el);
            });
            if (elem.nodeName === 'A') {
                processAnchor(elem);
            }
        }
    });
});

/* Define the observer for watching over
 * modified attributes of anchor elements */
var modifiedObserver = new MutationObserver(function(mutations) {
    mutations.forEach(function(m) {
        if ((m.type === 'attributes') && (m.target.nodeName === 'A')) {
            processAnchor(m.target);
        }
    });
});

/* Start observing */
insertedObserver.observe(document.documentElement, {
    childList: true,
    subtree: true
});
modifiedObserver.observe(document.documentElement, {
    attributes: true,
    substree: true
});