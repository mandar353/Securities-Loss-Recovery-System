

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        const formData = new FormData(form);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok) {

                const summary = result.summary || {};

                const totalLoss = summary.total_loss ?? 0;
                const totalInvestment = summary.total_investment ?? 0;
                const totalSale = summary.total_sale ?? 0;
                const eligibleRecords = summary.eligible_records ?? 0;

                document.getElementById('result').innerHTML = `
                    <h3>Results</h3>
                    <p><strong>Total Loss:</strong> $${totalLoss.toFixed(2)}</p>
                    <p><strong>Total Investment:</strong> $${totalInvestment.toFixed(2)}</p>
                    <p><strong>Total Sale:</strong> $${totalSale.toFixed(2)}</p>
                    <p><strong>Eligible Records:</strong> ${eligibleRecords}</p>

                    <a href="${result.download_url}" download class="download-btn">
                        Download Processed File
                    </a>
                `;
            } else {
                document.getElementById('result').innerHTML = `<p style="color:red;">${result.detail}</p>`;
            }

        } catch (error) {
            document.getElementById('result').innerHTML = `<p style="color:red;">${error.message}</p>`;
        }
    });
});