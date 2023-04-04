let autocomplete;


// document.getElementById("id_shop_name").required = false;
   // document.getElementById("id_docs").required = false;
function checkRole(answer) {

  console.log(answer)
  if (answer == "thisshop") { // hide the div that is not selected

    document.getElementById('thisshop').style.display = "block";
    // document.getElementById("id_shop_name").required = true;
    // document.getElementById("id_docs").required = true;
  } else{

    document.getElementById('thisshop').style.display = "none";

  }

}

$(document).ready(function() {
  // submit form data using AJAX
  $('#newsletter-form').on('submit', function(event) {
    event.preventDefault();

    // disable submit button
    $('#report-btn').attr('disabled', true);

    // send AJAX request
    $.ajax({
      url: '/accounts/newsletter/', // replace with actual URL path
      type: 'POST',
      data: $(this).serialize(),
      success: function(response) {
        // enable submit button
        $('#report-btn').attr('disabled', false);

        // clear email input field
        $('#daily-email-id').val('');

        // show success/error message
        Swal.fire({
          icon: response.icon,
          title: response.message,
        });
      },
      error: function(xhr, status, error) {
        // enable submit button
        $('#report-btn').attr('disabled', false);
      }
    });
  });
});
