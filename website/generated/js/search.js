function search() {

    const input = document.getElementById("search-posts");
    const posts = document.getElementById("posts").getElementsByClassName("post");

    const filter = input.value.toLowerCase();

    for(let p = 0; p < posts.length; p++) {
        const post = posts[p];
        const postTitle = post.getElementsByClassName("post-title")[0];
        const postLead = post.getElementsByClassName("post-lead")[0];

        const postTitleContent = postTitle.innerText.toLowerCase();
        const postLeadContent = postLead.innerText.toLowerCase();

        if(postTitleContent.indexOf(filter) > -1 || postLeadContent.indexOf(filter) > -1) {
            post.style.display = "";
        } else {
            post.style.display = "none";
        }
    }
}