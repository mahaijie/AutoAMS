$(document).ready(function () {

            $('.ConfirmDel').click(function () {
                delurl = $(this).attr("link");
                swal({
                    title: "确认删除吗？",
                    text: "删除后将无法恢复，请谨慎操作！",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#DD6B55",
                    confirmButtonText: "Yes",
                    closeOnConfirm: false

                }, function () {
                    $.get(delurl,function(data,status){
                            try  {
                                var obj = eval('(' + data + ')');
                            }
                            catch(exception) {
                                window.location.href=delurl;
                            }

                            if(obj.status == true) {
                                swal({
                                    title:"操作提示!",
                                    text:"删除成功！.",
                                    type:"success"
                                });
                                window.location.reload();
                            } else if(obj.status == false) {
                                swal({
                                    title:"操作失败!",
                                    text:"删除失败！"+obj.info,
                                    type:"error"
                                    }, function () {
                                        window.location.reload();
                                    });
                            }
                    });
                });

            });

});