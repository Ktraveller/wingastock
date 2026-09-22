document.addEventListener("DOMContentLoaded", function () {

    const searchInput =
        document.getElementById("supportSearchInput");

    const clearSearchButton =
        document.getElementById("clearSupportSearch");

    const faqList =
        document.getElementById("faqList");

    const faqItems =
        document.querySelectorAll(".faq-item");

    const noResults =
        document.getElementById("faqNoResults");

    const contactButton =
        document.getElementById("contactSupportButton");

    const reportButton =
        document.getElementById("reportProblemButton");

    const feedbackButton =
        document.getElementById("feedbackButton");

    const helpButton =
        document.getElementById("supportHelpButton");


    /* =====================================================
       FAQ ACCORDION
    ====================================================== */

    faqItems.forEach(function (item) {

        const question =
            item.querySelector(".faq-question");


        question.addEventListener(
            "click",
            function () {

                const isOpen =
                    item.classList.contains("open");


                /*
                 * Close other FAQ items.
                 */

                faqItems.forEach(function (otherItem) {

                    otherItem.classList.remove("open");

                });


                /*
                 * Open selected item if it was closed.
                 */

                if (!isOpen) {

                    item.classList.add("open");

                }

            }
        );

    });


    /* =====================================================
       SEARCH FAQ
    ====================================================== */

    function searchFAQs() {

        const query =
            searchInput.value
                .trim()
                .toLowerCase();


        let visibleCount = 0;


        faqItems.forEach(function (item) {

            const question =
                item.dataset.question
                    .toLowerCase();


            const answer =
                item.querySelector(".faq-answer")
                    .textContent
                    .toLowerCase();


            if (
                !query ||
                question.includes(query) ||
                answer.includes(query)
            ) {

                item.style.display = "";

                visibleCount++;

            } else {

                item.style.display = "none";

                item.classList.remove("open");

            }

        });


        clearSearchButton.style.display =
            query ? "flex" : "none";


        if (visibleCount === 0) {

            faqList.style.display = "none";

            noResults.style.display = "flex";

        } else {

            faqList.style.display = "";

            noResults.style.display = "none";

        }

    }


    if (searchInput) {

        searchInput.addEventListener(
            "input",
            searchFAQs
        );

    }


    /* =====================================================
       CLEAR SEARCH
    ====================================================== */

    if (clearSearchButton) {

        clearSearchButton.addEventListener(
            "click",
            function () {

                searchInput.value = "";

                searchFAQs();

                searchInput.focus();

            }
        );

    }


    /* =====================================================
       CONTACT SUPPORT
    ====================================================== */

    if (contactButton) {

        contactButton.addEventListener(
            "click",
            function () {

                const message = prompt(
                    "Contact Support\n\n" +
                    "Please enter your message:"
                );

                if (message && message.trim() !== "") {

                    const whatsappNumber = "255622652290";

                    const whatsappMessage =
                        "Hello WingaStock Support,\n\n" +
                        message.trim();

                    window.open(
                        "https://wa.me/" +
                        whatsappNumber +
                        "?text=" +
                        encodeURIComponent(whatsappMessage),
                        "_blank"
                    );
                }

            }
        );

    }


    /* =====================================================
       REPORT PROBLEM
    ====================================================== */

    if (reportButton) {

        reportButton.addEventListener(
            "click",
            function () {

                const problem = prompt(
                    "Report a Problem\n\n" +
                    "Please describe the problem you are experiencing:"
                );

                if (problem && problem.trim() !== "") {

                    const whatsappNumber = "255622652290";

                    const whatsappMessage =
                        "Hello WingaStock Support,\n\n" +
                        "I would like to report a problem:\n\n" +
                        problem.trim();

                    window.open(
                        "https://wa.me/" +
                        whatsappNumber +
                        "?text=" +
                        encodeURIComponent(whatsappMessage),
                        "_blank"
                    );
                }

            }
        );

    }


    /* =====================================================
       FEEDBACK
    ====================================================== */

    if (feedbackButton) {

        feedbackButton.addEventListener(
            "click",
            function () {

                const feedback = prompt(
                    "Send Feedback\n\n" +
                    "Please enter your feedback:"
                );

                if (feedback && feedback.trim() !== "") {

                    const whatsappNumber = "255622652290";

                    const whatsappMessage =
                        "Hello WingaStock Support,\n\n" +
                        "I would like to send feedback:\n\n" +
                        feedback.trim();

                    window.open(
                        "https://wa.me/" +
                        whatsappNumber +
                        "?text=" +
                        encodeURIComponent(whatsappMessage),
                        "_blank"
                    );
                }

            }
        );

    }


    /* =====================================================
       HELP BUTTON
    ====================================================== */

    if (helpButton) {

        helpButton.addEventListener(
            "click",
            function () {

                const firstFAQ =
                    document.querySelector(".faq-item");


                if (firstFAQ) {

                    firstFAQ.scrollIntoView({
                        behavior: "smooth",
                        block: "center"
                    });


                    setTimeout(function () {

                        firstFAQ.classList.add("open");

                    }, 300);

                }

            }
        );

    }

});