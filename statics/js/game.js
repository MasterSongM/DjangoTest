
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