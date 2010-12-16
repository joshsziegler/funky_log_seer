function(head, req) {
  var ddoc = this;
  var Mustache = require("lib/mustache");
  var List = require("vendor/couchapp/lib/list");
  var path = require("vendor/couchapp/lib/path").init(req);

  var today = new Date();
  var curr_year = today.getFullYear();
  var curr_month = today.getMonth() + 1; /* January == 0 */
  var curr_date = today.getDate();
  var default_day = String(curr_year) + String(curr_month) + String(curr_date);
  var keys = JSON.stringify([{"date":default_day }]);

  var view_all = path.list('index','all',{descending:true, limit:25, autoupdate:true});
  var view_errors = path.list('index','errors',{descending:true, limit:25, autoupdate:true});
  var view_warnings = path.list('index','warnings',{descending:true, limit:25, autoupdate:true});

  var volume_by_day = path.view('volume-by-day');
  var volume_by_hour = path.view('volume-by-hour');

  var path_parts = req.path;
  // The provides function serves the format the client requests.
  // The first matching format is sent, so reordering functions changes
  // thier priority. In this case HTML is the preferred format, so it comes first.
  provides("html", function() {
    var key = "";
    // render the html head using a template
    var stash = {
      header : {
        app_name : "Funky Log Seer",
        view_all : view_all,
        view_errors : view_errors,
        view_warnings : view_warnings,
        default_day : default_day
      },
      javascript : {
        volume_by_day : volume_by_day,
        volume_by_hour : volume_by_hour

      },
      scripts : {},
      db : req.path[0],
      design : req.path[2],
      assets : path.asset(),
      entries : List.withRows(function(row) {
        var entry = row.value;
        key = row.key;
        return {
          content : entry.Content,
          host : entry.Host,
          file : entry.File
        };
      })
    };
    return Mustache.to_html(ddoc.templates.index, stash, ddoc.templates.partials, List.send);
  });
};
