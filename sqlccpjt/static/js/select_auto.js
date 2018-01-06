/* 제작 게코소프트 신현식 */
$(document).ready(function() {
	var theSelect=$("select");//모든 셀렉트를 선택
	var speed=200; //가짜 셀렉트 클릭시 옵션 나오는 속도 1000=1초
	theSelect.addClass("blind"); //셀렉트를 회면 밖으로 보내버림

	/* 보여지는 셀렉트 태그들 추가 시작 */
	theSelect.wrap("<div class='select_box'>")
	theSelect.after("<dl class='select_deco'>");
	$(".select_deco").append("<dt><a href='#'></a></dt>");
	$(".select_deco").append("<dd></dd>");
	$(".select_deco dd").append("<ul></ul>");
	/* 보여지는 셀렉트 태그들 추가 끝 */
	
	var theFakeSelect=$(".select_deco");//가짜 셀렉트를 선택
	var fakeDt=$(".select_deco dt");//가짜 셀렉트의 dt를 선택
	var fakeDd=$(".select_deco dd");//가짜 셀렉트의 dd를 선택

	for(i=0; i<=theFakeSelect.length-1; i++){

		theFakeSelect.eq(i).children("dt").children("a").append(theFakeSelect.eq(i).prev("select").find("option:selected").text().replace(',', '')); //셀렉트 옵션의 첫 텍스트를 맨처음 보이게 함

		var theOption=theFakeSelect.eq(i).parent("div").children("select").find("option");//셀렉트 옵션값을 가져옴
		var theOptionText=theOption.append(',').text(); //셀렉트 옵션을 배열로 변환하기 위해서 ,를 추가함
		var theLi=theOptionText.split(","); //셀렉트 옵션을 배열로 변환

		/* 셀렉트 옵션값을 가져와서 배열로 li안에 뿌림 시작*/
		for(k=0; k<=theOption.length-1; k++){	
			theFakeSelect.eq(i).children("dd").children().append("<li class='"+theOption.eq(k).attr("class")+"'><a href='#' value='"+theOption.eq(k).val()+"' name='"+theOption.eq(k).attr("name")+"'>"+theLi[k]+"</a></li>");
		}
		/* 셀렉트 옵션값을 가져와서 배열로 li안에 뿌림 끝*/
		theFakeSelect.eq(i).css("width",fakeDd.eq(i).closest(".select_box").children("select").width()+22); //가짜 셀렉트 dt의 높이를 dd안에 요소를 가져와서 맞춤

	}

	/* 보여지는 셀렉트 마우스오버이벤트 시작 */	
	fakeDt.mouseover(function(){
		var thisNum=fakeDt.index(this);
		var thisDt=fakeDt.eq(thisNum);
		
		thisDt.addClass("active");
	})

	fakeDt.mouseleave(function(){
		var thisNum=fakeDt.index(this);
		var thisDt=fakeDt.eq(thisNum);

		thisDt.removeClass();
	})
	/* 보여지는 셀렉트 마우스오버이벤트 끝 */	
	
	/* 보여지는 셀렉트 클릭이벤트 시작 */	
	fakeDt.click(function(){	
		var thisNum=fakeDt.index(this);
		var thisDt=fakeDt.eq(thisNum);
		var thisDd=fakeDt.eq(thisNum).next("dd");
		fakeDd.slideUp(speed);//다른 활성화된 가짜 셀렉트를 닫는다

		if(thisDd.is(":visible")){
			thisDd.slideUp(speed);
		}else{
			thisDd.slideDown(speed);
		}
		return false;
	})
	/* 보여지는 셀렉트 클릭이벤트 끝 */
	
	/* 보여지는 셀렉트 안쪽요소 오버이벤트 시작 */	
	var fakeUl=$(".select_deco>dd>ul");
	var fakeLi=$(".select_deco>dd>ul>li");

	fakeLi.mouseover(function(){
		var thisNum=fakeLi.index(this);
		var overLi=fakeLi.eq(thisNum);
		var thisDt=fakeLi.eq(thisNum).parent().parent().prev();

		overLi.addClass("active");
		thisDt.mouseover();
	})

	fakeLi.mouseleave(function(){
		var thisNum=fakeLi.index(this);
		var overLi=fakeLi.eq(thisNum);

		overLi.removeClass("active");
	})

	fakeUl.mouseleave(function(){
		var thisNum=fakeUl.index(this);
		var thisUl=fakeUl.eq(thisNum);
		var thisDt=thisUl.parent().prev();

		thisDt.mouseleave();
	})
	/* 보여지는 셀렉트 안쪽요소 오버이벤트 끝 */	

	/* 보여지는 셀렉트 안쪽요소 클릭이벤트 시작 */	
	fakeLi.click(function(){
		var thisNum=fakeLi.index(this);
		var thisNum2=$(this).parent().children().index(this);
		var overLi=fakeLi.eq(thisNum);
		var thisDt=overLi.parent().parent().prev().children();
		var thisDd=overLi.parent().parent();
		if(overLi.hasClass("title")){
		}else{
			thisDd.slideUp(speed);
			thisDt.text(overLi.text());
			thisDd.parent().prev("select").children().removeAttr("selected"); //가짜 셀렉트 재선택시 이전 선택된 옵션값을 지운다.
			thisDd.parent().prev("select").children().eq(thisNum2).click();
			thisDd.parent().prev("select").children().eq(thisNum2).attr("selected", "ture"); //가짜 셀렉트 선택시 진짜 셀렉터도 선택된다.
		}
		return false;
	})
	/* 보여지는 셀렉트 안쪽요소 클릭이벤트 끝 */

////////////////////////////////웹접근성 코드들/////////////////////////////////

	/* 진짜 셀렉트 포커스시 다음 가짜셀렉트로 강제 포커스 이동 시작*/
	theSelect.focus(function(){
		var thisNum=theSelect.index(this);
		var thisSelect=theSelect.eq(thisNum);
		var nextFake=thisSelect.parent().next(".select_deco").children("dt").children("a");

		thisSelect.parent().blur();
		nextFake.mouseover();
	})
	/* 진짜 셀렉트 포커스시 다음 가짜셀렉트로 강제 포커스 이동 끝 */

	/* 가짜 셀렉트 포커스이벤트 시작 */
	fakeDt.children().focus(function(){
		var thisNum=fakeDt.children().index(this);
		var thisDt=fakeDt.children().eq(thisNum);

		fakeDt.blur();
		thisDt.mouseover();
	})

	fakeDt.children().blur(function(){
		var thisNum=fakeDt.children().index(this);
		var thisDt=fakeDt.children().eq(thisNum);
		
		thisDt.mouseleave();
	})
	/* 가짜 셀렉트 포커스이벤트 끝 */
	
	/* 가짜 셀렉트 포커스상태에서 키보드 접근성 시작 */
	fakeDt.children().keydown(function(e){
		var thisNum=fakeDt.children().index(this);
		var thisDt=fakeDt.children().eq(thisNum);

		if (e.keyCode == "9") {
		thisDt.parent().click();
		}

		if (e.keyCode == "40") {
		thisDt.parent().click();
		thisDt.parent().next().children().children().eq(0).children().focus();
		return false;
		}
		
	})
	/* 가짜 셀렉트 포커스상태에서 키보드 접근성 끝 */


	/* 가짜 셀렉트 안쪽 리스트 포커스이벤트 시작 */
	fakeLi.children().focus(function(){
		var thisNum=fakeLi.children().index(this);
		var thisLi=fakeLi.children().eq(thisNum);

		thisLi.mouseover();
	})

	fakeLi.children().blur(function(){
		var thisNum=fakeLi.children().index(this);
		var thisLi=fakeLi.children().eq(thisNum);

		thisLi.mouseleave();
	})
	/* 가짜 셀렉트 안쪽 리스트 포커스이벤트 끝 */

	/* 가짜 셀렉트 안쪽 리스트 포커스시 키보드접근성 시작 */
	$(".select_deco li:last-child a").keydown(function(e){
		var thisNum=$(".select_deco li:last-child a").index(this);
		var thisLi=$(".select_deco li:last-child a").eq(thisNum);

		if (e.keyCode == "9") {
		thisLi.parent().parent().parent().slideUp(speed);
		}

		if (e.keyCode == "40") {
		thisLi.parent().parent().parent().slideUp(speed);
		return false;
		}
		
	})

	$(".select_deco li a").keydown(function(e){
		var thisNum=$(".select_deco li a").index(this);
		var thisLi=$(".select_deco li a").eq(thisNum);

		if (e.keyCode == "40") {
		thisLi.parent().next().children().focus();
		return false;
		}

		if (e.keyCode == "38") {
		thisLi.parent().prev().children().focus();
		return false;
		}

	})
	/* 가짜 셀렉트 안쪽 리스트 포커스시 키보드접근성 끝 */
})