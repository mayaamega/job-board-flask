document.addEventListener("DOMContentLoaded", () => {
  // Flash message auto-dismiss
  const flashMessages = document.querySelectorAll(".flash-message")
  flashMessages.forEach((message) => {
    setTimeout(() => {
      message.style.opacity = "0"
      setTimeout(() => {
        message.style.display = "none"
      }, 500)
    }, 5000)
  })
})

