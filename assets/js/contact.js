/*=============== EMAIL JS ===============*/
const contactForm = document.getElementById("contact-form"),
  contactMessage = document.getElementById("contact-message");

const sendEmail = (e) => {
  e.preventDefault();
  //serviceID - TemplateID - #form - publicKey
  emailjs
    .sendForm(
      "service_u20uoua",
      "template_w9msg9d",
      "#contact-form",
      "MlJ0JqwrxFxoY_e_j"
    )

    .then(
      () => {
        //Show sent message
        contactMessage.textContent = "Message sent successfully ✅";
        //remove message after five seconds
        setTimeout(() => {
          contactMessage.textContent = "";
        }, 5000);

        //Clear input fields
        contactForm.reset();
      },
      () => {
        //Show error message
        contactMessage.textContent = "Message not sent (service error) ❌";
      }
    );
};

contactForm.addEventListener("submit", sendEmail);
