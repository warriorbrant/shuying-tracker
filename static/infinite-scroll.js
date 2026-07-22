document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('[data-infinite-scroll]').forEach(function (sentinel) {
    var list = document.getElementById(sentinel.dataset.listId);
    var loadingEl = sentinel.dataset.loadingId ? document.getElementById(sentinel.dataset.loadingId) : null;
    var url = sentinel.dataset.url;
    if (!list || !url) return;

    var extraParams = {};
    if (sentinel.dataset.params) {
      try {
        extraParams = JSON.parse(sentinel.dataset.params);
      } catch (e) {
        extraParams = {};
      }
    }

    var loading = false;

    var observer = new IntersectionObserver(function (entries) {
      if (!entries[0].isIntersecting || loading) return;
      loading = true;
      if (loadingEl) loadingEl.style.visibility = 'visible';

      var params = new URLSearchParams(extraParams);
      params.set('offset', sentinel.dataset.offset);

      fetch(url + '?' + params.toString())
        .then(function (r) { return r.json(); })
        .then(function (data) {
          list.insertAdjacentHTML('beforeend', data.html);
          sentinel.dataset.offset = parseInt(sentinel.dataset.offset, 10) + data.count;
          loading = false;
          if (loadingEl) loadingEl.style.visibility = 'hidden';
          if (!data.has_more) {
            observer.disconnect();
            sentinel.remove();
            if (loadingEl) loadingEl.remove();
          }
        })
        .catch(function () {
          loading = false;
          if (loadingEl) loadingEl.style.visibility = 'hidden';
        });
    }, { rootMargin: '300px' });

    observer.observe(sentinel);
  });
});
