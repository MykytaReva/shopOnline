let autocomplete;




function checkRole(role) {
  if (role == 'thisshop') {
    document.getElementById('thisshop').style.display = 'block';
    document.getElementById('id_shop_name').required = true;
    document.getElementById('id_docs').required = true;
  } else {
    document.getElementById('thisshop').style.display = 'none';
    document.getElementById('id_shop_name').required = false;
    document.getElementById('id_docs').required = false;
  }
}

// function checkRole(answer) {


//   if (answer == "thisuser") { // hide the div that is not selected

//     document.getElementById('thisshop').style.display = "block";
//     document.getElementById("id_shop_name").required = false;
//     document.getElementById("id_docs").required = false;

//   } else{

//     document.getElementById('thisshop').style.display = "none";

//   }

// }

$(document).ready(function() {
  // submit form data using AJAX
  $('#newsletter-form').on('submit', function(event) {
    event.preventDefault();

    // disable submit button
    $('#report-btn').attr('disabled', true);

    // send AJAX request
    $.ajax({
      url: '/accounts/newsletter/',
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


$(document).ready(function() {
  $('.model-button').on('click', function(e) {
    e.preventDefault();
    var form = $(this).closest('form');
    $('#deleteModal').modal('show');
    $('#deleteModal').find('.modal-footer #confirm-delete').on('click', function() {
      form.submit();
    });

  });
  $('.close-but').on('click', function (e) {
    e.preventDefault();
    var myModal = new bootstrap.Modal(document.getElementById('myModal'), {
      keyboard: false
  })
    e.preventDefault();
    myModal.hide();
  });
});

