(function (window) {
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
                    var ans = parent.nextElementSibling;
                    ans.style.display = ans.style.display === 'none' ? 'block' : 'none';
                    location.hash = ['#', parent.id].join('');
                }
            };
        } else {
            return;
        }
    }(window));
}(window));
