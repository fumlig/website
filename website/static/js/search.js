function search() {
    const input = document.getElementById("search-posts");
    const posts = document.getElementById("posts").getElementsByClassName("post");

    filter = input.value.toLowerCase();

    for(let p = 0; p < posts.length; p++) {
        const post = posts[p];
        const postTitle = post.getElementsByClassName("post-title")[0];
        const postLead = post.getElementsByClassName("post-lead")[0];
        const postTags = post.getElementsByClassName("post-tags")[0];

        const postTitleContent = postTitle.innerText.toLowerCase();
        const postLeadContent = postLead.innerText.toLowerCase();
        const postTagsContent = postTags.innerText.toLowerCase();

        const match = 
            postTitleContent.indexOf(filter) > -1 || 
            postLeadContent.indexOf(filter) > -1 ||
            postTagsContent.indexOf(filter) > -1;

        if(match) {
            post.style.display = "block";
        } else {
            post.style.display = "none";
        }
    }
}

function searchFor(filter) {
    const input = document.getElementById("search-posts");
    input.value = filter;
    search();
}