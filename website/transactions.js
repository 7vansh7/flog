let transaction_form = document.getElementById('transaction_form')
let private_key_elem = document.getElementById('private_key')
let change_elem = document.getElementById('change_value')
let receiver_public_key_elem = document.getElementById('receiver_public_key')


async function send_transaction(event){
    event.preventDefault()
    let private_key = private_key_elem.value
    let change = change_elem.value
    let receiver_public_key = receiver_public_key_elem.value
    if (!private_key || !change || !receiver_public_key) {
        console.error("Private key or change or sender's public key not found or empty");
        alert('Private key empty')
        return
        }
to_send = {
        private_key: private_key,
        change:change,
        receiver_public_key:receiver_public_key
    }
    let res = await fetch("http://127.0.0.1:8000/make_transaction/",{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json' 
        },
        body: JSON.stringify(to_send) 
    })
    if (!res.ok){
        console.error('Network error',res)
    }
    let data = await res.json()
    console.log(data.message)
    alert(data.message)
}

transaction_form.addEventListener('submit',send_transaction)