function init() {
    const stage = new createjs.Stage("demoCanvas");
    const circle = new createjs.Shape();
    circle.graphics.beginFill("DeepSkyBlue").drawCircle(0, 0, 50);
    circle.x = 100;
    circle.y = 100;
    const text = new createjs.Text("How are you", "20px Arial", "#000000");
    stage.addChild(circle);
    stage.addChild(text);
    stage.update();
    return
}

//animate("选择器","动画","次数","时延")
$.fn.extend({
    animateCss: function (animationName) {
        var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
        $(this).addClass('animated ' + animationName).one(animationEnd, function () {
            $(this).removeClass('animated ' + animationName);
        });
    }
}); //使用示例： $('#yourElement').animateCss('bounce');
