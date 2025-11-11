// Keep track of the current table so we can destroy it
var currentDataTable;

// Define the "blueprints" for your tables
const tableConfig = {
    screenerA: {
        file: "data/screener_A.json",
        columns: [
            { "title": "Ticker", "data": "ticker" },
            { "title": "Change %", "data": "change_pct" },
            { "title": "Volume", "data": "volume" }
        ]
    },
    screenerB: {
        file: "data/screener_B.json",
        columns: [
            { "title": "Ticker", "data": "ticker" },
            { "title": "RSI", "data": "rsi" },
            { "title": "Signal", "data": "signal" }
        ]
    },
    screenerMomentum: {
        file: "data/screener_momentum.json",
        columns: [
            { "title": "Ticker", "data": "ticker" },
            { "title": "Price", "data": "price" },
            { "title": "52W High", "data": "high_52w" },
            { "title": "Dist to High %", "data": "dist_to_high_pct" },
            { "title": "Vol Ratio", "data": "volume_ratio" },
            { "title": "RS Score", "data": "rs_score" }
        ]
    }
    // Add new configs here for screener_C, screener_D, etc.
};

// The Reusable Function
function loadScreenerData(config) {
    // If a table already exists, destroy it completely
    if (currentDataTable) {
        currentDataTable.destroy();
        currentDataTable = null;
    }
    
    // Clear both header and body
    $('#tableHeader').empty();
    $('#stockTable tbody').empty();

    // Build the new table headers dynamically
    var headerRow = $('<tr></tr>');
    config.columns.forEach(function(col) {
        headerRow.append('<th>' + col.title + '</th>');
    });
    $('#tableHeader').html(headerRow);

    // Initialize the new DataTable
    currentDataTable = $('#stockTable').DataTable({
        "ajax": {
            "url": config.file,
            "dataSrc": "data"  // Tell DataTables the array is in the "data" property
        },
        "columns": config.columns,
        "paging": false,        // Disable pagination - show all rows
        "searching": true,      // Keep search functionality
        "ordering": true,       // Keep sorting functionality
        "destroy": true,        // Ensures it can be re-initialized
        "responsive": true,
        "scrollY": "500px",     // Enable vertical scrolling with 500px height
        "scrollCollapse": true  // Collapse if fewer rows than scroll height
    });
}

// The Button Click Handlers
$(document).ready(function() {
    $('#loadScreenerA').on('click', function() {
        loadScreenerData(tableConfig.screenerA);
    });

    $('#loadScreenerB').on('click', function() {
        loadScreenerData(tableConfig.screenerB);
    });

    $('#loadScreenerMomentum').on('click', function() {
        loadScreenerData(tableConfig.screenerMomentum);
    });
    
    // Add more button handlers here as you add screeners
    // $('#loadScreenerC').on('click', function() {
    //     loadScreenerData(tableConfig.screenerC);
    // });
});
