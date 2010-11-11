(function (window) {
    var util = {
        'fireEvent': function (element, event) {
           if (document.createEvent) {
               var evt = document.createEvent('HTMLEvents');
               evt.initEvent(event, true, true);
               return !element.dispatchEvent(evt);
           } else {
               var evt = document.createEventObject();
               return element.fireEvent('on' + event, evt)
           }
        }
    };
    // A nicer FAQ
    (function (window) {
        var faq = document.getElementById('faq');
        if (faq) {
            // Collapse Answers
            ans = faq.getElementsByTagName('dd');
            for (var i = 0, l = ans.length; i < l; i += 1) {
                ans[i].style.display = 'none';
            }
            faq.onclick = function (e) {
                var el = (e.srcElement || e.target),
                    parent = el.parentNode;
                if (el.tagName.toLowerCase() === 'a' && parent.tagName.toLowerCase() === 'dt') {
                    e.preventDefault();
                    var ans = parent.nextElementSibling ? parent.nextElementSibling : parent.nextSibling;
                    ans.style.display = ans.style.display === 'none' ? 'block' : 'none';
                    location.hash = ['#', parent.id].join('');
                }
            };
            if (/#q[0-9]/i.test(location.hash)) {
                // Un-collapse target (like http://some.com#foo)
                var el = document.getElementById(location.hash.substring(1));
                util.fireEvent(el.firstElementChild ?
                    el.firstElementChild :
                    el.firstChild, 'click');
            }
        } else {
            return;
        }
    }(window));
}(window));
