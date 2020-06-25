
let savedNum = 0;
let escapedNum = 0;
let flagLeft = true;	// 左侧气球的单词是否为真词，每个试次更新
let flagRight = false;	// 右侧气球的单词是否为真词，每个试次更新
let flagContinue = true;	// 实验是否在继续
let noClick; // 没有点击时，自动飞走的触发器
let fly; // 用于自动飞走时的动画的出发器

$(document).ready(function(){
    noClick = setTimeout(flyAway, 5000);
});

function f() {
		console.log('break it');
		flagContinue = false;
	}

// 发送Ajax异步请求，取得返回结果后更新单词
function getNewWords(clicked,flag) {
    console.log("flagContinue:",flagContinue)
    if(!flagContinue){
        console.log("测试完成！");
        $("#word-left").text("游戏");
        $("#word-right").text("结束");
        return;
    }

    $.ajax({
        //请求方式
        type : "POST",
        //请求的媒体类型
        dataType: "json",
        //请求地址
        url : "/next/",
        //数据，json字符串
        data : {'clicked':clicked, 'flag':flag},
        //请求成功
        success : function(result) {
            if(result.realWord == ""){
                $("#word-left").text("游戏");
                $("#word-right").text("结束");
                flagContinue = false;
                return;
            }
            let randomNum = new Date().getSeconds();
            console.log("根据当前时间的秒数获得随机数：",randomNum);
            if (randomNum % 2 == 0){
                flagLeft = true;
                $("#word-left").text(result.realWord);
                flagRight = false;
                $("#word-right").text(result.fakeWord);
            }
            else{
                flagLeft = false;
                $("#word-left").text(result.fakeWord);
                flagRight = true;
                $("#word-right").text(result.realWord);
            }
        },
        //请求失败，包含具体的错误信息
        error : function(e){
            alert("连接失败，请检查网络或者联系管理员！")
            console.log(e.status);
            console.log(e.responseText);
        }
    })
}
function flyAway() {
    //alert("No Click! Balloons Will Fly Away!");
    console.log("No Click! Balloons Will Fly Away!")
    $("#wrap").addClass("animate__bounce");
    fly = setTimeout(function () {
        $("#wrap").removeClass("animate__bounce").hide().show();
        $("#choose").addClass("animate__fadeOutUp").one('animationend',function (){
            $("#choose").removeClass("animate__fadeOutUp").hide();
            getNewWords(false, false);
        reset();
        //$("#choose").addClass("animate__bounceOut").show();
        })
    },2000);
}

function onceClick(button, flag) {
    if(!flagContinue){
        return;
    }

    $("#wrap").removeClass("animate__bounce").hide().show();
    clearTimeout(noClick);
    clearTimeout(fly);

    // 隐藏未点击侧的气球
    if (button == 'left'){
        $('#balloon_right').hide();
    }
    else if(button == 'right'){
        $('#balloon_left').hide();
    }
    $("#choose").addClass("animate__slideOutUp");

    if (flag == true){ // 该词为真词
        savedNum += 1;
        $("#choose").one('animationend',function () {
            getNewWords(true, flag);
            $("#choose").removeClass("animate__slideOutUp").hide();
            $("#saved").addClass("animate__bounceInDown").show();
        })

        $("#saved").one("animationend",function () {
            $("#saved").removeClass("animate__bounceInDown").hide();
            $("#saved1").addClass("animate__fadeOutLeft").show();
        })

        $("#saved1").one("animationend",function () {
            $("#saved1").removeClass("animate__fadeOutLeft").hide();

            $("#sheep").hide();
            $("#sheep").addClass("animate__wobble").show();
        })
        $("#sheep").one("animationend",function (){
            $("#sheep").removeClass("animate__wobble");
            $("#savedNumber").text(savedNum);
            reset();
        })
    }
    else if(flag == false){
        escapedNum += 1;
        $("#choose").one('animationend',function () {
            getNewWords(true, flag);
            $("#choose").removeClass("animate__slideOutUp").hide();
            $("#escaped").addClass("animate__bounceInDown").show();
        })

        $("#escaped").one("animationend",function () {
            $("#escaped").removeClass("animate__bounceInDown").hide();
            $("#escaped1").addClass("animate__fadeOutRight").show();
        })

        $("#escaped1").one("animationend",function () {
            $("#escaped1").removeClass("animate__fadeOutRight").hide();

            $("#wolf").hide();
            $("#wolf").addClass("animate__wobble").show();
        })
        $("#wolf").one("animationend",function (){
            $("#wolf").removeClass("animate__wobble");
            $('#caughtNumber').text(escapedNum);
            reset();
        })
    }
    else {
        alert("发生了未知的错位，请联系管理员！")
    }
}
function reset() {
    $('#balloon_right').show();
    $('#balloon_left').show();
    $("#choose").show();

    if(!flagContinue){
        return;
    }
    noClick = setTimeout(flyAway, 5000);
}