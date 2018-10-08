
// 添加用户模态框
$("#Addusers").on('click',function(){
    $('#adduserModal').modal('show')  
})

// 添加用户提交数据
$("#adduserbtn").click(function(){
    var check = $("#adduserForm").Validform().check()
     if (check) {
        $.post("/add/",$("#adduserForm").serialize(),function(data) {
        data=JSON.parse(data)
        if(data["code"]==0){
            location.reload()
        }else{
            
            alert(data["msg"])
      }
        })
         return false;
   }     
})


// 点击更新按钮，获取id，从逻辑端查出对应的数据，弹出模态窗渲染数据
$(".update").click(function(){   
    //$('#updateModal').modal('hide')
    var id=$(this).attr("data-id")
    $.getJSON("/update",{'id':id},function(data){
            console.log(data);
            $("#upid").val(data["id"]);
            $("#username").val(data["username"]);
            $("#name_cn").val(data["name_cn"]);
            $("#mobile").val(data["mobile"]);
            $("#email").val(data["email"]);
            $('#updateModal').modal('show');
            if (data["role"] == 0) 
               {  
                  $('.roles').eq(0).prop("checked",true);
                }
            else if (data["role"] == 1)
               {
                 $('.roles').eq(1).prop("checked",true);
               }
            else {
                  $('.roles').eq(2).prop("checked",true);
                 };

            if (data["status"] == 0)
                {
                    $('.user_status').eq(0).prop("checked",true);
                 }
            else
                {
                    $('.user_status').eq(1).prop("checked",true);
                }

        })
})

// 更新数据
$("#updatebtn").click(function(){
    var check = $("#updateForm").Validform().check()
    if (check) {
      $.post("/update/",$("#updateForm").serialize(),function(data) {
      data=JSON.parse(data)
      if(data["code"]==0){
        swal({
                title:"success",
                text:"更新成功",
                type:"success",
                confirmButtonText:'确定'
                },function(){
                    location.reload()
                })

    }else{
        alert("update error")
    }
    })
    return false;
  }
})

/*用户详情*/
$('.detail').click(function(){
    var id=$(this).attr('list_id')
    var url = "/update/?id="+id
    $.getJSON(url,function(data){
	    result = data
        console.log(result)
		 $('#detail_username').html('<pre>'+result['username']+'</pre>')
         $('#detail_name_cn').html('<pre>'+result['name_cn']+'</pre>')		 
         $('#detail_mobile').html('<pre>'+result['mobile']+'</pre>')
         $('#detail_email').html('<pre>'+result['email']+'</pre>')
    })
    $('#infoModel').modal('show')
})



/*删除用户*/
$(".del").click(function(){
	if(confirm("是否确认删除？")){
		var id = $(this).attr('data-id')
        var url = "/delete/?id="+id
		$.getJSON(url,function(data){
			if (data['code']== 0 ){
                location.reload()
			}else{
                alert(data["msg"])
			}
    	})
    }  // end confirm
})   


$(function(){
   $(".adduser").Validform({                 
           tiptype:3
     });
})


/*获取用户id，显示重置密码的模态窗*/
$(".reset").click(function(){
    var id=$(this).attr("data-id")
    $.getJSON("/resetpwdone",{'id':id},function(data){
        console.log(data);
        $("#resetid").val(data["id"]);
        $('#resetpasswd').modal('show')
    })
})

/*重置用户密码*/
$("#rspwbtn").click(function(){
   var check = $("#resetpw").Validform().check()
    if (check) {
     if ($("#newpasswd").val() != $("#confirm_pwd").val()){
        swal("新密码与确认密码不一致")
        return false
     }
     var str = $("#resetpw").serialize()
     var url = '/resetpwdone'
     $.post(url,str,function(data){
        data=JSON.parse(data)
        console.log(data)
        if (data['code']==0){   //recevie json object
             swal("更新成功")
             $('#resetpasswd').modal('hide')
        }else{
             swal(data['msg'])
              }
   })
     return false
  }
})

$(function(){
   $(".resetpass").Validform({
           tiptype:3
     });
})
