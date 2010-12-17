function(head, req) {
  var ddoc = this;
  var Mustache = require("lib/mustache");
  var List = require("vendor/couchapp/lib/list");
  var path = require("vendor/couchapp/lib/path").init(req);

  var path_parts = req.path;
  // The provides function serves the format the client requests.
  // The first matching format is sent, so reordering functions changes
  // thier priority. In this case HTML is the preferred format, so it comes first.
  provides("html", function() {
    var key = "";
    // render the html head using a template
    var stash = {
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
    return Mustache.to_html(ddoc.templates.results, stash, ddoc.templates.partials, List.send);
  });
};
