let autocomplete;

function initAutoComplete(){
  autocomplete = new google.maps.places.Autocomplete(
      document.getElementById('id_address'),
      {
          types: ['geocode', 'establishment'],
          //default in this app is "IN" - add your country code
          componentRestrictions: {country: ['ua', 'pl', 'de', 'uk', 'cz']}
        })
  // function to specify what should happen when the prediction is clicked
  autocomplete.addListener('place_changed', onPlaceChanged);
  }



  function onPlaceChanged (){
      var place = autocomplete.getPlace();

      // User did not select the prediction. Reset the input field or alert()
      if (!place.geometry){
          document.getElementById('id_address').placeholder = "Start typing...";
      }
      else{
          console.log('place name=>', place.name)
      }

      // get the address components and assign them to the fields
      // console.log(place);
      var geocoder = new google.maps.Geocoder()
      var address = document.getElementById('id_address').value

      geocoder.geocode({'address': address}, function(results, status){
          // console.log('results=>', results)
          // console.log('status=>', status)
          if(status == google.maps.GeocoderStatus.OK){
              var latitude = results[0].geometry.location.lat();
              var longtitude = results[0].geometry.location.lng();

              $('#id_latitude').val(latitude)
              $('#id_longtitude').val(longtitude)
          }
      });

      // loop through the address components and assign other address data
      console.log(place.address_components);
      for(var i=0; i<place.address_components.length; i++){
          for(var j=0; j<place.address_components[i].types.length; j++){
              // get country
              if(place.address_components[i].types[j] == 'country'){
                  $('#id_country').val(place.address_components[i].long_name);
              }
              // get state
              if(place.address_components[i].types[j] == 'administrative_area_level_1'){
                  $('#id_state').val(place.address_components[i].long_name);
              }
              // get city
              if(place.address_components[i].types[j] == 'locality'){
                  $('#id_city').val(place.address_components[i].long_name);
              }
              // get pincode
              if(place.address_components[i].types[j] == 'postal_code'){
                  $('#id_pin_code').val(place.address_components[i].long_name);
              }else{
                  $('#id_pin_code').val("");
              }
          }
      }

  }

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

