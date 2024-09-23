(function() {
    var clientside = window.dash_clientside = window.dash_clientside || {};
    var ns = clientside["_dashprivate_clientside_funcs"] = clientside["_dashprivate_clientside_funcs"] || {};

    ns["setPageTitle"] = function(data) {
        document.title = data.title;
    };
})();
