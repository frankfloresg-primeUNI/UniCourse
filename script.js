fetch("/api/posts")
    .then(response => response.json())
    .then(posts => {
        console.log(posts);
    })