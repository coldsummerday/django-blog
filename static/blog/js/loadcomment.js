var index_base = 30;
function addcomment(id,name,email,date,content,parentid,parentName,parentEmail){
	var liElement =  document.createElement('li');
	liElement.id = 'comemnt:' + id.toString();
	liElement.className = 'item clearfix';
	liElement.setAttribute('style','margin-left: '+index_base+'px;');
	var mainElement = addCommentMain(email,name,date);
	liElement.appendChild(mainElement);
	mainElement.appendChild(addCommentBody(id,parentName,parentEmail,content,parentid));
	var ul = document.getElementsByClassName('commentList')[0]
	if(parentid==null)
	{
		liElement.setAttribute('style','margin-left: '+index_base+'px;');

		ul.appendChild(liElement);
	}
	else{
		var beforeElement =  document.getElementById('comemnt:'+parentid.toString());
		var index_before = Number(beforeElement.style.marginLeft.split('px')[0]);
		var index = index_before + index_base;
		liElement.setAttribute('style','margin-left: '+index.toString()+'px;');
		ul.insertBefore(liElement,beforeElement.nextSibling)
	}


}
function addCommentMain(email,name,time)
{
	var main = document.createElement('div');
	main.className = 'comment-main';
	var header = document.createElement('div');
	header.className = 'comment-header';
	main.appendChild(header);
	var meta  = document.createElement('div')
	meta.className = 'comment-meta';
	header.appendChild(meta);
	meta.innerHTML = '<a class="comment-author" href="mailto:' + email + '">' + name +'</a> 评论于 <time >' + time +'</time> '

	return main;
}
function addCommentBody(id,pidName,pidEmail,content,pid)
{
	var bodyElement = document.createElement('div');
	bodyElement.className = 'comment-body';
	var pElement = document.createElement('p');
	bodyElement.appendChild(pElement);
	if(pidName==null)
	{
	pElement.innerHTML ='<p>'+ content +'<button type="button" class="btn btn-info" style="float: right;" onclick="opencomment(\''+id.toString()+'\')">回复他/她</button></p> '
	}
	else
	{
		pElement.innerHTML = '<p><a href="mailto:'+pidEmail+'">@'+pidName+'</a>'+content+'<button type="button" class="btn btn-info"style="float: right;" onclick="opencomment(\''+id.toString()+'\')">回复他/她</button></p>'
	}
	return bodyElement;
}
function build_comment_tree(returndata)
{

	for(var key in returndata)
	{
		var value = returndata[key];
		addcomment(value.id,value.username,value.email,value.date_publish_str,value.content,value.pid_id,value.pid_username,value.pid_email)
	}
}
function ajaxGetComemntList (url) {

$.get(url, function (data, status) {

                if(status=='success')
                {
                    //先删除所有评论再刷新
                    var comment_list_obj = document.getElementsByClassName('commentList')[0]
                    while (comment_list_obj.firstChild)
                    {
                        comment_list_obj.removeChild(comment_list_obj.firstChild);
                    }
                    build_comment_tree(data);
                }


           });
}

