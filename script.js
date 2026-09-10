const courses = [
    {
        name: "Programación I",
        professor: "Juan Pérez",
        rating: 4.5,
        description: "Curso donde aprendes fundamentos de programación."
    },
    {
        name: "Cálculo II",
        professor: "María López",
        rating: 4.2,
        description: "Curso enfocado en integrales y aplicaciones."
    },
    {
        name: "Circuitos Eléctricos",
        professor: "Carlos Torres",
        rating: 3.8,
        description: "Análisis de circuitos eléctricos y sus componentes."
    }
];

const container = document.getElementById("courses-container");

courses.forEach((course, index) => {

    const card = document.createElement("div");

    card.classList.add("course");

    card.innerHTML = `
        <h3>${course.name}</h3>
        <p>Profesor: ${course.professor}</p>
        <p>⭐ ${course.rating}</p>

        <button onclick="verCurso(${index})">
            Ver curso
        </button>

        <div id="details-${index}"></div>
    `;

    container.appendChild(card);
});


function verCurso(index) {

    const course = courses[index];

    const details = document.getElementById(`details-${index}`);

    details.innerHTML = `
        <hr>
        <p><strong>Descripción:</strong></p>
        <p>${course.description}</p>
    `;
}