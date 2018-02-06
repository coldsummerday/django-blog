function updatePostList(data,apiurl){

	var mainElemet = document.getElementById('post-list-main')
	clearChildEl(mainElemet);
	    if(data.data.length==0)
    {
     mainElemet.innerHTML='<div class="no-post">暂时还没有发布的文章！</div>';
    }
	var urlinfo = parseQueryString(data.urlinfo)
	var articleArr = data.data;
	var  articleUrl = 'articles/'
	for(var id in articleArr)
	{
		var article = articleArr[id];
		addArticle(article,mainElemet,articleUrl+article.id)
	}
	addPagination(urlinfo,apiurl,data.before,data.next,mainElemet);

}

function addPagination(urlinfo,apiurl,before,next,mainEl)
{
	var pageEl= document.createElement('div')
	mainEl.appendChild(pageEl)
	var parentEl = document.createElement('ul')
	parentEl.className='pager'
	pageEl.appendChild(parentEl)
	var divEl = document.createElement('div')
	//重新拼接api接口,留下page
	var resturl = apiurl.concat('?')
			for(var id in urlinfo)
			{
				if(id!='page')
				{
					resturl = resturl + id +'=' + urlinfo[id] +'&'
				}
			}
	if(before)
	{
		var beforeEl = document.createElement('li')
		if(urlinfo.hasOwnProperty('page'))
		{
			pageNumer = (Number(urlinfo.page) - 1).toString()
			resturl = resturl.concat('page='+pageNumer)
			beforeEl.innerHTML='<button  type="button" class="btn btn-primary" onclick="ajaxGetFromApi(\''+resturl+'\')">上一页</button>'
			parentEl.appendChild(beforeEl);
		}
	}
	if(next)
	{
		var nextEl = document.createElement('li')
		if(urlinfo.hasOwnProperty('page'))
		{
				pageNumer = (Number(urlinfo.page) + 1).toString()
		}
		else{
			pageNumer = '1'
		}
		resturl = resturl.concat('page='+pageNumer)
		nextEl.innerHTML='<button  type="button" class="btn btn-primary" onclick="ajaxGetFromApi(\''+resturl+'\')">下一页</button>'
		parentEl.appendChild(nextEl);
	}
}
function addArticle(article,parentDom,articleUrl)
{
	var blogPost =document.createElement('div')
	blogPost.className = 'blog-post'
	var h2Element = document.createElement('h2')
	h2Element.setAttribute('align','center')
	h2Element.innerText = article.title;
	blogPost.appendChild(h2Element);
	var h4Element = document.createElement('h4')
	h4Element.setAttribute('align','center')
	h4Element.innerText = article.date_publish_str
	blogPost.appendChild(h4Element);
	var pElement = document.createElement('p')
	pElement.innerText = article.desc
	blogPost.appendChild(pElement);
	var aReadMoreElement = document.createElement('a')
	aReadMoreElement.setAttribute('href',articleUrl)
	aReadMoreElement.className="btn btn-default btn-lg "
	aReadMoreElement.innerHTML='Read More <i class="fa fa-angle-right"></i>'
	blogPost.appendChild(aReadMoreElement);
	var aCommentEl = document.createElement('a')
	aCommentEl.innerText = '评论数:' + article.comment_count
	blogPost.appendChild(aCommentEl);
	aClick = document.createElement('a')
	aClick.innerText = '浏览量' + article.click_count
	blogPost.appendChild(aClick);
	parentDom.appendChild(blogPost)
}

function parseQueryString(url) {
    var obj = {};
    var keyvalue = [];
    var key = "",
        value = "";
    var paraString = url.substring(url.indexOf("?") + 1, url.length).split("&");
    for (var i in paraString) {
        keyvalue = paraString[i].split("=");
        key = keyvalue[0];
        value = keyvalue[1];
        obj[key] = value;
    }
    return obj;
}
function clearChildEl(parentEl)
{
	 while (parentEl.firstChild)
        {
             parentEl.removeChild(parentEl.firstChild);
        }
}
function ajaxGetFromApi(url) {
     $.get(url, function (data, status) {

                if(status=='success')
                {
                    updatePostList(data,'/articleapi/')
                }


           });
}
