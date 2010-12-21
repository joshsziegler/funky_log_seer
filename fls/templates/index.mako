<!DOCTYPE html>
<html>
  <head>
    <title>${page_title}</title>
    <link rel="stylesheet" href="css/main.css" type="text/css" /> 
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
    <script type="text/javascript" src="js/get_url_arg.js"></script>
    <script type="text/javascript" src="js/get_form_vals.js"></script>
  </head>
  <body>
      <%include file="/js_on_page_load.mako"/>
      <%include file="/header.mako"/>
      <ul>
      % for line in log_results:
          <li>${line[0]} - ${line[1]}</li>
      % endfor
      </ul>
  </body>
</html>

