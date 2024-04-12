document.addEventListener('DOMContentLoaded', () => {
    updateCartTotals();
    addQuantityChangeListeners();
    addRemoveItemListeners();
    addClearCartListener();
});

function updateCartTotals() {
    let totalAmount = 0;
    let totalQuantity = 0;

    document.querySelectorAll("input[name=totalTxtPrice]").forEach(input => {
        totalAmount += parseFloat(input.value);
    });

    document.querySelectorAll("input[name=item]").forEach(input => {
        totalQuantity += parseInt(input.value);
    });

    document.querySelector(".totalAmount").textContent = totalAmount.toFixed(2);
    document.querySelector(".totalQuantity").textContent = totalQuantity;
}

function addQuantityChangeListeners() {
    document.querySelectorAll(".bi-cart-plus-fill").forEach(item => {
        item.addEventListener("click", () => updateItemQuantity(item, true));
    });

    document.querySelectorAll(".bi-cart-dash").forEach(item => {
        item.addEventListener("click", () => updateItemQuantity(item, false));
    });
}

function updateItemQuantity(item, isIncrease) {
    const closestTr = item.closest("tr");
    const closestPrice = parseFloat(closestTr.querySelector(".txtprice").textContent.replace('$', ''));
    const closestQuantityInput = closestTr.querySelector("input[name=item]");
    const closestTotalPriceInput = closestTr.querySelector("input[name=totalTxtPrice]");

    let currentQuantity = parseInt(closestQuantityInput.value);
    let newQuantity = isIncrease ? currentQuantity + 1 : currentQuantity - 1;
    if (newQuantity < 0) newQuantity = 0; // Ensure quantity cannot be negative

    closestQuantityInput.value = newQuantity;
    closestTotalPriceInput.value = closestPrice * newQuantity;

    updateCartTotals();
}

function addRemoveItemListeners() {
    document.querySelectorAll('.remove-item').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            removeItemFromCart(productId);
        });
    });
}

function removeItemFromCart(productId) {
    fetch(`/store/users/cart/remove/${productId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        } else {
            console.error('Failed to remove item from cart');
        }
    })
    .catch(error => console.error('Error:', error));
}

function addClearCartListener() {
    document.getElementById('clear-cart-btn').addEventListener('click', () => clearCart());
}

function clearCart() {
    fetch('/store/users/cart/clear/', {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
    })
    .then(response => {
        if (response.ok) {
            location.reload();
        } else {
            console.error('Failed to clear cart');
        }
    })
    .catch(error => console.error('Error:', error));
}