<!DOCTYPE html>
<html>
  <head>
    <title>Event Sourcing Test</title>
    <meta charset="utf-8" />
  </head>
  <body>
    <div>
      <h1>Person {{ p.name.firstname }} {{ p.name.lastname }}</h1>
      <div>Address:</div>
      <div>{{ p.address.street }}, {{ p.address.city }}</div>
      <div>Status:</div>
      <div>{{ p.status_label }}</div>
      <div>Version: {{ p.version }}</div>
    </div>
    <div>
      <h1>Change address</h1>
      <form method="post" action="/{{ person_id }}/change_address">
        <div>
          <div>New street:</div>
          <div><input type="text" name="new_street" /></div>
        </div>
        <div>
          <div>New city:</div>
          <div><input type="text" name="new_city" /></div>
        </div>
        <div>
          <input type="submit" value="Submit" />
        </div>
      </form>
    </div>
    <div>
      <h1>Change marital status</h1>
      <form method="post" action="/{{ person_id }}/change_status">
        <div>
          <div>
            New status:
          </div>
          <div>
            <select name="new_status">
              % for item in statuses:
              <option value="{{ item[0] }}">{{ item[1] }}</option>
              % end
            </select>
          </div>
      </div>
        <div>
          <input type="submit" value="Submit" />
        </div>
      </form>
    </div>
  </body>
</html>

