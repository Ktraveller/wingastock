/* =========================================================
   PRODUCT DATA FROM DJANGO
========================================================= */

const productData =
    document.getElementById("productData");


function getProductData() {

    if (!productData) {
        return null;
    }

    return {

        reactUrl:
            productData.dataset.reactUrl,

        title:
            productData.dataset.title || "",

        description:
            productData.dataset.description || "",

        price:
            productData.dataset.price || "",

        seller:
            productData.dataset.seller || "",

        phone:
            productData.dataset.phone || "",

        location:
            productData.dataset.location || "",

        uploaded:
            productData.dataset.uploaded || "",

        image:
            productData.dataset.image || ""

    };

}






/* =========================================================
   SEND PRODUCT TO WHATSAPP
========================================================= */

function sendWhatsApp() {

    const productData = document.getElementById("productData");

    if (!productData) {
        console.error("Product data not found.");
        return;
    }

    const phone = productData.dataset.phone || "";
    const title = productData.dataset.title || "";
    const description = productData.dataset.description || "";
    const price = productData.dataset.price || "";
    const seller = productData.dataset.seller || "";
    const location = productData.dataset.location || "";
    const uploaded = productData.dataset.uploaded || "";
    const productUrl = productData.dataset.url || window.location.href;


    /* ---------------------------------------------------------
       CHECK PHONE NUMBER
    --------------------------------------------------------- */

    if (!phone.trim()) {
        alert("Seller phone number is not available.");
        return;
    }


    /* ---------------------------------------------------------
       CLEAN TANZANIA PHONE NUMBER
    --------------------------------------------------------- */

    let cleanPhone = phone.replace(/\D/g, "");

    // 0622652290 -> 255622652290
    if (cleanPhone.startsWith("0")) {
        cleanPhone = "255" + cleanPhone.substring(1);
    }

    // +255622652290 -> 255622652290
    if (cleanPhone.startsWith("255")) {
        // Already correct
    }


    /* ---------------------------------------------------------
       CREATE WHATSAPP MESSAGE
    --------------------------------------------------------- */

    const message =
        `Hello ${seller},

        I am interested in this product on WingaStock.

        Product: ${title}

        Price: ${price} TSh

        Description:
        ${description}

        View product:
        ${productUrl}`;


    /* ---------------------------------------------------------
       OPEN WHATSAPP
    --------------------------------------------------------- */

    const whatsappUrl =
        "https://wa.me/" +
        cleanPhone +
        "?text=" +
        encodeURIComponent(message);

    window.open(whatsappUrl, "_blank");
}








/* =========================================================
   GET CSRF COOKIE
========================================================= */

function getCookie(name) {

    let cookieValue = null;


    if (
        document.cookie &&
        document.cookie !== ""
    ) {

        const cookies =
            document.cookie.split(";");


        for (
            let i = 0;
            i < cookies.length;
            i++
        ) {

            const cookie =
                cookies[i].trim();


            if (
                cookie.substring(
                    0,
                    name.length + 1
                ) ===
                (name + "=")
            ) {

                cookieValue =
                    decodeURIComponent(
                        cookie.substring(
                            name.length + 1
                        )
                    );

                break;

            }

        }

    }


    return cookieValue;

}



/* =========================================================
   REACTION / LIKE / DISLIKE
========================================================= */

function reactToProduct(reaction) {

    const data =
        getProductData();


    if (!data || !data.reactUrl) {

        console.error(
            "Product reaction URL is missing."
        );

        return;

    }


    fetch(
        data.reactUrl,
        {

            method: "POST",

            headers: {

                "Content-Type":
                    "application/x-www-form-urlencoded",

                "X-CSRFToken":
                    getCookie("csrftoken"),

                "X-Requested-With":
                    "XMLHttpRequest"

            },

            body:
                `reaction=${encodeURIComponent(
                    reaction
                )}`

        }
    )

        .then(function (response) {

            return response.json();

        })

        .then(function (result) {

            if (!result.success) {

                alert(
                    result.message ||
                    "Unable to react."
                );

                return;

            }


            const likeCount =
                document.getElementById(
                    "like-count"
                );


            const dislikeCount =
                document.getElementById(
                    "dislike-count"
                );


            const likeButton =
                document.getElementById(
                    "like-btn"
                );


            const dislikeButton =
                document.getElementById(
                    "dislike-btn"
                );


            if (likeCount) {

                likeCount.textContent =
                    result.likes;

            }


            if (dislikeCount) {

                dislikeCount.textContent =
                    result.dislikes;

            }


            if (likeButton) {

                likeButton.classList.remove(
                    "active"
                );

            }


            if (dislikeButton) {

                dislikeButton.classList.remove(
                    "active"
                );

            }


            if (
                result.reaction === "like" &&
                likeButton
            ) {

                likeButton.classList.add(
                    "active"
                );

            }


            if (
                result.reaction === "dislike" &&
                dislikeButton
            ) {

                dislikeButton.classList.add(
                    "active"
                );

            }

        })

        .catch(function (error) {

            console.error(
                "Reaction error:",
                error
            );

        });

}



/* =========================================================
   PRODUCT IMAGE
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const mainImage =
            document.getElementById(
                "mainProductImage"
            );


        const thumbnails =
            document.querySelectorAll(
                ".product-thumbnail"
            );


        if (!mainImage) return;


        thumbnails.forEach(
            function (thumbnail) {

                thumbnail.addEventListener(
                    "click",
                    function () {

                        const image =
                            this.dataset.image;


                        if (!image) return;


                        mainImage.src =
                            image;


                        thumbnails.forEach(
                            function (item) {

                                item.classList.remove(
                                    "active"
                                );

                            }
                        );


                        this.classList.add(
                            "active"
                        );

                    }
                );

            }
        );

    }
);



/* =========================================================
   SHARE PRODUCT
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const shareButton =
            document.getElementById(
                "shareButton"
            );


        if (!shareButton) return;


        shareButton.addEventListener(
            "click",
            async function () {

                const data =
                    getProductData();


                if (!data) {

                    console.error(
                        "Product data is missing."
                    );

                    return;

                }


                const productUrl =
                    window.location.href;


                const shareText =

                    `${data.title}\n\n` +

                    `Price: ${data.price}\n` +

                    `Description: ${data.description}\n\n` +

                    `Seller: ${data.seller}\n` +

                    `Phone: ${data.phone}\n` +

                    `Location: ${data.location}\n` +

                    `Uploaded: ${data.uploaded}\n\n` +

                    `View product:\n${productUrl}`;


                try {


                    /* =====================================
                       SHARE ACTUAL PRODUCT IMAGE
                    ====================================== */

                    if (data.image) {

                        const response =
                            await fetch(
                                data.image
                            );


                        const blob =
                            await response.blob();


                        const file =
                            new File(
                                [blob],
                                "wingastock-product.jpg",
                                {
                                    type:
                                        blob.type ||
                                        "image/jpeg"
                                }
                            );


                        if (
                            navigator.share &&
                            navigator.canShare &&
                            navigator.canShare({
                                files: [file]
                            })
                        ) {

                            await navigator.share({

                                title:
                                    data.title,

                                text:
                                    shareText,

                                files: [
                                    file
                                ]

                            });


                            return;

                        }

                    }



                    /* =====================================
                       NORMAL SHARE
                    ====================================== */

                    if (navigator.share) {

                        await navigator.share({

                            title:
                                data.title,

                            text:
                                shareText,

                            url:
                                productUrl

                        });


                        return;

                    }



                    /* =====================================
                       CLIPBOARD FALLBACK
                    ====================================== */

                    if (navigator.clipboard) {

                        await navigator.clipboard.writeText(
                            shareText
                        );


                        alert(
                            "Product information copied."
                        );

                    }

                }

                catch (error) {

                    console.error(
                        "Share failed:",
                        error
                    );

                }

            }
        );

    }
);



/* =========================================================
   FAVORITE BUTTON
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const favoriteButton =
            document.getElementById(
                "favoriteButton"
            );


        if (!favoriteButton) return;


        favoriteButton.addEventListener(
            "click",
            function () {

                const icon =
                    this.querySelector("i");


                if (!icon) return;


                if (
                    icon.classList.contains("far")
                ) {

                    icon.classList.remove(
                        "far"
                    );

                    icon.classList.add(
                        "fas"
                    );

                    this.classList.add(
                        "active"
                    );

                } else {

                    icon.classList.remove(
                        "fas"
                    );

                    icon.classList.add(
                        "far"
                    );

                    this.classList.remove(
                        "active"
                    );

                }

            }
        );

    }
);