const accessToken = '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';
const username = 'harrrrison';

// Fetch GitHub profile data
fetch(`https://api.github.com/users/${username}`, {
    headers: {
        Authorization: `Bearer ${accessToken}`,
    },
})
    .then(response => response.json())
    .then(data => {
        // Display profile information
        const profileSection = document.getElementById('profile');
        profileSection.innerHTML = `
        <div class="githugProfileBlock">
        <h1 class="repoName"><a href="${data.html_url}">${data.name}</a></h1>
        <p>${data.bio}</p>
        <p>Followers: ${data.followers}</p>
        </div>
    `;
    })
    .catch(error => console.error('Error fetching profile:', error));

// Fetch GitHub repositories
fetch(`https://api.github.com/users/${username}/repos?sort=updated`, {
    headers: {
        Authorization: `Bearer ${accessToken}`,
    },
})
    .then(response => response.json())
    .then(repositories => {
        // Display repositories
        const repositoriesSection = document.getElementById('repositories');

        repositories.forEach(repo => {
            repositoriesSection.innerHTML += `
 
            <div class="flip-container">
            <div class="flipper">
            <div class = "front">
                <h3>${repo.name}</h3>
            </div>
            <div class="back">
                <p>${repo.description}</p>
                <p>Language: ${repo.language}</p>
            </div>
            </div>   
            </div>  

        `;
        });
    })
    .catch(error => console.error('Error fetching repositories:', error));
