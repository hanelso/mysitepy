//var i = 10;
//var o = {};
//var s = "hello";
//var jquery = function(){ alert(""); }
//var $ = jquery;
//jquery();
//$();
//sum(fuction(){
//alert("");
//});

//var 는 JavaScript에서 변수를 설정하는 방법
$(function(){
	$('#email').change(function(){
    	console.log('changed!!!');
	    $('#btn-emailcheck').show();
	    $('#img-emailcheck').hide();
	});

	var btn = $('#btn-emailcheck');
	btn.click(function(){

	    email = $('#email');
    	password = $('#password');
	    check = $('#img-emailcheck');

        // email이 입력되지 않은 경우
    	if(email == ''){
	    	return;
	    }

//	$.ajax(url="", type="", data=""); 이건 파이썬 방식
	    $.ajax({
		    url: '/user/checkemail?email=' + email.val(),
	    	type : 'get',
		    data : '',
		    dataType:'json',
//		    success는 콜백 함수로 ajax가 서버에 요청하고 응답을 받아온 후 실행할 함수를 말한다.
		    success : function(response){
			    if(response.result == false){
			    	alert('이미 존재하는 email입니다.');
			    	email.val('');
			    	email.focus();
			    	return;
			    	}

			    	alert('사용할 수 있는 email입니다.');
			    	btn.hide();
			    	check.show();
			    	password.focus();
			 }
		});	//이건 객체를 넣어준것임
	});
});