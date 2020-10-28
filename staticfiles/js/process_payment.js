const page_data = JSON.parse(document.getElementById('page_data').textContent);

const paymentButton = document.getElementById("submit");
paymentButton.disabled = true;

const stripe_pk = page_data["stripe_pk"];
const stripe = Stripe(stripe_pk);
const pmtAmt = page_data["amt"] * 100.0;
const description = "Test description";
fetch("/payments/get-payment-intent/", {
    method: "POST",
    headers: {
        "X-CSRFToken": getCookie("csrftoken"),
        "Accept": "application/json",
        "Content-type": "application/json"
    },
    body: JSON.stringify({
        payment_amount: pmtAmt,
        description: description
    }),
})
.then(function(res) {
    return res.json();
})
.then(function(data) {
    const elements = stripe.elements();

    const style = {
        base: {
            color: "#32325d",
            fontFamily: "Arial, sans-serif",
            fontSmoothing: "antialiased",
            fontSize: "16px",
            "::placeholder": {
                color: "#32325d"
            },
        },
        invalid: {
            fontFamily: "Arial, sans-serif",
            color: "#fa755a",
            iconColor: "#fa755a"
        }
    };

    const card = elements.create("card", { style: style });
    card.mount("#card-element");

    card.on("change", function (e) {
        paymentButton.disabled = e.empty;
        document.querySelector("#card-error").textContent = e.error ? e.error.message : "";
    });

    const paymentForm = document.getElementById("payment-form");
    paymentForm.addEventListener("submit", function(e) {
        e.preventDefault();
        payWithCard(stripe, card, data.clientSecret);
    });
})
.catch(function(err) {
    console.error(err.message);
});

const payWithCard = function(stripe, card, clientSecret) {
    submitting(true);
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            type: "card",
            card: card,
            billing_details: {
                address: {
                    line1: page_data["street_address"],
                    city: page_data["city"],
                    state: page_data["state"],
                    postal_code: page_data["zipcode"],
                },
                email: page_data["email"],
                name: page_data["name"],
                phone: page_data["phone"],
            },
        },
        receipt_email: page_data["email"]
    })
    .then(function(result) {
        if (result.error) {
            showError(result.error.message);
        } else {
            orderComplete(result.paymentIntent.id, result.paymentIntent.amount, result.paymentIntent.created);
        }
    });
}

const orderComplete = function(paymentIntentId, amount, tstamp) {
    const paymentConfirmation = Math.random().toString(16).substr(2, 12);
    let queryParams = "?p=" + paymentIntentId;
    queryParams += "&p_cnf=" + tstamp + "-" + paymentConfirmation;
    queryParams += "&amt=" + amount;
    const redirectURL = "/payments/payment-success/" + queryParams;
    window.location = redirectURL;
}

const showError = function(errorText) {
    submitting(false);
    paymentButton.disabled = true;
    const paymentForm = document.getElementById('payment-form');
    const errorDisplay = document.getElementById('card-error');
    paymentForm.style.display = "none";
    errorDisplay.innerHTML =
        '<p class="lead text-danger">Whoops! An error occurred while processing your payment.</p><p>' +
        errorText +
        '</p><p>Please try again later.</p>';
}

const submitting = function(isSubmitting) {
    if (isSubmitting) {
        document.getElementById('button-icon-regular').classList.add('hidden');
        document.getElementById('button-icon-wait').classList.remove('hidden');
        document.getElementById('button-text').innerText = "Submitting payment, please wait...";
        paymentButton.disabled = true;
    } else {
        document.getElementById('button-icon-regular').classList.remove('hidden');
        document.getElementById('button-icon-wait').classList.add('hidden');
        document.getElementById('button-text').innerText = "Submit Payment";
        paymentButton.disabled = false;
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}