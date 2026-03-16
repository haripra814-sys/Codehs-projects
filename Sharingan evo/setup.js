class ItachiEyes {
  constructor() {
    this.leftEye = document.querySelector(".left-eye")
    this.rightEye = document.querySelector(".right-eye")
    this.statusText = document.querySelector(".status-text")
    this.statusProgress = document.querySelector(".status-progress")
    this.toggleBtn = document.getElementById("toggleBtn")
    this.pauseBtn = document.getElementById("pauseBtn")

    this.isMangekyo = false
    this.isAutoMode = true
    this.intervalId = null
    this.progressInterval = null
    this.transitionDuration = 3000 // 3 seconds

    this.init()
  }

  addRealisticMovements() {
    // Add subtle eye tracking to mouse movement
    document.addEventListener("mousemove", (e) => {
      const eyes = [this.leftEye, this.rightEye]
      const mouseX = e.clientX / window.innerWidth
      const mouseY = e.clientY / window.innerHeight

      eyes.forEach((eye, index) => {
        const pupil = eye.querySelector(".pupil")
        const offsetX = (mouseX - 0.5) * 3 // Subtle movement
        const offsetY = (mouseY - 0.5) * 2

        pupil.style.transform = `translate(${offsetX}px, ${offsetY}px)`
      })
    })

    // Add realistic blinking at random intervals
    setInterval(() => {
      if (Math.random() < 0.3) {
        // 30% chance every interval
        this.triggerBlink()
      }
    }, 3000)
  }

  triggerBlink() {
    const eyes = [this.leftEye, this.rightEye]
    eyes.forEach((eye) => {
      const eyeOuter = eye.querySelector(".eye-outer")
      eyeOuter.style.animation = "none"
      eyeOuter.style.transform = "scaleY(0.1)"

      setTimeout(() => {
        eyeOuter.style.transform = "scaleY(1)"
        eyeOuter.style.animation = ""
      }, 150)
    })
  }

  init() {
    this.startAutoTransition()
    this.setupEventListeners()
    this.updateStatus()
    this.addRealisticMovements() // Add this line
  }

  setupEventListeners() {
    this.toggleBtn.addEventListener("click", () => {
      this.toggleEyes()
    })

    this.pauseBtn.addEventListener("click", () => {
      this.toggleAutoMode()
    })

    // Add keyboard controls
    document.addEventListener("keydown", (e) => {
      if (e.code === "Space") {
        e.preventDefault()
        this.toggleEyes()
      } else if (e.code === "KeyP") {
        this.toggleAutoMode()
      }
    })

    // Add click on eyes to toggle
    this.leftEye.addEventListener("click", () => this.toggleEyes())
    this.rightEye.addEventListener("click", () => this.toggleEyes())
  }

  toggleEyes() {
    this.isMangekyo = !this.isMangekyo

    if (this.isMangekyo) {
      this.activateMangekyo()
    } else {
      this.activateSharingan()
    }

    this.updateStatus()
    this.addTransitionEffect()
  }

  activateSharingan() {
    this.leftEye.classList.remove("mangekyo")
    this.rightEye.classList.remove("mangekyo")
    this.statusText.textContent = "Sharingan"
    this.statusText.style.color = "#ff4444"
  }

  activateMangekyo() {
    this.leftEye.classList.add("mangekyo")
    this.rightEye.classList.add("mangekyo")
    this.statusText.textContent = "Mangekyo Sharingan"
    this.statusText.style.color = "#8B0000"
  }

  addTransitionEffect() {
    // Enhanced flash effect with more realistic colors
    const flash = document.createElement("div")
    flash.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: radial-gradient(circle at center, 
        rgba(255, 68, 68, 0.4) 0%, 
        rgba(139, 0, 0, 0.2) 30%,
        rgba(0, 0, 0, 0.1) 60%,
        transparent 100%);
      pointer-events: none;
      z-index: 1000;
      animation: realisticFlash 0.8s ease-out;
    `

    document.body.appendChild(flash)

    // Add enhanced flash animation
    const style = document.createElement("style")
    style.textContent = `
      @keyframes realisticFlash {
        0% { opacity: 0; transform: scale(0.8); }
        30% { opacity: 1; transform: scale(1.1); }
        60% { opacity: 0.7; transform: scale(1.05); }
        100% { opacity: 0; transform: scale(1); }
      }
    `
    document.head.appendChild(style)

    // Add pupil dilation effect during transition
    const pupils = document.querySelectorAll(".pupil")
    pupils.forEach((pupil) => {
      pupil.style.transform = "scale(1.3)"
      setTimeout(() => {
        pupil.style.transform = "scale(1)"
      }, 400)
    })

    setTimeout(() => {
      if (document.body.contains(flash)) {
        document.body.removeChild(flash)
      }
      if (document.head.contains(style)) {
        document.head.removeChild(style)
      }
    }, 800)
  }

  startAutoTransition() {
    if (this.intervalId) {
      clearInterval(this.intervalId)
    }

    this.intervalId = setInterval(() => {
      if (this.isAutoMode) {
        this.toggleEyes()
      }
    }, this.transitionDuration)

    this.startProgressBar()
  }

  startProgressBar() {
    if (this.progressInterval) {
      clearInterval(this.progressInterval)
    }

    let progress = 0
    const increment = 100 / (this.transitionDuration / 50) // Update every 50ms

    this.progressInterval = setInterval(() => {
      if (this.isAutoMode) {
        progress += increment
        if (progress >= 100) {
          progress = 0
        }
        this.statusProgress.style.width = progress + "%"
      }
    }, 50)
  }

  toggleAutoMode() {
    this.isAutoMode = !this.isAutoMode

    if (this.isAutoMode) {
      this.pauseBtn.textContent = "Pause Auto"
      this.pauseBtn.classList.remove("paused")
      this.startAutoTransition()
    } else {
      this.pauseBtn.textContent = "Resume Auto"
      this.pauseBtn.classList.add("paused")
      this.statusProgress.style.width = "0%"
    }
  }

  updateStatus() {
    // Add a subtle animation to the status text
    this.statusText.style.transform = "scale(1.1)"
    setTimeout(() => {
      this.statusText.style.transform = "scale(1)"
    }, 200)
  }
}

// Initialize the application when the DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  new ItachiEyes()

  // Add some additional visual effects
  createBackgroundEffects()
})

function createBackgroundEffects() {
  // Add more dynamic particles
  const container = document.querySelector(".background-effects")

  setInterval(() => {
    if (container.children.length < 10) {
      const particle = document.createElement("div")
      particle.className = "particle"
      particle.style.left = Math.random() * 100 + "%"
      particle.style.top = Math.random() * 100 + "%"
      particle.style.animationDelay = Math.random() * 2 + "s"
      particle.style.animationDuration = Math.random() * 4 + 4 + "s"

      container.appendChild(particle)

      // Remove particle after animation
      setTimeout(() => {
        if (container.contains(particle)) {
          container.removeChild(particle)
        }
      }, 8000)
    }
  }, 2000)
}

// Add some easter eggs
let konamiCode = []
const konamiSequence = [
  "ArrowUp",
  "ArrowUp",
  "ArrowDown",
  "ArrowDown",
  "ArrowLeft",
  "ArrowRight",
  "ArrowLeft",
  "ArrowRight",
  "KeyB",
  "KeyA",
]

document.addEventListener("keydown", (e) => {
  konamiCode.push(e.code)

  if (konamiCode.length > konamiSequence.length) {
    konamiCode.shift()
  }

  if (konamiCode.join(",") === konamiSequence.join(",")) {
    // Easter egg: Rapid transition mode
    const eyes = document.querySelectorAll(".eye")
    eyes.forEach((eye) => {
      eye.style.animation = "eyePulse 0.5s ease-in-out infinite"
    })

    setTimeout(() => {
      eyes.forEach((eye) => {
        eye.style.animation = "eyePulse 3s ease-in-out infinite"
      })
    }, 5000)

    konamiCode = []
  }
})
