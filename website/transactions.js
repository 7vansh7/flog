let transaction_form = document.getElementById('transaction_form')
let private_key = document.getElementsById('private_key').value
let change = document.getElementsById('change_value').value
let senders_public_key = document.getElementById('senders_public_key').value


async function send_transaction(event){
    event.preventDefault()

    if (!private_key | !change | !senders_public_key) {
        console.error("Private key or change or sender's public key not found or empty");
        alert('Private key empty')
        return
        }
    to_send = {
        private_key: private_key,
        change:change,
        senders_public_key:senders_public_key
    }
    let res = await fetch("http://127.0.0.1:8000/",{
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
}

transaction_form.addEventListener('submit',send_transaction)