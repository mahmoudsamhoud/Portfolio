/* Contact form delivery through EmailJS. */
(() => {
  const form = document.getElementById("contact-form");
  const status = document.getElementById("contact-message");
  if (!form || !status) return;
  const button = form.querySelector('[type="submit"]');
  let sending = false;
  form.addEventListener("submit", async event => {
    event.preventDefault();
    if (sending || !form.reportValidity()) return;
    sending = true;
    button.disabled = true;
    form.setAttribute("aria-busy", "true");
    status.className = "text-center contact-status";
    status.textContent = "Sending message…";
    try {
      if (!window.emailjs) throw new Error("Email service unavailable");
      await window.emailjs.sendForm("service_u20uoua", "template_csmwvyd", form, "MlJ0JqwrxFxoY_e_j");
      status.classList.add("sent-message");
      status.textContent = "Message sent successfully.";
      form.reset();
    } catch (error) {
      status.classList.add("error-message");
      status.textContent = "Message could not be sent. Please try again or email me directly.";
    } finally {
      sending = false;
      button.disabled = false;
      form.removeAttribute("aria-busy");
    }
  });
})();
