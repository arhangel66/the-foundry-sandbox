const opSymbolToApi = { '+': '+', '−': '-', '×': '*', '÷': '/' };

const exprEl = document.getElementById('expression');
const resultEl = document.getElementById('result');
const input1 = document.getElementById('operand1');
const input2 = document.getElementById('operand2');
const opBtns = document.querySelectorAll('.op-btn');

let state = { a: '', b: '', op: '+' };
let debounceTimer = null;
let activeController = null;

function setActiveOp(symbol) {
    state.op = symbol;
    opBtns.forEach(btn => {
        const active = btn.dataset.op === symbol;
        btn.classList.toggle('bg-indigo-600', active);
        btn.classList.toggle('bg-gray-800', !active);
    });
}

function formatNumber(x) {
    // Limit float precision to avoid 0.1+0.2 noise
    const precise = parseFloat(x.toPrecision(10));
    return String(precise);
}

function showResult(value) {
    resultEl.textContent = formatNumber(value);
    resultEl.classList.remove('text-red-400');
    resultEl.classList.add('text-white');
}

function showError(msg) {
    resultEl.textContent = msg;
    resultEl.classList.remove('text-white');
    resultEl.classList.add('text-red-400');
}

function updateExpression() {
    const a = state.a !== '' ? state.a : '?';
    const b = state.b !== '' ? state.b : '?';
    exprEl.textContent = `${a} ${state.op} ${b}`;
}

async function calculate() {
    if (state.a === '' || state.b === '') return;

    if (activeController) activeController.abort();
    activeController = new AbortController();

    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({
                operand1: state.a,
                operand2: state.b,
                operation: opSymbolToApi[state.op],
            }).toString(),
            signal: activeController.signal,
        });

        const data = await response.json();

        if (!response.ok) {
            showError(data.detail || 'Error');
        } else {
            showResult(data.result);
        }
    } catch (err) {
        if (err.name !== 'AbortError') showError('Error');
    }
}

function scheduleCalculate(immediate = false) {
    clearTimeout(debounceTimer);
    if (immediate) {
        calculate();
    } else {
        debounceTimer = setTimeout(calculate, 300);
    }
}

input1.addEventListener('input', () => {
    state.a = input1.value;
    updateExpression();
    scheduleCalculate();
});

input2.addEventListener('input', () => {
    state.b = input2.value;
    updateExpression();
    scheduleCalculate();
});

[input1, input2].forEach(el => {
    el.addEventListener('keydown', e => {
        if (e.key === 'Enter') scheduleCalculate(true);
    });
});

opBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        setActiveOp(btn.dataset.op);
        updateExpression();
        scheduleCalculate(true);
    });
});

// Default active op
setActiveOp('+');
