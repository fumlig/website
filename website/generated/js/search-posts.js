function searchPosts() {

    const input = document.getElementById("search-posts");
    const posts = document.getElementById("posts").getElementsByClassName("post");

    filter = input.value.toLowerCase();

    let filters = []
    let i = 0;
    let f = "";
    while(i < filter.length) {
        if(filter[i] == ",") {
            filters.push(f);
            f = "";
            // ignore spaces after ,
            while(i+1 < filter.length && filter[i+1] == " ") {
                i++;
            }
        } else {
            f += filter[i];
        }
        i++;
    }
    if(f.length > 0) {
        filters.push(f);
    }
    
    for(let p = 0; p < posts.length; p++) {
        const post = posts[p];
        const postTitle = post.getElementsByClassName("post-title")[0];
        const postLead = post.getElementsByClassName("post-lead")[0];
        const postTags = post.getElementsByClassName("post-tags")[0];

        const postTitleContent = postTitle.innerText.toLowerCase();
        const postLeadContent = postLead.innerText.toLowerCase();
        const postTagsContent = postTags.innerText.toLowerCase();

        let show = true;
        for(let f = 0; f < filters.length; f++) {
            const match = 
                postTitleContent.indexOf(filters[f]) > -1 || 
                postLeadContent.indexOf(filters[f]) > -1 ||
                postTagsContent.indexOf(filters[f]) > -1;
            if(!match) {
                show = false;
                break;
            }
        }


        if(show) {
            post.style.display = "block";
        } else {
            post.style.display = "none";
        }
    }
}

function searchPostsFor(filter) {
    const input = document.getElementById("search-posts");
    input.value = filter;
    searchPosts();
}