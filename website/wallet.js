let wallet_info_form = document.getElementById('wallet_info')
let holdings_add_form = document.getElementById('wallet_holdings_add')
let create_wallet_form = document.getElementById('create_wallet_form')
let wallet_add_ptag = document.getElementById('wallet_info_ptag')
let private_key_ptag = document.getElementById('new_private_key')
let public_key_ptag = document.getElementById('new_public_key')
let holdings_add_confirmation = document.getElementById('holdings_add_confirmation')

async function get_wallet_info(event){
   event.preventDefault()
   let private_key =  document.getElementById('text').value
   if (!private_key) {
    console.error('Private key not found or empty');
    alert('Private key empty')
    return
    }
   let holdings = await fetch(`http://127.0.0.1:8000/wallet_info/`,{
    method: 'POST', 
    headers: {
        'Content-Type': 'application/json' 
    },
    body: JSON.stringify({private_key: private_key}) 
})
    if (!holdings.ok){
        throw new Error('Network response was not ok');
    }
    let data = await holdings.json();
    wallet_add_ptag.textContent = data.message
}

async function add_holdings_to_wallet(event){
    event.preventDefault()
    let public_key =  document.getElementById('public_key_form_holdings').value
    let change = document.getElementById('text_change').value
    if (!public_key | !change) {
     console.error('Public key or change not found or empty');
     alert('Public key or change empty')
     return
     }
     to_send = {public_key: public_key,change:change}
     console.log(to_send)
    let message = await fetch(`http://127.0.0.1:8000/wallet_add/`,{
     method: 'POST', 
     headers: {
         'Content-Type': 'application/json' 
     },
     body: JSON.stringify(to_send) 
 })
     if (!message.ok){
         throw new Error('Network response was not ok',message.body);
     }
     let data = await message.json();
     holdings_add_confirmation.textContent = data.message
 }
 
async function create_new_user(event){
    event.preventDefault()
    let ans = await fetch('http://127.0.0.1:8000/create_wallet/',{
        method: 'GET', 
    })
    
    if (!ans.ok){
        throw new Error('Network response was not ok',ans.body);
    }
    let data = await ans.json();
    alert(data.message)
    public_key_ptag.innerText = data.public_key
    private_key_ptag.textContent = data.private_key
}

wallet_info_form.addEventListener('submit', get_wallet_info)
create_wallet_form.addEventListener('submit',create_new_user)
holdings_add_form.addEventListener('submit',add_holdings_to_wallet)