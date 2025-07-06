const track = document.querySelector('.slider-track');
const prevBtn = document.getElementById('prev');
const nextBtn = document.getElementById('next');
const slides = document.querySelectorAll('.slider-track img');

const slideWidth = 220; // 200px + 2x10px margen
const visibleSlides = 3;
const totalSlides = slides.length;

let currentIndex = 0;

function updateSlider() {
  const offset = currentIndex * slideWidth;
  track.style.transition = 'transform 0.4s ease-in-out';
  track.style.transform = `translateX(-${offset}px)`;
}

// Función para rotar al inicio cuando pasamos del final
function loopForward() {
  if (currentIndex < totalSlides - visibleSlides) {
    currentIndex++;
  } else {
    currentIndex = 0;
  }
  updateSlider();
}

// Función para rotar al final cuando retrocedemos desde el inicio
function loopBackward() {
  if (currentIndex > 0) {
    currentIndex--;
  } else {
    currentIndex = totalSlides - visibleSlides;
  }
  updateSlider();
}

nextBtn.addEventListener('click', loopForward);
prevBtn.addEventListener('click', loopBackward);
