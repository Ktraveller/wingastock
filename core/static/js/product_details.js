
// ================= IMAGE SWITCHER =================

function changeImage(img){

    document.getElementById("mainImage").src =
        img.src;
}

// ================= REQUEST CONTACT =================

document.querySelector(".primary").addEventListener("click", () => {

    alert("Contact request sent to seller!");

    // Future API:
    // POST /api/contact-request
});

// ================= WHATSAPP =================

document.querySelector(".whatsapp").addEventListener("click", () => {

    window.open(
        "https://wa.me/255700000000",
        "_blank"
    );
});