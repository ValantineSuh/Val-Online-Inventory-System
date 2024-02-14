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