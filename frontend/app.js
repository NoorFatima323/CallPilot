async function bookAppointment() {
    const service_type = document.getElementById("service").value;
    const preferred_date = document.getElementById("date").value;
    const time_range = document.getElementById("time").value;
    const user_name = document.getElementById("name").value;

    if (!preferred_date) {
        alert("Please select a date");
        return;
    }

    // Initial running message
    document.getElementById("output").textContent =
        "🤖 Running agent swarm...\nContacting providers...\nEvaluating availability...\n";

    try {
        const response = await fetch("http://127.0.0.1:8000/book_appointment", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                service_type,
                preferred_date,
                time_range,
                user_name
            })
        });

        const data = await response.json();
        const resultBox = document.getElementById("resultBox");
        const resultText = document.getElementById("resultText");

        if (data.top_providers && data.top_providers.length > 0) {
            // Display top 3 options
            let providersHTML = "";
            data.top_providers.forEach((p, index) => {
                providersHTML += `
                    <h4>Option ${index + 1}</h4>
                    <strong>Provider:</strong> ${p.name}<br>
                    <strong>Service:</strong> ${p.type}<br>
                    <strong>Time Slot:</strong> ${p.appointment_slot}<br>
                    <strong>Rating:</strong> ⭐ ${p.rating}<br>
                    <strong>Distance:</strong> ${p.distance_km} km<br><br>
                `;
            });
            resultText.innerHTML = providersHTML;
            resultBox.classList.remove("hidden");

            // Show top provider confirmation in output <pre>
            const best = data.top_providers[0];
            document.getElementById("output").textContent =
                `✅ Appointment Confirmed (Top Choice)\n\n` +
                `Provider: ${best.name}\n` +
                `Service: ${best.type}\n` +
                `Time Slot: ${best.appointment_slot}\n` +
                `Rating: ⭐ ${best.rating}\n` +
                `Distance: ${best.distance_km} km\n\n` +
                `🧠 Decision Logic:\n` +
                `- Agent contacted ${data.top_providers.length} providers\n` +
                `- Respected your time preference: ${time_range}\n` +
                `- Scored options by rating & distance\n` +
                `- Selected optimal slot automatically`;

        } else {
            document.getElementById("output").textContent = "❌ " + data.message;
            resultBox.classList.add("hidden");
        }

    } catch (error) {
        document.getElementById("output").textContent =
            "❌ Error connecting to backend.\nMake sure FastAPI server is running.";
        resultBox.classList.add("hidden");
    }
}
