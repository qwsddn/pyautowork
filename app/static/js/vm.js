
// 申请vm模态框
$("#Addvpn").on('click',function(){
    $('#addvpnModal').modal('show')  
})

// 申请vm提交数据
$("#addvpnbtn").click(function(){
    var check = $("#addvpnForm").Validform().check()
     if (check) {
        $.post("/vmadd/",$("#addvpnForm").serialize(),function(data) {
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

// 添加vm提交数据
$("#addvpnbtn1").click(function(){
    var check = $("#addvpnForm").Validform().check()
     if (check) {
        $.post("/vmadd1/",$("#addvpnForm").serialize(),function(data) {
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
        var url = "/vmaudit/?id="+id
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
    $.getJSON("/vmupdate",{'id':id},function(data){
            console.log(data);
            $("#upid").val(data["id"]);
            $("#hostname").val(data["hostname"]);
            $("#system").val(data["system"]);
            $("#term").val(data["term"]);
            $("#cpu").val(data["cpu"]);
            $("#mem").val(data["mem"]);
            $("#disk").val(data["disk"]);
            $("#used").val(data["used"]);
            $("#owner").val(data["owner"]);
            $("#project").val(data["project"]);
            $("#expire_date").val(data["expire_date"]);
            $('#updateModal').modal('show');
            if (data["status"] == 0) 
               {  
                  $('.vm_status').eq(0).prop("checked",true);
                }
            else if (data["status"] == 1)
               {
                 $('.vm_status').eq(1).prop("checked",true);
               }
            else {
                  $('.vm_status').eq(2).prop("checked",true);
                 };

        })
})

// 更新编辑数据
$("#updatebtn").click(function(){
    var check = $("#updateForm").Validform().check()
    if (check) {
      $.post("/vmupdate/",$("#updateForm").serialize(),function(data) {
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

/*vm详情*/
$('.detail').click(function(){
    var id=$(this).attr('list_id')
    var url = "/vmupdate/?id="+id
    $.getJSON(url,function(data){
	    result = data
        console.log(result)
		 $('#detail_hostname').html('<pre>'+result['hostname']+'</pre>')
		 $('#detail_system').html('<pre>'+result['system']+'</pre>')
         $('#detail_term').html('<pre>'+result['term']+'</pre>')		 
         $('#detail_cpu').html('<pre>'+result['cpu']+'</pre>')		 
         $('#detail_mem').html('<pre>'+result['mem']+'</pre>')		 
         $('#detail_disk').html('<pre>'+result['disk']+'</pre>')		 
         $('#detail_ip').html('<pre>'+result['ip']+'</pre>')		 
         $('#detail_mask').html('<pre>'+result['mask']+'</pre>')		 
         $('#detail_gateway').html('<pre>'+result['gateway']+'</pre>')		 
         $('#detail_project').html('<pre>'+result['project']+'</pre>')		 
         $('#detail_status').html('<pre>'+result['status']+'</pre>')
         $('#detail_owner').html('<pre>'+result['owner']+'</pre>')
         $('#detail_used').html('<pre>'+result['used']+'</pre>')
         $('#detail_create_date').html('<pre>'+result['create_date']+'</pre>')
         $('#detail_expire_date').html('<pre>'+result['expire_date']+'</pre>')
    })
    $('#infoModel').modal('show')
})



/*删除vm*/
$(".del").click(function(){
	if(confirm("是否确认删除？")){
		var id = $(this).attr('data-id')
        var url = "/vmdelete/?id="+id
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

