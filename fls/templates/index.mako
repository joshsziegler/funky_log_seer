<!DOCTYPE html>
<html>
  <head>
    <title>${page_title}</title>
    <link rel="stylesheet" href="css/main.css" type="text/css" /> 
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.7/jquery-ui.min.js"></script>
    <script type="text/javascript" src="js/get_url_arg.js"></script>
    <script type="text/javascript" src="js/get_form_vals.js"></script>
    <script type="text/javascript" src="js/update_page.js"></script>
  </head>
  <body>
      <%include file="/js_on_page_load.mako"/>
      <%include file="/header.mako"/>
      <div id="results">
          <ul class="entries">
              % for line in log_results:
                  <li><a href="#" class="">${line[0]}</a>
                  <a href="#" class="host_key_change">${line[1]}</a> : ${line[2]}</li>
              % endfor
          </ul>
      </div>
  </body>
</html>

