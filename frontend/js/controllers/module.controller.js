// ========================================
// module.js
// JSL Digital Learning Academy
// ========================================

document.addEventListener("DOMContentLoaded", () => {

    // ========================================
    // Progress Bar Animation
    // ========================================

    const progressFill = document.querySelector(".progress-fill");

    if (progressFill) {

        const targetWidth = 10; // Percentage

        let currentWidth = 0;

        const animation = setInterval(() => {

            if (currentWidth >= targetWidth) {

                clearInterval(animation);

            } else {

                currentWidth++;

                progressFill.style.width = currentWidth + "%";

            }

        }, 25);

    }

    // ========================================
    // Smooth Scrolling
    // ========================================

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {

        anchor.addEventListener("click", function (e) {

            e.preventDefault();

            const target = document.querySelector(this.getAttribute("href"));

            if (target) {

                target.scrollIntoView({

                    behavior: "smooth"

                });

            }

        });

    });

    // ========================================
    // Continue Learning Button
    // ========================================

    const continueButton = document.querySelector(".btn-primary");

    if (continueButton) {

        continueButton.addEventListener("click", () => {

            window.location.href = "plant-workflow.html";

        });

    }

    // ========================================
    // Hero Buttons
    // ========================================

    const watchButton = document.querySelector(".btn-outline");

    if (watchButton) {

        watchButton.addEventListener("click", () => {

            alert("Company introduction video will be available soon.");

        });

    }

    // ========================================
    // Timeline Animation
    // ========================================

    const timelineItems = document.querySelectorAll(".timeline-item");

    const timelineObserver = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add("show");

            }

        });

    }, {

        threshold: 0.2

    });

    timelineItems.forEach(item => {

        timelineObserver.observe(item);

    });

    // ========================================
    // Card Hover Animation
    // ========================================

    const cards = document.querySelectorAll(
        ".highlight-card, .objective-card, .value-card, .plant-card, .product-card"
    );

    cards.forEach(card => {

        card.addEventListener("mouseenter", () => {

            card.style.transform = "translateY(-8px)";

        });

        card.addEventListener("mouseleave", () => {

            card.style.transform = "translateY(0px)";

        });

    });

    // ========================================
    // Plant Cards Click
    // ========================================

    document.querySelectorAll(".plant-card").forEach(card => {

        card.addEventListener("click", () => {

            const plant = card.querySelector("h3").innerText;

            alert("Opening details for " + plant);

        });

    });

    // ========================================
    // Product Cards Click
    // ========================================

    document.querySelectorAll(".product-card").forEach(card => {

        card.addEventListener("click", () => {

            alert("Product: " + card.innerText);

        });

    });

    // ========================================
    // Active Navbar
    // ========================================

    document.querySelectorAll(".module-navbar nav ul li").forEach(item => {

        item.addEventListener("click", () => {

            document.querySelectorAll(".module-navbar nav ul li").forEach(li => {

                li.classList.remove("active");

            });

            item.classList.add("active");

        });

    });

    // ========================================
    // Scroll Reveal Animation
    // ========================================

    const revealElements = document.querySelectorAll(

        ".company-hero, .about-company, .learning-objectives, .company-timeline, .vision-mission, .plants, .products"

    );

    const revealObserver = new IntersectionObserver((entries) => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.classList.add("visible");

            }

        });

    }, {

        threshold: 0.15

    });

    revealElements.forEach(element => {

        revealObserver.observe(element);

    });

    // ========================================
    // Footer Year
    // ========================================

    const footer = document.querySelector(".module-footer p");

    if (footer) {

        footer.innerHTML = `© ${new Date().getFullYear()} JSL Digital Learning Academy`;

    }

});