// web/script.js

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('scraperForm');
    const urlInput = document.getElementById('urlInput');
    const statusDiv = document.getElementById('status');
    const resultsContainer = document.createElement('div');
    resultsContainer.id = 'results-container';
    document.querySelector('.container').appendChild(resultsContainer);

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const url = urlInput.value;
        statusDiv.textContent = 'Skrappaaja käynnistyy... Ole hyvä ja odota.';
        resultsContainer.innerHTML = ''; // Tyhjennetään aiemmat tulokset

        try {
            const response = await fetch('http://localhost:5000/trigger-scraper', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: url }),
            });
            
            const scrapedData = await response.json();
            console.log(`scraped: ${scrapedData}`);

            if (response.ok) {
                // Tässä voit lisätä tarkistuksen, onko scraperissa virheitä
                if (scrapedData.error) {
                    statusDiv.textContent = `Virhe: ${scrapedData.error}`;
                } else if (Array.isArray(scrapedData) && scrapedData.length > 0) {
                    statusDiv.textContent = 'Skrappaaja valmis. Tässä tulokset:';
                    
                    scrapedData.forEach(item => {
                        const apartmentDiv = document.createElement('div');
                        apartmentDiv.className = 'apartment-listing';
                        // HUOM: Muutettu avaimet vastaamaan scraperin palauttamaa dataa
                        apartmentDiv.innerHTML = `
                            <h4>${item.Address}</h4>
                            <p><strong>Hinta:</strong> ${item.Price}</p>
                            <p><a href="${item.Link}" target="_blank">Katso ilmoitus</a></p>
                        `;
                        resultsContainer.appendChild(apartmentDiv);
                    });
                } else {
                    statusDiv.textContent = 'Ei ilmoituksia tällä hakuehdolla tai skrappaaja palautti virheen.';
                }
            } else {
                statusDiv.textContent = `Virhe: ${scrapedData.error || 'Tuntematon virhe'}`;
            }
        } catch (error) {
            console.error('Virhe pyynnössä:', error);
            statusDiv.textContent = `Virhe: Ei voitu yhdistää palvelimeen.`;
        }
    });
});