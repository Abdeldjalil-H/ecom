var updateBtns = document.getElementsByClassName('update-cart')

for(const btn of updateBtns) {
    btn.addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action

        if(user === 'AnonymousUser') {
            console.log('not')
        } else {
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action) {
    fetch(fetchUrl, {
        method: 'POST', 
        headers: {
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'productId': productId, 'action': action})
    })

    .then((response) =>  response.json())

    .then((data) => {
        var cartItems = data['cartItems']
        for(node of document.getElementsByClassName('cart-items')) {
            node.innerHTML = cartItems;
        }
        for(node of document.getElementsByClassName('total-price')) {
            node.innerHTML = data['totalPrice']
        }
    })
}