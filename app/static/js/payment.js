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
    var country = addressComponents.country;
    var firstName = document.getElementById('firstName').value;
    var lastName = document.getElementById('lastName').value;
    var address = document.getElementById('id_address').value;
    var postCode = document.getElementById('id_pin_code').value;
    var city = document.getElementById('id_city').value;
    // var country = document.getElementById('id_country').value;

    stripe.confirmCardPayment(clientsecret, {
        payment_method: {
            card: card,
            billing_details:{
                name: firstName+lastName,
                address: {
                    line1: address,
                    postal_code: postCode,
                    country: country,
                    city: city
                }
            },
        }
    }).then(function(result){
        if (result.error) {
            console.log('payment error')
            console.log(result.error.message)
        } else {
            if (result.paymentIntent.status == 'succeeded') {
                console.log('payment processed')

                window.location.replace('http://127.0.0.1:8000/payment/orderplaced/');
            }
        }
    });
})