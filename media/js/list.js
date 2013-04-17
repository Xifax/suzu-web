$(document).ready(function() {

    var Item = Backbone.Model.extend({});

    var Items = Backbone.PageableCollection.extend({
        model: Item,
        url: "list_all",
        state: {
            pageSize: 20
        },
        mode: "client",
    });

    var items = new Items();

    var columns = [{
        name: "id",
        label: "#",
        editable: false,
        cell: Backgrid.IntegerCell.extend({
            orderSeparator: ''
    })
    }, {
        name: "value",
        label: "Value",
        cell: "string",
        editable: false,
        width: "fixed",
    }, {
        name: "pos",
        label: "Part of speech",
        cell: "string",
        editable: false,
    }, {
        name: "added",
        label: "Added",
        cell: "string",
        editable: false,
    }, {
        name: "status",
        label: "Status",
        cell: "string",
        editable: false,
    }, {
        name: "category",
        label: "Category",
        cell: "string",
        editable: false,
    }, {
        name: "lang",
        label: "Language",
        cell: "string",
        editable: false
    }];

    // Initialize a new Grid instance
    var grid = new Backgrid.Grid({
        columns: columns,
        collection: items,
        footer: Backgrid.Extension.Paginator,
    });

    // Render the grid and attach the root to HTML
    $("#items").append(grid.render().$el);

    // Fetch items from url
    items.fetch();

});


