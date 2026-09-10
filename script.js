let courses = [];

const container = document.getElementById("courses-container");


async function cargarCursos() {

    const response = await fetch(
        "http://127.0.0.1:5000/api/courses"
    );

    courses = await response.json();

    mostrarCursos(courses);
}


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

            <button onclick="editarCurso(${course.id})">
                ✏️ Editar
            </button>

            <button onclick="eliminarCurso(${course.id})">
                🗑️ Eliminar
            </button>
        `;

        container.appendChild(card);
    });
}


if (container) {

    cargarCursos();

    const search = document.getElementById("search");

    search.addEventListener("input", () => {

        const text = search.value.toLowerCase();

        const filtered = courses.filter(course =>
            course.name.toLowerCase().includes(text)
        );

        mostrarCursos(filtered);
    });
}


const detailContainer =
    document.getElementById("course-detail");


async function cargarDetalle() {

    const params =
        new URLSearchParams(window.location.search);

    const id = params.get("id");

    const response = await fetch(
        `http://127.0.0.1:5000/api/courses/${id}`
    );

    if (!response.ok) {

        detailContainer.innerHTML =
            "<h2>Curso no encontrado</h2>";

        return;
    }

    const course = await response.json();

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
}


if (detailContainer) {
    cargarDetalle();
}

const form = document.getElementById("course-form");

if (form) {

    form.addEventListener("submit", async (event) => {

        event.preventDefault();

        const newCourse = {
            name: document.getElementById("name").value,
            professor: document.getElementById("professor").value,
            rating: Number(document.getElementById("rating").value),
            description: document.getElementById("description").value,
            advice: document.getElementById("advice").value
        };

        const response = await fetch(
            "http://127.0.0.1:5000/api/courses",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(newCourse)
            }
        );

        const result = await response.json();

        console.log(result);

        form.reset();

        cargarCursos();
    });
}

async function eliminarCurso(id) {

    const confirmar = confirm(
        "¿Seguro que quieres eliminar este curso?"
    );

    if (!confirmar) {
        return;
    }

    await fetch(
        `http://127.0.0.1:5000/api/courses/${id}`,
        {
            method: "DELETE"
        }
    );

    cargarCursos();
}

async function editarCurso(id) {

    const course = courses.find(
        course => course.id === id
    );

    const name = prompt(
        "Nombre del curso:",
        course.name
    );

    if (!name) return;

    const professor = prompt(
        "Profesor:",
        course.professor
    );

    const rating = prompt(
        "Rating:",
        course.rating
    );

    const description = prompt(
        "Descripción:",
        course.description
    );

    const advice = prompt(
        "Consejo:",
        course.advice
    );

    await fetch(
        `http://127.0.0.1:5000/api/courses/${id}`,
        {
            method: "PUT",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                name,
                professor,
                rating: Number(rating),
                description,
                advice
            })
        }
    );

    cargarCursos();
}