$(document).ready(function() {
    $('#flexSwitchCheckDefault').change(function() {
      var itemId = $(this).data('id');
      var isAvailable = $(this).prop('checked');
      console.log('work');
      $.ajax({
        url: '/docter/update_is_available',
        method: 'POST',
        data: {
          'item_id': itemId,
          'is_available': isAvailable,
        },
        success: function(response) {
          // Update the toggle switch based on the current availability status
          if (response.is_available) {
            $('#flexSwitchCheckDefault').prop('checked', true);
          } else {
            $('#flexSwitchCheckDefault').prop('checked', false);
          }
        },
        error: function(xhr) {
          console.log(xhr.statusText + ': ' + xhr.responseText);
        }
      });
    });
  });  