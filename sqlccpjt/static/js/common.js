$(document).ready(function(){

/* show/hide(only one obj) start*/
$(document).on(
	"click", ".click_show_hide", function(){

	var thisNum=$(".click_show_hide").index(this);
	var thisShowClick=$(".click_show_hide").eq(thisNum);
	var target=thisShowClick.attr("class").replace("click_show_hide target_","show_hide_");
	var targetShowHide=$("."+target+"");

	if(targetShowHide.is(":visible")){
		targetShowHide.stop().fadeOut("500");
		$(".lay_pop_blind").stop().fadeOut("500");
	}else{
		targetShowHide.stop().fadeIn("500");
		$(".lay_pop_blind").stop().fadeIn("500");
	}
	return false;
});
/* show/hide(only one obj) end*/

/* 테이블 상단 전체체크 시작 */

var tbodyCheck=$("tbody :checkbox");

$(document).on(
	"change", "thead :checkbox", function(){    
	var thisTbodyCheck=$(this).parents("table").find("tbody :checkbox");

    if($(this).is(":checked")){                
		thisTbodyCheck.attr("checked", true);
    }else{
		thisTbodyCheck.attr("checked", false);
    }
 });
/* 테이블 상단 전체체크 끝 */

/*  푸터고정  시작 */
var winHeight=$(window).height();
var wrapHeight=$("#wrap").height();
var wrapHeight2=$(".index_wrap").height();
var theFooter=$("#footer");

function footerMove(){
	 winHeight=$(window).height();
	 wrapHeight=$("#wrap").height();

	if(wrapHeight2!=null && wrapHeight2<=winHeight){
		theFooter.addClass("on");
	}else{
		if(wrapHeight<=winHeight){
			theFooter.addClass("on");
		}else{
			theFooter.removeClass("on");
		}
	}
}
window.onload = footerMove;
window.onresize = footerMove;
/*  푸터고정  끝 */

/* 인덱스 아이콘 start*/
$(document).on(
	"mouseenter", ".index_icon li", function(){
	$(this).stop().animate({width:434},500);
	$(this).addClass("on");
});

$(document).on(
	"mouseleave", ".index_icon li", function(){
	$(this).stop().animate({width:200},500);
	$(this).removeClass("on");
});
/* 인덱스 아이콘 end*/

/* 탭 start*/
$(document).on(
	"click", ".tap_btn li", function(){
	$(this).addClass("on").siblings().removeClass("on");
	var thisNum=$(this).parents(".tap_btn").find(".on").index();
	$(this).parents(".tap_wrap").find(".tap_content").css("position","absolute").css("top","-1000em");
	$(this).parents(".tap_wrap").find(".tap_content").eq(thisNum).css("position","relative").css("top","0");
	footerMove();
	return false;
});
/* 탭 end*/

/* 드래그앤 드롭 시작 */
$(".sortable").sortable({
	revert: true,
	scope:"ok",
});

$(".drag_list .index_bar, .sortable .index_bar").draggable({ 
	snap:".sortable",
	scope:"ok",
	connectToSortable: ".sortable",
	helper:"clone",
	revert:"invalid"
});

$(".drag_list .index_bar, .sortable .index_bar").draggable({ 
	snap:".container",
	revert:false,
	stop: function( event, ui ) {
		$(this).remove();
	}
});
/* 드래그앤 드롭 끝 */
})