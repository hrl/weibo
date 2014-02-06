post_img_thumbnail_width = $('.post-img-thumbnail').width();
$('.post-img-thumbnail').height(post_img_thumbnail_width);

{% jinja %}
{% for i in range( post.get_image()|length ) %}
image_set_size("post-{{post.id}}-image-thumbnail-{{i}}", post_img_thumbnail_width);
thumbnail_set_onclick("post-{{post.id}}-image-carousel", "post-{{post.id}}-image-thumbnail-{{i}}", 'post-{{post.id}}-img-thumbnail', {{i}});
carousel_set_onclick("post-{{post.id}}-image-carousel", "post-{{post.id}}-image-carousel-{{i}}", 'post-{{post.id}}-img-thumbnail')
{% endfor %}
{% endjinja %}

$('#post-{{post.id}}-like')[0].onclick = function(){like('post-{{post.id}}-like', "post-{{post.id}}-unlike", "post", {{post.id}});}
$('#post-{{post.id}}-unlike')[0].onclick = function(){unlike('post-{{post.id}}-like', "post-{{post.id}}-unlike", "post", {{post.id}});}

$('#post-{{post.id}}-collect')[0].onclick = function(){collect('post-{{post.id}}-collect', 'post-{{post.id}}-uncollect', "post", {{post.id}});}
$('#post-{{post.id}}-uncollect')[0].onclick = function(){uncollect('post-{{post.id}}-collect', 'post-{{post.id}}-uncollect', "post", {{post.id}});}

{% if post.repo %}
post_repo_img_thumbnail_width = $('.post-repo-img-thumbnail').width();
$('.post-repo-img-thumbnail').height(post_repo_img_thumbnail_width);

{% jinja %}
{% for i in range( post.repo.get_image()|length ) %}
image_set_size("post-repo-{{post.repo.id}}-image-thumbnail-{{i}}", post_repo_img_thumbnail_width);
thumbnail_set_onclick("post-repo-{{post.repo.id}}-image-carousel", "post-repo-{{post.repo.id}}-image-thumbnail-{{i}}", 'post-repo-{{post.repo.id}}-img-thumbnail', {{i}});
carousel_set_onclick("post-repo-{{post.repo.id}}-image-carousel", "post-repo-{{post.repo.id}}-image-carousel-{{i}}", 'post-repo-{{post.repo.id}}-img-thumbnail')
{% endfor %}
{% endjinja %}


$('#post-repo-{{post.repo.id}}-like')[0].onclick = function(){like('post-repo-{{post.repo.id}}-like', "post-repo-{{post.repo.id}}-unlike", "post", {{post.repo.id}});}
$('#post-repo-{{post.repo.id}}-unlike')[0].onclick = function(){unlike('post-repo-{{post.repo.id}}-like', "post-repo-{{post.repo.id}}-unlike", "post", {{post.repo.id}});}

$('#post-repo-{{post.repo.id}}-collect')[0].onclick = function(){collect('post-repo-{{post.repo.id}}-collect', 'post-repo-{{post.repo.id}}-uncollect', "post", {{post.repo.id}});}
$('#post-repo-{{post.repo.id}}-uncollect')[0].onclick = function(){uncollect('post-repo-{{post.repo.id}}-collect', 'post-repo-{{post.repo.id}}-uncollect', "post", {{post.repo.id}});}

{% endif %}
