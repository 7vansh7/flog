let table_wallets = document.getElementById('all_wallets')
let table_transactions = document.getElementById('all_transactions')

let reload_button = document.getElementById('reload_button')

async function get_all_wallets(event){
    event.preventDefault()
    let res = await fetch("http://127.0.0.1:8000/all_public_keys")
    if(!res.ok){
        console.error('Network issue')
        return
    }
    let keys = await res.json()
    let keys_array = keys.keys.split(',')
    let count = 1
    keys_array.pop()
    keys_array.forEach(element => {
        let tr_element = document.createElement('tr')
        let td_element = document.createElement('td')
        let td_count = document.createElement('td')
        let tr = table_wallets.appendChild(tr_element)
        td_count.innerText = count
        tr.appendChild(td_count)
        td_element.innerText = element
        tr.appendChild(td_element)
        count ++
    });
}

reload_button.addEventListener('click', get_all_wallets)

// table_wallets.appendChild(tr_elemenet)
// table_wallets.appendChild(th_element)