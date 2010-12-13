function(head, req) {
  var ddoc = this;
  var Mustache = require("lib/mustache");
  var List = require("vendor/couchapp/lib/list");
  var path = require("vendor/couchapp/lib/path").init(req);

  var indexPath = path.list('index','recent-items',{descending:true, limit:15});
  var errorsSearchPath = path.list('index','errors',{descending:true, limit:15});
  var warningsSearchPath = path.list('index','warnings',{descending:true, limit:15});
  var onlyKeyPath = path.list('index',{descending:true, limit:15, key:'SOMEKEY'});
  var accumLogVolPath = path.view('log-volume');


  var today = new Date();
  var curr_year = today.getFullYear();
  var curr_month = today.getMonth();
  var curr_date = today.getDate();

  var last_year = curr_year - 1;
  var next_month = curr_month + 1;

  var default_start_key = String(last_year) + String(curr_month) + String(curr_date);
  var default_end_key = String(curr_year) + String(next_month) + String(curr_date);

  var path_parts = req.path;
  // The provides function serves the format the client requests.
  // The first matching format is sent, so reordering functions changes
  // thier priority. In this case HTML is the preferred format, so it comes first.
  provides("html", function() {
    var key = "";
    // render the html head using a template
    var stash = {
      header : {
        index : indexPath,
        blogName : "Funky Log Seer",
        errors_search : errorsSearchPath,
        warnings_search: warningsSearchPath,
        default_start_date: default_start_key,
        default_end_date: default_end_key
      },
      javascript : {
        accumLogVolumePath : accumLogVolPath 
      },
      scripts : {},
      db : req.path[0],
      design : req.path[2],
      assets : path.asset(),
      onlykey : onlyKeyPath, 
      entries : List.withRows(function(row) {
        var entry = row.value;
        key = row.key;
        return {
          content : entry.Content,
          host : entry.Host,
          file : entry.File
        };
      }),
      older : function() {
        return path.older(key);
      },
      "15" : path.limit(15),
      "30" : path.limit(30),
      "60" : path.limit(60)
    };
    return Mustache.to_html(ddoc.templates.index, stash, ddoc.templates.partials, List.send);
  });
};
