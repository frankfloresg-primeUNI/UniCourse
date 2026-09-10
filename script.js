const courses = [
    {
        id: 1,
        name: "Programación I",
        professor: "Juan Pérez",
        rating: 4.5,
        description: "Curso donde aprendes fundamentos de programación.",
        advice: "Practica programación todas las semanas."
    },
    {
        id: 2,
        name: "Cálculo II",
        professor: "María López",
        rating: 4.2,
        description: "Curso enfocado en integrales y aplicaciones.",
        advice: "Haz ejercicios constantemente y no acumules temas."
    },
    {
        id: 3,
        name: "Circuitos Eléctricos",
        professor: "Carlos Torres",
        rating: 3.8,
        description: "Análisis de circuitos eléctricos y sus componentes.",
        advice: "Practica problemas y entiende los conceptos antes de memorizar."
    }
];


// ==============================
// PÁGINA PRINCIPAL
// ==============================

const container = document.getElementById("courses-container");

if (container) {

    function mostrarCursos(lista) {

        container.innerHTML = "";

        lista.forEach(course => {

            const card = document.createElement("div");

            card.classList.add("course");

            card.innerHTML = `
                <h3>${course.name}</h3>
                <p>Profesor: ${course.professor}</p>
                <p>⭐ ${course.rating}</p>

                <a href="detalle.html?id=${course.id}">
                    <button>Ver curso</button>
                </a>
            `;

            container.appendChild(card);
        });
    }

    mostrarCursos(courses);


    // BUSCADOR

    const search = document.getElementById("search");

    search.addEventListener("input", () => {

        const text = search.value.toLowerCase();

        const filteredCourses = courses.filter(course =>
            course.name.toLowerCase().includes(text)
        );

        mostrarCursos(filteredCourses);
    });
}


// ==============================
// PÁGINA DE DETALLE
// ==============================

const detailContainer = document.getElementById("course-detail");

if (detailContainer) {

    const params = new URLSearchParams(window.location.search);

    const id = Number(params.get("id"));

    const course = courses.find(course => course.id === id);

    if (course) {

        detailContainer.innerHTML = `
            <h2>${course.name}</h2>

            <p>
                <strong>Profesor:</strong>
                ${course.professor}
            </p>

            <p>
                <strong>Rating:</strong>
                ⭐ ${course.rating}
            </p>

            <hr>

            <h3>Descripción</h3>
            <p>${course.description}</p>

            <h3>💡 Consejo</h3>
            <p>${course.advice}</p>
        `;

    } else {

        detailContainer.innerHTML = `
            <h2>Curso no encontrado</h2>
        `;
    }
}