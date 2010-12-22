<div id="toolbar">
    <div id="header">
      <h1><a href="#">${app_name}</a></h1>
    </div>
    <form name="search" action="${search_page}" method="get" class="search">
        <div class="group">
            <span class="ctrl_label">Host:</span>
            <select name="file" class="host_key_selector">
                <option value="">all</option>
                <%
                  # Dictionaries have no "order" so sort the keys
                  sorted_file_names = sorted(file_options.iterkeys(), key=str.lower)
                %>
                % for file in sorted_file_names:
                      <option value="${file}">${file}</option>
                % endfor
            </select>
            <!--  TODO: Look into enabling multiple selections -->
        </div>
        <div class="group">
            <span class="ctrl_label">Search:</span>
            <input type="text" name="regex" size="40" />
        </div>
        <div class="group">
            <span id="auto_update_label" class="ctrl_label">Update:</span>
            <input type="checkbox" name="autoupdate" value="true" />
        </div>
        <div class="group">
            <span class="ctrl_label">Limit:</span>
            <select name="limit" class="">
                <option value="25">25</option>
                <option value="50">50</option>
                <option value="100">100</option>
            </select>
        </div>
        <div class="group">
            <span class="ctrl_label">Ascending:</span>
            <input type="checkbox" name="ascending" value="true" />
        </div>
        <div class="">
        </div>
    </form>
</div>

