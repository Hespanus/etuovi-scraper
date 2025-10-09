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
            const response = await fetch('/api/trigger-scraper', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: url }),
            });
            
            // TÄMÄ ON DEBUGGAUSVAIHE: Tarkistetaan mitä palvelin lähetti takaisin
            const rawResponse = await response.clone().text();
            console.log("Palvelimen raaka vastaus:", rawResponse);

            if (!response.ok) {
            // Jos API palauttaa virheen (esim. 500), yritetään näyttää se
            try {
                const errorData = JSON.parse(rawResponse);
                throw new Error(errorData.error || `HTTP-virhe: ${response.status} (${errorData.message || 'Tuntematon virhe API:ssa'})`);
            } catch (e) {
                // Jos vastaus ei ollut JSON, näytetään raaka teksti.
                throw new Error(`HTTP-virhe: ${response.status}. Palvelin palautti epämuotoista dataa: ${rawResponse}`);
            }
        }

            const scrapedData = await response.json();
            //console.log(`scraped:`, scrapedData);

            if (Array.isArray(scrapedData) && scrapedData.length > 0) {
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
        } catch (error) {
            console.error('Virhe pyynnössä:', error);
            statusDiv.textContent = `Virhe: ${error.message || 'Tuntematon virhe'}`;
        }
    });
});
