// ===== TEMA LIGHT/DARK =====
const themeToggleBtn = document.getElementById('themeToggleBtn');
const themeIcon = document.getElementById('themeIcon');
const htmlElement = document.documentElement;

const savedTheme = localStorage.getItem('belas-theme') || 'light';
htmlElement.setAttribute('data-theme', savedTheme);
updateThemeIcon(savedTheme);

themeToggleBtn.addEventListener('click', () => {
  const currentTheme = htmlElement.getAttribute('data-theme');
  const newTheme = currentTheme === 'light' ? 'dark' : 'light';

  htmlElement.setAttribute('data-theme', newTheme);
  localStorage.setItem('belas-theme', newTheme);
  updateThemeIcon(newTheme);

  showToast(`Tema ${newTheme === 'dark' ? 'escuro' : 'claro'} ativado`);
});

function updateThemeIcon(theme) {
  themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
}

// ===== LIGHTBOX =====
const imageLightbox = document.getElementById('imageLightbox');
const lightboxImage = document.getElementById('lightboxImage');

function openImageLightbox(imageUrl) {
  lightboxImage.src = imageUrl;
  imageLightbox.classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeImageLightbox() {
  imageLightbox.classList.remove('active');
  document.body.style.overflow = '';
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeImageLightbox();
    // Fechar modais fullscreen
    document.querySelectorAll('.modal-fullscreen.active').forEach(modal => {
      modal.classList.remove('active');
    });
    document.body.style.overflow = '';
  }
});

// ===== MODAL FULLSCREEN PONTOS TURÍSTICOS =====
function openFullscreenModal(modalId) {
  const modal = document.getElementById(modalId);
  modal.classList.add('active');
  document.body.style.overflow = 'hidden';
  // Scroll para o topo do modal
  setTimeout(() => {
    const content = modal.querySelector('.modal-fullscreen-content');
    if (content) content.scrollTop = 0;
  }, 100);
}

function closeFullscreenModal(event, modalId) {
  if (event.target === event.currentTarget) {
    const modal = document.getElementById(modalId);
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }
}

function closeFullscreenModalDirect(modalId) {
  const modal = document.getElementById(modalId);
  modal.classList.remove('active');
  document.body.style.overflow = '';
}

// ===== ESTRELAS INTERATIVAS =====
const starContainer = document.getElementById('starInput');
const ratingInput = document.getElementById('fbRating');
const stars = starContainer.querySelectorAll('.star');

stars.forEach(star => {
  star.addEventListener('click', () => {
    const value = parseInt(star.getAttribute('data-value'));
    ratingInput.value = value;
    updateStarInput(value);
  });

  star.addEventListener('mouseenter', () => {
    const value = parseInt(star.getAttribute('data-value'));
    highlightStars(value);
  });

  star.addEventListener('mouseleave', () => {
    const currentValue = parseInt(ratingInput.value) || 0;
    highlightStars(currentValue);
  });

  star.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      const value = parseInt(star.getAttribute('data-value'));
      ratingInput.value = value;
      updateStarInput(value);
    }
  });
});

function updateStarInput(value) {
  stars.forEach(star => {
    const starValue = parseInt(star.getAttribute('data-value'));
    if (starValue <= value) {
      star.classList.add('active');
      star.setAttribute('aria-checked', 'true');
    } else {
      star.classList.remove('active');
      star.setAttribute('aria-checked', 'false');
    }
  });
}

function highlightStars(value) {
  stars.forEach(star => {
    const starValue = parseInt(star.getAttribute('data-value'));
    star.classList.toggle('active', starValue <= value);
  });
}

// ===== PREVIEW DE IMAGEM =====
function handleImagePreview(event) {
  const file = event.target.files[0];
  const preview = document.getElementById('fbPreview');
  const previewImg = document.getElementById('fbPreviewImg');

  if (file) {
    const reader = new FileReader();
    reader.onload = function (e) {
      previewImg.src = e.target.result;
      preview.classList.add('active');
    };
    reader.readAsDataURL(file);
  }
}

function removeImagePreview() {
  const preview = document.getElementById('fbPreview');
  const fileInput = document.getElementById('fbImageFile');
  const previewImg = document.getElementById('fbPreviewImg');

  preview.classList.remove('active');
  fileInput.value = '';
  previewImg.src = '';
}

// ===== TOAST =====
function showToast(message) {
  const toast = document.getElementById('toastMsg');
  toast.textContent = message;
  toast.classList.add('show');

  setTimeout(() => {
    toast.classList.remove('show');
  }, 3000);
}

// ===== VALIDAÇÃO DO FORMULÁRIO =====
document.getElementById('feedbackForm').addEventListener('submit', function (e) {
  const rating = parseInt(ratingInput.value);
  if (rating < 1 || rating > 5 || isNaN(rating)) {
    e.preventDefault();
    showToast('Por favor, selecione uma avaliação de 1 a 5 estrelas.');
    starContainer.scrollIntoView({ behavior: 'smooth' });
  }

  else{
    showToast('Obrigado pelo seu Depoimento!.');
    setTimeout(() => {
      toast.classList.remove('show');
    }, 5000);
  }
});

// ===== CARROSSEL DE FEEDBACKS =====
function initFeedbackCarousel() {
  const track = document.getElementById('feedbacksCarouselTrack');
  const container = document.getElementById('feedbacksCarouselContainer');
  const prevBtn = document.getElementById('carouselPrevBtn');
  const nextBtn = document.getElementById('carouselNextBtn');
  const dotsContainer = document.getElementById('carouselDots');

  if (!track || !container || !prevBtn || !nextBtn) return;

  const items = track.querySelectorAll('.feedback-item');
  if (items.length === 0) return;

  let currentIndex = 0;
  let itemsPerView = calculateItemsPerView();
  let totalPages = Math.ceil(items.length / itemsPerView);

  function calculateItemsPerView() {
    const containerWidth = container.clientWidth;
    const itemWidth = 340; // min-width + gap aproximado
    return Math.max(1, Math.floor(containerWidth / itemWidth));
  }

  function createDots() {
    if (!dotsContainer) return;
    dotsContainer.innerHTML = '';
    totalPages = Math.ceil(items.length / itemsPerView);
    for (let i = 0; i < totalPages; i++) {
      const dot = document.createElement('button');
      dot.className = 'carousel-dot';
      dot.setAttribute('aria-label', `Página ${i + 1} de depoimentos`);
      dot.addEventListener('click', () => goToPage(i));
      dotsContainer.appendChild(dot);
    }
    updateDots();
  }

  function updateDots() {
    if (!dotsContainer) return;
    const dots = dotsContainer.querySelectorAll('.carousel-dot');
    dots.forEach((dot, index) => {
      dot.classList.toggle('active', index === currentIndex);
    });
  }

  function updateCarousel() {
    const itemWidth = items[0].offsetWidth;
    const gap = 24; // 1.5rem gap
    const offset = currentIndex * itemsPerView * (itemWidth + gap);
    track.style.transform = `translateX(-${offset}px)`;

    prevBtn.disabled = currentIndex === 0;
    nextBtn.disabled = currentIndex >= totalPages - 1;

    updateDots();
  }

  function goToPage(pageIndex) {
    currentIndex = Math.max(0, Math.min(pageIndex, totalPages - 1));
    updateCarousel();
  }

  prevBtn.addEventListener('click', () => {
    if (currentIndex > 0) {
      currentIndex--;
      updateCarousel();
    }
  });

  nextBtn.addEventListener('click', () => {
    if (currentIndex < totalPages - 1) {
      currentIndex++;
      updateCarousel();
    }
  });

  // Swipe para mobile
  let touchStartX = 0;
  let touchEndX = 0;

  track.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });

  track.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
  }, { passive: true });

  function handleSwipe() {
    const swipeThreshold = 50;
    if (touchStartX - touchEndX > swipeThreshold) {
      // Swipe left - next
      if (currentIndex < totalPages - 1) {
        currentIndex++;
        updateCarousel();
      }
    } else if (touchEndX - touchStartX > swipeThreshold) {
      // Swipe right - prev
      if (currentIndex > 0) {
        currentIndex--;
        updateCarousel();
      }
    }
  }

  // Atualizar ao redimensionar
  window.addEventListener('resize', () => {
    itemsPerView = calculateItemsPerView();
    totalPages = Math.ceil(items.length / itemsPerView);
    if (currentIndex >= totalPages) {
      currentIndex = Math.max(0, totalPages - 1);
    }
    createDots();
    updateCarousel();
  });

  createDots();
  updateCarousel();
}

// Inicializar carrossel quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', initFeedbackCarousel);
// Também inicializar após carregamento completo (para imagens)
window.addEventListener('load', initFeedbackCarousel);