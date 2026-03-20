Debugging the Blueprint: A Bilingual DNA Integrity Monitor for Global Health.

## Inspiration
The inspiration for this project came from the realization that our DNA is essentially the "source code" of life. Just as a computer's binary can be corrupted by a "bit-flip," human DNA is constantly "hacked" by environmental stressors like cosmic radiation and terrestrial toxins. I wanted to bridge the gap between high-level molecular biology and accessible data science to help NGOs visualize genetic health risks in under-resourced communities.

## What it does
Open-Source Gene Guard is a bilingual (English/Spanish) web application that simulates the impact of environmental toxins on DNA integrity. Users can input specific toxin levels, and the Python-based backend calculates the probability of 8-oxoG (8-oxoguanine) lesions—the most common form of oxidative DNA damage. The app provides a "Community Health Score" and a real-time data visualization of genetic "data corruption."

## How we built it
The project was built using a "Full-Stack" approach:

Backend: Python and Flask handle the stochastic mutation logic, specifically targeting the low oxidation potential of Guanine.

Frontend: HTML5 and SCSS were used to create a clean, "UN-Blue" branded interface.

Data Vis: Chart.js powers the dynamic integrity graphs.

Bilingual Logic: A custom JSON-based translation system allows the entire UI to toggle between English and Spanish, ensuring global accessibility for NGOs.

## Challenges we ran into
The biggest challenge was translating complex chemical concepts—like "oxidation potential"—into a simplified algorithm that could run in a web browser. I also had to ensure the 8-oxoG mutation logic was scientifically grounded while remaining performant. Debugging the Flask routing for the bilingual toggle required a deep dive into how web sessions handle language states.

## Accomplishments that we're proud of
I am incredibly proud of creating a tool that is both scientifically accurate and accessible. Successfully implementing a "Language Toggle" was a major win, as it reflects my commitment to the UN Sustainable Development Goal 10 (Reduced Inequalities). Seeing a 7th-grade project move from a simple terminal script to a functional web dashboard was a huge milestone.

## What we learned
Through this project, I learned the fundamentals of Bioinformatics—how to treat biological sequences as data strings. I also improved my full-stack development skills, specifically in linking a Python backend to a responsive frontend. Most importantly, I learned that coding is a powerful tool for humanitarian advocacy.

## What's next for Open-Source Gene Guard
The next step is to integrate real-world environmental data via APIs (like air quality or radiation sensors) to provide live "Genetic Risk" maps for specific geographic regions. I also plan to expand the library of "Molecular Targets" to include more than just Guanine, creating a comprehensive "Firewall" for human health.

