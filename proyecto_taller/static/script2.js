document.addEventListener('DOMContentLoaded', function () {
    var productModal = new bootstrap.Modal(document.getElementById('productModal'));
    var productCards = document.getElementsByClassName('product-card');

    for (var i = 0; i < productCards.length; i++) {
        productCards[i].addEventListener('click', function () {
            var productName = this.getAttribute('data-product');
            var productDescription = this.getElementsByClassName('card-text')[0].innerText;

            document.getElementById('product-name').innerText = productName;
            document.getElementById('product-description').innerText = productDescription;

            productModal.show();
        });
    }
});