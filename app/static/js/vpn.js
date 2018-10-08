
// 申请vpn模态框
$("#Addvpn").on('click',function(){
    $('#addvpnModal').modal('show')  
})

// 申请vpn提交数据
$("#addvpnbtn").click(function(){
    var check = $("#addvpnForm").Validform().check()
     if (check) {
        $.post("/vpnadd/",$("#addvpnForm").serialize(),function(data) {
        data=JSON.parse(data)
        if(data["code"]==0){
			swal({
					title:"success",
					text:data["msg"],
					type:"success",
					confirmButtonText:'确定'
					},function(){
						location.reload()
					})
        }else{
            alert(data['msg'])
      }
        })
         return false;
   }     
})

// 添加vpn提交数据
$("#addvpnbtn1").click(function(){
    var check = $("#addvpnForm").Validform().check()
     if (check) {
        $.post("/vpnadd1/",$("#addvpnForm").serialize(),function(data) {
        data=JSON.parse(data)
        if(data["code"]==0){
			swal({
					title:"success",
					text:data["msg"],
					type:"success",
					confirmButtonText:'确定'
					},function(){
						location.reload()
					})
        }else{
            alert(data['msg'])
      }
        })
         return false;
   }     
})

$(function(){
   $(".addvpn").Validform({                 
           tiptype:3
     });
})

/*审核vpn*/
$(".audit").click(function(){
	if(confirm("是否确认审核？")){
		var id = $(this).attr('data-id')
        var url = "/vpnaudit/?id="+id
		$.getJSON(url,function(data){
			if (data['code']== 0 ){
				swal({
						title:"success",
						text:data["msg"],
						type:"success",
						confirmButtonText:'确定'
						},function(){
							location.reload()
						})
			}else{
                alert(data["msg"])
			}
    	})
    }  // end confirm
})   

// 点击编辑按钮，获取id，从逻辑端查出对应的数据，弹出模态窗渲染数据
$(".update").click(function(){   
    //$('#updateModal').modal('hide')
    var id=$(this).attr("data-id")
    $.getJSON("/vpnupdate",{'id':id},function(data){
            console.log(data);
            $("#upid").val(data["id"]);
            $("#name").val(data["name"]);
            $("#term").val(data["term"]);
            $("#used").val(data["used"]);
            $("#owner").val(data["owner"]);
            $("#create_date").val(data["create_date"]);
            $("#expire_date").val(data["expire_date"]);
            $('#updateModal').modal('show');
            if (data["status"] == 0) 
               {  
                  $('.vpn_status').eq(0).prop("checked",true);
                }
            else if (data["status"] == 1)
               {
                 $('.vpn_status').eq(1).prop("checked",true);
               }
            else {
                  $('.vpn_status').eq(2).prop("checked",true);
                 };

        })
})

// 更新编辑数据
$("#updatebtn").click(function(){
    var check = $("#updateForm").Validform().check()
    if (check) {
      $.post("/vpnupdate/",$("#updateForm").serialize(),function(data) {
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
        alert(data["msg"])
    }
    })
    return false;
  }
})

/*vpn详情*/
$('.detail').click(function(){
    var id=$(this).attr('list_id')
    var url = "/vpnupdate/?id="+id
    $.getJSON(url,function(data){
	    result = data
        console.log(result)
		 $('#detail_name').html('<pre>'+result['name']+'</pre>')
         $('#detail_term').html('<pre>'+result['term']+'</pre>')		 
         $('#detail_status').html('<pre>'+result['status']+'</pre>')
         $('#detail_owner').html('<pre>'+result['owner']+'</pre>')
         $('#detail_used').html('<pre>'+result['used']+'</pre>')
         $('#detail_create_date').html('<pre>'+result['create_date']+'</pre>')
         $('#detail_expire_date').html('<pre>'+result['expire_date']+'</pre>')
    })
    $('#infoModel').modal('show')
})



/*删除vpn*/
$(".del").click(function(){
	if(confirm("是否确认删除？")){
		var id = $(this).attr('data-id')
        var url = "/vpndelete/?id="+id
		$.getJSON(url,function(data){
			if (data['code']== 0 ){
                location.reload()
			}else{
                alert(data["msg"])
                location.reload()
			}
    	})
    }  // end confirm
})   

