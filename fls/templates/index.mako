<!DOCTYPE html>
<html>
  <head>
    <title>${page_title}</title>
    <link rel="stylesheet" href="main.css" type="text/css"/> 
  </head>
  <body>
      <%include file="/header.mako"/>
      <ul>
      % for line in log_results:
          <li>${line[0]} - ${line[1]}</li>
      % endfor
      </ul>
  </body>
</html>

