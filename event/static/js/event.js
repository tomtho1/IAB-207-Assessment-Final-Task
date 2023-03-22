function calcCost(quantity) {
    const cost = document.getElementById("cost");
    cost.value = (cost.getAttribute("data-cost") * quantity).toLocaleString('en-AU', { style: 'currency', currency: 'AUD' });
}

document.getElementById("quantity").addEventListener("click", (e) => calcCost(e.target.value));