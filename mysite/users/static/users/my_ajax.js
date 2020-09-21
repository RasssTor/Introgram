function like(post_id) {
element = document.getElementById('lk' + post_id);
count = document.getElementById('count'+post_id);
                if (element.className == "like like-button")
                    {
                    console.log($("input[name=csrfmiddlewaretoken]").val());
                     element.className = "unlike like-button";
                     count.innerText = count.innerText - 1;
                     $.ajax({
                        url: 'post/like/',
                        method: 'get',
                        data: {
                            id: post_id,
                            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
                              },
                        success: function () {}

                            });
                    }
                 else {
                    count.innerText = parseInt(count.innerText) + 1;
                    element.className = "like like-button";
                            $.ajax({
            url: 'post/like/',
            method: 'post',
            data: {
                id: post_id,
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function () {
            }
        });
                 }

    }

function comment(post_id) {
if ($('#text' + post_id).val() != ''){
console.log(post_id);
        $.ajax({
            type: 'POST',
            url: 'add/comment/',
            data: {
                text: $('#text' + post_id).val(),
                id: post_id,
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function () {
                let div = document.createElement('div');
                let comments = document.getElementById('comments' + post_id);
                console.log(document.getElementById('main-photo-url').innerText)
                div.className = "comment";
                let divInter = document.createElement('div');
                divInter.className = "comment-author"
                divInter.innerHTML = "<img src=" + document.getElementById('main-photo-url').innerText + " class='very-small-avatar'>"

                add_url = document.createElement('a');
                add_url.setAttribute("href", document.getElementById('user-name').innerText);
                add_url.className = "comment-username"
                add_url.text = " " + document.getElementById('user-name').innerText
                divInter.append(add_url)
                let divInter2 = document.createElement('div');
                divInter2.innerHTML = $('#text' + post_id).val();
                divInter2.className = "comment-text"
                div.append(divInter);
                div.append(divInter2);
                document.getElementById('text' + post_id).value = "";
                comments.append(div)
                console.log(comments);
        }
});
}
}
//$(window).on("scroll", function() {
//    var x = 1
//    if ($(window).scrollTop() > $(document).height() - $(window).height() - 300){
//    x = x + 1;

//    $.ajax({
//            type: 'GET',
//            url: '?page=' + x.toString(),
////            data: {
////                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
////            },
//            success: function (data) {
//
//            var result = data.split('<div class="posts">');
//            result[1] = result[1].toString() - '</html>'
//            console.log(result[1]);
//        }
//});}
//    });

