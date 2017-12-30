# Templeton foundation

## Steps to get the data

In Google Chrome, go to <https://templeton.org/grants/grant-database>.

Now open the developer tools with Ctrl-Shift-I, and enter the following two
lines in the console:

```javascript
var otable = jQuery('#grants-table').dataTable();
console.log(JSON.stringify(otable.fnGetData()));
```

This will print a JSON dump of all the grants data. This will work as long as
Templeton keeps using [DataTables](https://datatables.net/) to render the data.

Then right click and "save as" `data.json`. You want to clean up the typed text
and prompt and stuff so it's just the JSON.
