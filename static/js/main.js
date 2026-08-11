// JobConnect Premium Client-side scripts

document.addEventListener("DOMContentLoaded", function () {
    // 1. Automatically fade out alert messages after 5 seconds
    const alerts = document.querySelectorAll(".alert-dismissible");
    alerts.forEach(function (alert) {
        setTimeout(function () {
            let bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        }, 5000);
    });

    // 2. Micro-animation on button and card hovers
    const animateCards = document.querySelectorAll(".card-custom");
    animateCards.forEach(function (card) {
        card.addEventListener("mouseenter", function () {
            this.style.transition = "all 0.3s cubic-bezier(0.16, 1, 0.3, 1)";
        });
    });
});

/**
 * Draws a beautiful dashboard statistics bar chart on a canvas element.
 * @param {string} canvasId - The ID of the canvas element.
 * @param {Array} labels - Label array for the jobs.
 * @param {Array} data - Data counts of applications.
 */
function drawRecruiterChart(canvasId, labels, data) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    const width = canvas.width;
    const height = canvas.height;
    
    // Clear canvas
    ctx.clearRect(0, 0, width, height);

    // If no data, show message
    if (!data || data.length === 0) {
        ctx.fillStyle = "#64748b";
        ctx.font = "14px 'Inter', sans-serif";
        ctx.textAlign = "center";
        ctx.fillText("No application data available yet", width / 2, height / 2);
        return;
    }

    const padding = 40;
    const chartHeight = height - padding * 2;
    const chartWidth = width - padding * 2;
    
    const maxVal = Math.max(...data, 5); // Default to at least 5 grid lines
    const barWidth = Math.min(50, chartWidth / data.length - 20);
    const spacing = (chartWidth - barWidth * data.length) / (data.length + 1);

    // Draw grid lines
    ctx.strokeStyle = "#e2e8f0";
    ctx.lineWidth = 1;
    ctx.fillStyle = "#64748b";
    ctx.font = "10px 'Inter', sans-serif";
    
    const gridLines = 5;
    for (let i = 0; i <= gridLines; i++) {
        const y = padding + chartHeight - (i / gridLines) * chartHeight;
        const val = Math.round((i / gridLines) * maxVal);
        
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(width - padding, y);
        ctx.stroke();
        
        ctx.fillText(val, padding - 15, y + 4);
    }

    // Draw bars
    data.forEach((val, idx) => {
        const barHeight = (val / maxVal) * chartHeight;
        const x = padding + spacing + idx * (barWidth + spacing);
        const y = padding + chartHeight - barHeight;

        // Gradient for bars
        const gradient = ctx.createLinearGradient(x, y, x, y + barHeight);
        gradient.addColorStop(0, "#4f46e5"); // indigo
        gradient.addColorStop(1, "#818cf8"); // light indigo

        // Rounded bar
        ctx.fillStyle = gradient;
        ctx.beginPath();
        if (ctx.roundRect) {
            ctx.roundRect(x, y, barWidth, barHeight, [4, 4, 0, 0]);
        } else {
            ctx.rect(x, y, barWidth, barHeight);
        }
        ctx.fill();

        // Draw values on top of bars
        ctx.fillStyle = "#0f172a";
        ctx.font = "bold 11px 'Inter', sans-serif";
        ctx.textAlign = "center";
        ctx.fillText(val, x + barWidth / 2, y - 6);

        // Draw labels below chart
        ctx.fillStyle = "#475569";
        ctx.font = "10px 'Inter', sans-serif";
        const rawLabel = labels[idx] || "";
        const truncLabel = rawLabel.length > 10 ? rawLabel.substring(0, 8) + ".." : rawLabel;
        ctx.fillText(truncLabel, x + barWidth / 2, padding + chartHeight + 16);
    });
}
