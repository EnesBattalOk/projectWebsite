document.addEventListener('DOMContentLoaded', () => {
    // Slider Logic
    const slides = document.querySelectorAll('.slide');
    const prevBtn = document.querySelector('.slider-nav.prev');
    const nextBtn = document.querySelector('.slider-nav.next');
    const dotsContainer = document.querySelector('.slider-dots');

    let currentSlide = 0;
    const slideCount = slides.length;

    if (slideCount > 1) {
        // Create dots
        slides.forEach((_, i) => {
            const dot = document.createElement('div');
            dot.classList.add('dot');
            if (i === 0) dot.classList.add('active');
            dot.addEventListener('click', () => goToSlide(i));
            dotsContainer.appendChild(dot);
        });

        const dots = document.querySelectorAll('.dot');

        const updateDots = () => {
            dots.forEach((dot, i) => {
                dot.classList.toggle('active', i === currentSlide);
            });
        };

        const goToSlide = (n) => {
            slides[currentSlide].classList.remove('active');
            currentSlide = (n + slideCount) % slideCount;
            slides[currentSlide].classList.add('active');
            updateDots();
        };

        nextBtn.addEventListener('click', () => goToSlide(currentSlide + 1));
        prevBtn.addEventListener('click', () => goToSlide(currentSlide - 1));

        // Auto-play
        setInterval(() => {
            goToSlide(currentSlide + 1);
        }, 5000);
    }

    // Mobile Navigation Logic
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    const menuOverlay = document.querySelector('.mobile-menu-overlay');

    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            if (menuOverlay) menuOverlay.classList.toggle('active');

            // Toggle icon from bars to times
            const icon = mobileMenuBtn.querySelector('i');
            if (navLinks.classList.contains('active')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });

        if (menuOverlay) {
            menuOverlay.addEventListener('click', () => {
                navLinks.classList.remove('active');
                menuOverlay.classList.remove('active');
                const icon = mobileMenuBtn.querySelector('i');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            });
        }

        // Mobile Dropdown Logic
        const dropBtn = document.querySelector('.dropbtn');
        const dropdown = document.querySelector('.dropdown');
        if (dropBtn && dropdown) {
            dropBtn.addEventListener('click', (e) => {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    dropdown.classList.toggle('active');
                }
            });
        }
    }

    // Smooth scroll for anchors
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Fade in elements on scroll
    const scrollElements = document.querySelectorAll(".news-card");
    const elementInView = (el, dividend = 1) => {
        const elementTop = el.getBoundingClientRect().top;
        return (
            elementTop <= (window.innerHeight || document.documentElement.clientHeight) / dividend
        );
    };

    const displayScrollElement = (element) => {
        element.style.opacity = "1";
        element.style.transform = "translateY(0)";
    };

    const hideScrollElement = (element) => {
        element.style.opacity = "0";
        element.style.transform = "translateY(20px)";
    };

    const handleScrollAnimation = () => {
        scrollElements.forEach((el) => {
            if (elementInView(el, 1.25)) {
                displayScrollElement(el);
            }
        });
    }

    // Set initial state for cards
    scrollElements.forEach(el => {
        el.style.opacity = "0";
        el.style.transform = "translateY(20px)";
        el.style.transition = "all 0.6s ease-out";
    });

    window.addEventListener("scroll", () => {
        handleScrollAnimation();
    });

    // Trigger once on load
    handleScrollAnimation();

    // --- Water Saving Diary Logic ---
    const waterDiarySection = document.querySelector('.water-saving-diary-section');
    if (waterDiarySection) {
        const daysContainer = document.getElementById('daysList');
        const totalDisplay = document.getElementById('totalDisplay');
        const avgDisplay = document.getElementById('avgDisplay');
        const savingStatus = document.getElementById('savingStatus');
        const saveBtn = document.getElementById('saveEntryBtn');
        const refreshBtn = document.getElementById('refreshEntries');
        const entriesList = document.getElementById('entriesList');
        const familySizeSelect = document.getElementById('familySize');

        // Generate 30 days
        for (let i = 1; i <= 30; i++) {
            const row = document.createElement('div');
            row.className = 'day-entry-row';
            row.innerHTML = `
                <div class="day-label">Gün ${i}</div>
                <div class="day-input-wrapper">
                    <input type="number" step="0.01" min="0" value="0.0" class="day-input" data-day="${i}">
                </div>
                <div class="unit-label">m³</div>
            `;
            daysContainer.appendChild(row);
        }

        const calculateTotals = () => {
            let total = 0;
            const inputs = document.querySelectorAll('.day-input');
            inputs.forEach(input => {
                total += parseFloat(input.value) || 0;
            });

            const familySize = parseInt(familySizeSelect.value) || 1;
            const avg = total / familySize;

            totalDisplay.textContent = total.toFixed(2);
            avgDisplay.textContent = avg.toFixed(2) + ' m³';

            // Simple logic: if per person < 0.2 m3 per day (6m3 per month), it's excellent
            // 0.2m3 * 30 days = 6m3 per month per person is a good target.
            if (avg <= (6)) {
                savingStatus.textContent = 'Mükemmel Tasarruf! 🌱';
                savingStatus.style.color = '#fff';
            } else if (avg <= 10) {
                savingStatus.textContent = 'İyi Durumda 👍';
                savingStatus.style.color = '#e0f2fe';
            } else {
                savingStatus.textContent = 'Daha Fazla Tasarruf Yapılabilir 💧';
                savingStatus.style.color = '#fecaca';
            }
        };

        daysContainer.addEventListener('input', calculateTotals);
        familySizeSelect.addEventListener('change', calculateTotals);

        const loadEntries = async () => {
            try {
                const response = await fetch('/api/water-entries');
                const entries = await response.json();

                if (entries.length === 0) {
                    entriesList.innerHTML = '<div class="p-4 text-center text-muted">Henüz veri girişi yapılmamış.</div>';
                    return;
                }

                entriesList.innerHTML = entries.map(e => `
                    <div class="entry-item">
                        <div class="entry-main-info">
                            <h4>${e.studentName}</h4>
                            <p>${e.schoolName || 'Okul Belirtilmedi'}</p>
                        </div>
                        <div class="entry-meta">
                            <span class="entry-consumption">${e.totalConsumption.toFixed(2)} m³</span>
                            <span class="entry-date">${new Date(e.createdAt).toLocaleDateString()}</span>
                        </div>
                    </div>
                `).join('');
            } catch (err) {
                console.error(err);
                entriesList.innerHTML = '<div class="p-3 text-center text-danger">Veriler yüklenemedi.</div>';
            }
        };

        saveBtn.addEventListener('click', async () => {
            const studentName = document.getElementById('studentName').value;
            if (!studentName) {
                alert('Lütfen adınızı giriniz.');
                return;
            }

            saveBtn.disabled = true;
            saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Kaydediliyor...';

            const monthData = [];
            document.querySelectorAll('.day-input').forEach(input => {
                monthData.push({
                    day: input.dataset.day,
                    value: parseFloat(input.value) || 0
                });
            });

            const payload = {
                studentName: studentName,
                schoolName: document.getElementById('schoolName').value,
                teacherName: document.getElementById('teacherName').value,
                familySize: familySizeSelect.value,
                totalConsumption: parseFloat(totalDisplay.textContent),
                monthData: monthData
            };

            try {
                const response = await fetch('/api/save-water-entry', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                const result = await response.json();
                if (result.success) {
                    alert('Verileriniz başarıyla kaydedildi!');
                    loadEntries();
                    // Optional: Reset form or scroll to top
                } else {
                    alert('Hata: ' + result.message);
                }
            } catch (err) {
                alert('Kayda hata oluştu. Lütfen tekrar deneyin.');
            } finally {
                saveBtn.disabled = false;
                saveBtn.innerHTML = '<i class="fas fa-cloud-upload-alt"></i> Verileri Sunucuya Kaydet';
            }
        });

        refreshBtn.addEventListener('click', loadEntries);

        // Initial load
        loadEntries();
    }
});
