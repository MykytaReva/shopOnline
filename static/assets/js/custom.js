let autocomplete;
let addressComponents = {}; // declare addressComponents in a global scope

// i do not believe that it is this one2222
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

      addressComponents = place.address_components.reduce((obj, item) => { // assign value to addressComponents
        if (item.types[0] === 'country') {
          obj[item.types[0]] = item.short_name;
        } else {
          obj[item.types[0]] = item.long_name;
        }
        return obj;
      }, {});
      console.log(addressComponents);
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

//newsletter
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


//model
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


// wishlist home page
$(document).ready(function() {
  // submit form data using AJAX
  $("form[id^='wish-form']").on('submit', function(event) {
    event.preventDefault();

    // disable submit button

    // send AJAX request
    $.ajax({
      url: $(this).attr('action'),
      type: 'POST',
      data: $(this).serialize(),
      success: function(response) {
        // Enable submit button
        $('#wish-btn-' + response.item_id).attr('disabled', false);

        // Update the heart icon
        if ($('#fa-' + response.item_id).hasClass('fa-regular')) {
            $('#fa-' + response.item_id).removeClass('fa-regular').addClass('fa-solid');
        } else {
            $('#fa-' + response.item_id).removeClass('fa-solid').addClass('fa-regular');
        }

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

  // wishlist page remove card
  $(document).ready(function() {
    // submit form data using AJAX
    $("form[id^='wish-page']").on('submit', function(event) {
      event.preventDefault();

      // disable submit button

      // send AJAX request
      var form = $(this);
      $.ajax({
        url: $(this).attr('action'),
        type: 'POST',
        data: $(this).serialize(),
        success: function(response) {

          Swal.fire({
              icon: response.icon,
              title: response.message,
          });
          var itemId = form.attr('id').split('-')[2];
          $('#wish-card-' + itemId).remove();

          var wishDiv = $('#w-count');
          var wqty = parseInt(wishDiv.text());
          wishDiv.text(wqty - 1);
          if (wqty == 1) {
            $('#empty-wishlist').css('display', 'block');
          }
      },

        error: function(xhr, status, error) {
          // enable submit button
          $('#report-btn').attr('disabled', false);
        }
      });
    });
  });


// add to the cart
$(document).ready(function() {
  // submit form data using AJAX
  $("form[id^='add-cart']").on('submit', function(event) {
    event.preventDefault();

    // disable submit button

    // send AJAX request
    var form = $(this);
    $.ajax({
      url: $(this).attr('action'),
      type: 'POST',
      data: $(this).serialize(),
      success: function(response) {
        // show success/error message
        // Swal.fire({
        //   icon: response.icon,
        //   title: response.message,
        // });
        $('#add-cart-btn').attr('disabled', true);
        if ($('#fa-icon').hasClass('fa fa-cart-plus')) {
          Swal.fire({
            icon: response.icon,
            title: response.message,
          });
          $('#fa-icon').removeClass('fa fa-cart-plus').addClass('fa fa-shopping-cart');
      }
        // increment quantity
        var itemId = form.attr('id').split('-')[2];
        var quantityDiv = $('#qty-' + itemId);
        var cartSpan = $('#cart-c');
        var item_price = $('#price-' + itemId)
        var price = $('#ttott')

        var item_price_sum = parseFloat(item_price.text()).toFixed(2);
        var sumprice = parseFloat(price.text()).toFixed(2);
        var quantity = parseInt(quantityDiv.text());
        var quantityCart = parseInt(cartSpan.text());

        quantityDiv.text(quantity + 1);
        cartSpan.text(quantityCart + 1);
        price.text((parseFloat(sumprice)+parseFloat(item_price_sum)).toFixed(2));

      },
      error: function(xhr, status, error) {
        // enable submit button
      }
    });
  });
});

// subtract from the cart
$(document).ready(function() {
  // submit form data using AJAX
  $("form[id^='subtract-cart']").on('submit', function(event) {
    event.preventDefault();
    // send AJAX request
    var form = $(this);
    $.ajax({
      url: $(this).attr('action'),
      type: 'POST',
      data: $(this).serialize(),
      success: function(response) {
        // increment quantity
        var itemId = form.attr('id').split('-')[2];
        var quantityDiv = $('#qty-' + itemId);
        var cartSpan = $('#cart-c');
        var item_price = $('#price-' + itemId)
        var price = $('#ttott')

        var item_price_sum = parseFloat(item_price.text()).toFixed(2);
        var sumprice = parseFloat(price.text()).toFixed(2);
        var quantity = parseInt(quantityDiv.text());
        var quantityCart = parseInt(cartSpan.text());

        quantityDiv.text(quantity - 1);
        cartSpan.text(quantityCart - 1);
        price.text((parseFloat(sumprice)-parseFloat(item_price_sum)).toFixed(2));
        // delete item if quantity is 0
        if (quantity - 1 <= 0) {
          Swal.fire({
            icon: response.icon,
            title: response.message,
          });
          $('#tr-' + itemId).remove();
        }
        if ($('.table tbody tr').length == 0) {
          $('#empty-cart').css('display', 'block');
          $('#tab').css('display', 'none');
        }

      },
      error: function(xhr, status, error) {
        // enable submit button
      }
    });
  });
});

//delete from the cart
$(document).ready(function() {
  // submit form data using AJAX
  $("form[id^='remove-cart']").on('submit', function(event) {
    event.preventDefault();

    // disable submit button

    // send AJAX request
    var form = $(this);
    $.ajax({
      url: $(this).attr('action'),
      type: 'POST',
      data: $(this).serialize(),
      success: function(response) {
        // show success/error message
        Swal.fire({
          icon: response.icon,
          title: response.message,
        });
        var itemId = form.attr('id').split('-')[2];
        var quantityDiv = $('#qty-' + itemId);
        var cartSpan = $('#cart-c');
        var item_price = $('#price-' + itemId)
        var price = $('#ttott')

        var item_price_sum = parseFloat(item_price.text()).toFixed(2);
        var sumprice = parseFloat(price.text()).toFixed(2);
        var quantity = parseInt(quantityDiv.text());
        var quantityCart = parseInt(cartSpan.text());

        cartSpan.text(quantityCart - quantity);
        price.text((parseFloat(sumprice)-parseFloat(item_price_sum)*parseFloat(quantity)).toFixed(2));

        // delete item if quantity is 0
        $('#tr-' + itemId).remove();
        if ($('.table tbody tr').length == 0) {
          $('#empty-cart').css('display', 'block');
          $('#tab').css('display', 'none');
        }

      },
      error: function(xhr, status, error) {
        // enable submit button
      }
    });
  });
});
