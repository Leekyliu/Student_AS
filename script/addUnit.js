
(function ($) {
    var baseUrl = "http://ec2-3-104-75-184.ap-southeast-2.compute.amazonaws.com:16888";

    var input = $('.validate-input .account-info');

    $('.login100-form-btn').on('click',function(){
        var check = true;

        for(var i=0; i<input.length; i++) {
            if (validate(input[i]) == false ) {
                showValidate(input[i]);
                check = false;
            }
        }
        if(check) {

            var param = {};
            param.Faculty = $("input[name='Faculty']").val();
            param.AreaOfStudy = $("input[name='AreaOfStudy']").val();
            param.AreaOfStudyCode = $("input[name='AreaOfStudyCode']").val();
            param.Level = $("input[name='Level']").val();
            param.Offered = $("input[name='Offered']").val();
            param.UnitCode = $("input[name='UnitCode']").val();
            param.UnitName = $("input[name='UnitName']").val();
            param.MoreInfo = $("input[name='MoreInfo']").val();


            $.ajax({
                url: baseUrl + "/addUnitFunction",
                type: "post",
                data: param,
                datatype: "json",
                success: function (state) {
                    
                    if (state =="Success") {
                        alert("Added successfully")
                        window.location.href = "/staff"
                    } 
                    else{
                        alert("Fail to add unit code")
                    }

                }
            })
        }


    });



    $('.validate-form .input100').each(function(){
        $(this).focus(function(){
            hideValidate(this);
        });
    });

    function validate (input) {
       
            if($(input).val().trim() == ''){
                return false;
            }
        
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();

        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).removeClass('alert-validate');
    }


})(jQuery);