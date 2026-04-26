const UNARY_OPS = new Set(['sqrt', 'log']);

const opSymbolToApi = {
    '+': '+',
    '−': '-',
    '×': '*',
    '÷': '/',
    '**': '**',
    '%': '%',
    'sqrt': 'sqrt',
    'log': 'log',
};

const exprEl = document.getElementById('expression');
const resultEl = document.getElementById('result');
const input1 = document.getElementById('operand1');
const input2 = document.getElementById('operand2');
const input2Wrapper = input2.parentElement;
const opBtns = document.querySelectorAll('.op-btn');

let state = { a: '', b: '', op: '+' };
let debounceTimer = null;
let activeController = null;

function setActiveOp(symbol) {
    state.op = symbol;
    opBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.op === symbol);
    });

    const isUnary = UNARY_OPS.has(symbol);
    if (isUnary) {
        input2.disabled = true;
        input2Wrapper.style.opacity = '0.5';
    } else {
        input2.disabled = false;
        input2Wrapper.style.opacity = '1';
    }
}

function formatNumber(x) {
    const precise = parseFloat(x.toPrecision(10));
    return String(precise);
}

function showResult(value) {
    resultEl.textContent = formatNumber(value);
    resultEl.classList.remove('error');
}

function showError(msg) {
    resultEl.textContent = msg;
    resultEl.classList.add('error');
}

function updateExpression() {
    const a = state.a !== '' ? state.a : '?';
    const isUnary = UNARY_OPS.has(state.op);

    if (isUnary) {
        exprEl.textContent = `${state.op}(${a})`;
    } else {
        const b = state.b !== '' ? state.b : '?';
        exprEl.textContent = `${a} ${state.op} ${b}`;
    }
}

async function calculate() {
    const isUnary = UNARY_OPS.has(state.op);

    if (state.a === '') return;
    if (!isUnary && state.b === '') return;

    if (activeController) activeController.abort();
    activeController = new AbortController();

    try {
        const params = new URLSearchParams({
            operand1: state.a,
            operation: opSymbolToApi[state.op],
        });

        if (!isUnary) {
            params.append('operand2', state.b);
        }

        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: params.toString(),
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

setActiveOp('+');
