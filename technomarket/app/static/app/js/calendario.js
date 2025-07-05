const monthYearElement = document.getElementById('monthYear');
const datesElement = document.getElementById('dates');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const diasSemana = [
    "Domingo",    // 0
    "Lunes",      // 1
    "Martes",     // 2
    "Miercoles",  // 3
    "Jueves",     // 4
    "Viernes",    // 5
    "Sábado"      // 6
];

let currentDate = new Date();

const updateCalendar = () => {
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth();

    const firstDay = new Date(currentYear, currentMonth, 1);
    const lastDay = new Date(currentYear, currentMonth + 1, 0);
    const totalDays = lastDay.getDate();
    const firstDayIndex = firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1;
    const lastDayIndex = lastDay.getDay() === 0 ? 6 : lastDay.getDay() - 1;

    const monthYearString = currentDate.toLocaleString('default', {month: 'long', year:'numeric'});
    monthYearElement.textContent = monthYearString;

    let datesHTML = '';

    for (let i = 0; i < firstDayIndex; i++) {
        const prevDate = new Date(currentYear, currentMonth, -i);
        datesHTML = `<div class="date inactive">${prevDate.getDate()}</div>` + datesHTML;
    }

    for (let i = 1; i <= totalDays; i++) {
        const date = new Date(currentYear, currentMonth, i);
        const isToday = date.toDateString() === new Date().toDateString();
        const activeClass = isToday ? 'active' : '';
        const dayIndex = date.getDay(); // 0=Domingo ... 6=Sábado
        datesHTML += `<div class="date ${activeClass}" data-day-index="${dayIndex}">${i}</div>`;
    }

    for (let i = 1; i < 7 - lastDayIndex; i++) {
        const nextDate = new Date(currentYear, currentMonth + 1, i);
        datesHTML += `<div class="date inactive">${nextDate.getDate()}</div>`;
    }

    datesElement.innerHTML = datesHTML;
};

prevBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    updateCalendar();
});

nextBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    updateCalendar();
});

document.addEventListener("DOMContentLoaded", function () {
    const infoDiv = document.getElementById("info-horario");

    datesElement.addEventListener("click", function (e) {
        const target = e.target.closest(".date");
        if (!target || !target.dataset.dayIndex) return;

        const diaIndex = parseInt(target.dataset.dayIndex);
        const diaNombre = diasSemana[diaIndex];

        if (typeof disponibilidades !== 'undefined' && disponibilidades[diaNombre]) {
            const html = disponibilidades[diaNombre].map(d => `
                <div class="trabajador-item">
                    <span>👤 ${d.trabajador}</span>
                    <span>${d.inicio} - ${d.fin}</span>
                </div>
            `).join('');
            infoDiv.innerHTML = html;
        } else {
            infoDiv.innerHTML = "<p>No hay trabajadores disponibles ese día.</p>";
        }
    });
});

updateCalendar();
