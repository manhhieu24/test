function redirect(Url) {
    window.location.href = Url;
}

function goBack() {
    window.history.back()
}


async function updateExchangeRate() {
  const currencySelect = document.getElementById('currencySelect');
  const selectedCurrency = currencySelect.value;
  const apiKey = '98ea6fa4eb9bc5bb5140fd36';
  const url = `https://v6.exchangerate-api.com/v6/${apiKey}/latest/USD`;

  try {
      const response = await fetch(url);
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      const data = await response.json();
      const exchangeRate = data.conversion_rates[selectedCurrency];

      const totalSumPriceElement = document.getElementById('totalSumPrice');
      const totalSumPriceUSD = parseFloat(totalSumPriceElement.dataset.usd);

      const convertedPrice = (totalSumPriceUSD * exchangeRate).toFixed(2);

      totalSumPriceElement.innerText = `Total: ${convertedPrice} ${selectedCurrency}`;
  } catch (error) {
      console.error('There was a problem with the fetch operation:', error);
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const currencySelect = document.getElementById('currencySelect');
  currencySelect.addEventListener('change', updateExchangeRate);
});



function openForm() {
  document.getElementById("myForm").style.display = "block";
}

function closeForm() {
  document.getElementById("myForm").style.display = "none";
}





