// ===== CAROUSEL =====
let currentSlide = 0;
const totalSlides = 5;

function updateCarousel() {
    document.getElementById('carousel-track').style.transform = `translateX(-${currentSlide * 100}%)`;
    document.querySelectorAll('.carousel-dot').forEach((dot, i) => {
        dot.classList.toggle('active', i === currentSlide);
    });
}
function carouselNext() { currentSlide = (currentSlide + 1) % totalSlides; updateCarousel(); }
function carouselPrev() { currentSlide = (currentSlide - 1 + totalSlides) % totalSlides; updateCarousel(); }

// Init dots
(function () {
    const dotsContainer = document.getElementById('carousel-dots');
    for (let i = 0; i < totalSlides; i++) {
        const dot = document.createElement('button');
        dot.className = 'carousel-dot' + (i === 0 ? ' active' : '');
        dot.onclick = () => { currentSlide = i; updateCarousel(); };
        dotsContainer.appendChild(dot);
    }
})();

// Auto slide
setInterval(carouselNext, 5000);