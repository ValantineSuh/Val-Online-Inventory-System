$(document).ready(function() {
    $('#search-button').click(function() {
      var query = $('#query').val();
      $.ajax({
        url: '/search',
        type: 'GET',
        data: { query: query },
        success: function(response) {
          var results = response;
          var resultsHtml = '';
          for (var i = 0; i < results.length; i++) {
            resultsHtml += '<p>' + results[i] + '</p>';
          }
          $('#search-results').html(resultsHtml);
        },
        error: function(error) {
          console.log('Search request failed:', error);
        }
      });
    });
  });
// javascript code

// function updateLocationCount() {
//     $.ajax({
//         url: '/employee/count',
//         type: 'GET',
//         success: function(data) {
//             $('#employee-count').text(data.count);
//         }
//     });
// }

// // Call the updateLocationCount function every 5 seconds
// setInterval(updateLocationCount, 1000);

