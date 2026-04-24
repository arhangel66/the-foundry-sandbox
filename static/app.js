const form = document.getElementById('calculatorForm');
const resultContainer = document.getElementById('resultContainer');
const errorContainer = document.getElementById('errorContainer');
const resultValue = document.getElementById('resultValue');
const errorMessage = document.getElementById('errorMessage');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const operand1 = parseFloat(document.getElementById('operand1').value);
    const operand2 = parseFloat(document.getElementById('operand2').value);
    const operation = document.getElementById('operation').value;

    // Hide previous results/errors
    resultContainer.classList.add('hidden');
    errorContainer.classList.add('hidden');

    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                operand1,
                operand2,
                operation,
            }).toString(),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Unknown error');
        }

        const data = await response.json();
        resultValue.textContent = data.result;
        resultContainer.classList.remove('hidden');
    } catch (error) {
        errorMessage.textContent = error.message;
        errorContainer.classList.remove('hidden');
    }
});
