# Templeton foundation

In Google Chrome, go to <https://templeton.org/grants/grant-database>.

```javascript
var otable = jQuery('#grants-table').dataTable();
console.log(JSON.stringify(otable.fnGetData()));
```

Then right click and "save as" `data.json`. You want to clean up the typed text
and prompt and stuff so it's just the JSON.
