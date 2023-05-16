// var stripe = Stripe('pk_test_51MONwDBlafiM1XPR4QImWUi1iYocnjdirTLwPcRG4JLRA4Ne21UmAdH1WxTnMHFU9CoikdBBDUX17wpt9crgMT2q00EqU5OVnh');

// var elem = document.getElementById('submit');
// clientsecret = elem.getAttribute('data-secret');

// var elements = stripe.elements();
// var style = {
//     base: {
//         color: "#000",
//         lineHeight: '2.4',
//         fontSize: '16px'
//     }
// };

// var card = elements.create('card', {style: style});
// card.mount('#card-element');

// card.on('change', function(event){
//     var displayError = document.getElementById('card-errors')
//     if (event.error) {
//         displayError.textContent = event.error.message;
//         $('#card-errors').addClass('alert alert-info');
//     } else {
//         displayError.textContent = '';
//         $('#card-errors').removeClass('alert alert-info');
//     }
// });

// var form = document.getElementById('payment-form');

// form.addEventListener('submit', function(ev){
//     ev.preventDefault();
//     var firstName = document.getElementById('firstName').value;
//     var lastName = document.getElementById('lastName').value;
//     var state = document.getElementById('id_state').value;
//     var phone_number = document.getElementById('id_phone_number').value;
//     var address = document.getElementById('id_address').value;
//     var postCode = document.getElementById('id_pin_code').value;
//     var city = document.getElementById('id_city').value;
//     var country = document.getElementById('id_country').value;

//     $.ajax({
//         type: 'POST',
//         url: 'http://127.0.0.1:8000/orders/add/',
//         data: {
//             order_key: clientsecret,
//             csrfmiddlewaretoken: CSRF_TOKEN,
//             action: 'post',
//             first_name: firstName,
//             last_name: lastName,
//             address: address,
//             pin_code: postCode,
//             city: city,
//             country: country,
//             phone_number: phone_number,
//             state: state,
//         },
//         success: function (json) {
//             stripe.confirmCardPayment(clientsecret, {
//                 payment_method: {
//                     card: card,
//                     billing_details:{
//                         name: firstName+lastName,
//                         address: {
//                             line1: address,
//                             postal_code: postCode,
//                             country: country,
//                             city: city
//                         }
//                     },
//                 }
//             }).then(function(result){
//                 if (result.error) {
//                     console.log('payment error')
//                     console.log(result.error.message)
//                 } else {
//                     if (result.paymentIntent.status == 'succeeded') {

//                         window.location.replace('http://127.0.0.1:8000/payment/orderplaced/');
//                     }
//                 }
//             });

//         },
//         error: function(xhr, errmsg, err){},
//     });

// });
var stripe = Stripe('pk_test_51MONwDBlafiM1XPR4QImWUi1iYocnjdirTLwPcRG4JLRA4Ne21UmAdH1WxTnMHFU9CoikdBBDUX17wpt9crgMT2q00EqU5OVnh');

var elem = document.getElementById('submit');
clientsecret = elem.getAttribute('data-secret');

var elements = stripe.elements();
var style = {
    base: {
        color: "#000",
        lineHeight: '2.4',
        fontSize: '16px'
    }
};

var card = elements.create('card', {style: style});
card.mount('#card-element');

card.on('change', function(event){
    var displayError = document.getElementById('card-errors')
    if (event.error) {
        displayError.textContent = event.error.message;
        $('#card-errors').addClass('alert alert-info');
    } else {
        displayError.textContent = '';
        $('#card-errors').removeClass('alert alert-info');
    }
});
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev){
    ev.preventDefault();
    var firstName = document.getElementById('firstName').value;
    var lastName = document.getElementById('lastName').value;
    var state = document.getElementById('id_state').value;
    var phone_number = document.getElementById('id_phone_number').value;
    var address = document.getElementById('id_address').value;
    var postCode = document.getElementById('id_pin_code').value;
    var city = document.getElementById('id_city').value;
    var countryName = document.getElementById('id_country').value;
    console.log(countryName);

    // Create a geocoder object
    var geocoder = new google.maps.Geocoder();

    // Geocode the country name to get the country code
    geocoder.geocode({ address: countryName }, function(results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
            if (results.length > 0) {
                var countryCode = results[0].address_components[0].short_name;
                console.log(countryName);
                if (countryCode) {
                    console.log('Valid country code:', countryCode);
                } else {
                    console.log('Invalid country name');
                    countryCode = null;
                    console.log('Proceeding with payment without country code');
                }

                // Use the countryCode in your AJAX data
                $.ajax({
                    type: 'POST',
                    url: 'http://127.0.0.1:8000/orders/add/',
                    data: {
                        order_key: clientsecret,
                        csrfmiddlewaretoken: CSRF_TOKEN,
                        action: 'post',
                        first_name: firstName,
                        last_name: lastName,
                        address: address,
                        pin_code: postCode,
                        city: city,
                        country: countryCode,
                        phone_number: phone_number,
                        state: state,
                    },
                    success: function (json) {
                        stripe.confirmCardPayment(clientsecret, {
                            payment_method: {
                                card: card,
                                billing_details:{
                                    name: firstName + lastName,
                                    address: {
                                        line1: address,
                                        postal_code: postCode,
                                        country: countryCode,
                                        city: city
                                    }
                                },
                            }
                        }).then(function(result){
                            if (result.error) {
                                Swal.fire({
                                    icon: 'error',
                                    title: 'Payment Error',
                                    text: result.error.message
                                });
                                console.log('Payment error');
                                console.log(result.error.message);
                            } else {
                                if (result.paymentIntent.status == 'succeeded') {
                                    window.location.replace('http://127.0.0.1:8000/payment/orderplaced/');
                                }
                            }
                        });

                    },
                    error: function(xhr, errmsg, err){},
                });
            } else {
                // Country not found
            }
        } else {
            // Geocoding request failed
            Swal.fire({
                icon: 'error',
                title: 'Payment Error',
                text: 'Invalid country name'
            });
        }
    });
});