
/*
新建变量var 赋值方法和python一样,但一句话结束后必须写 ; 分号
数据类型: 布尔,Number,String,Undefined = 未定义的值,声明变量未赋值,null空对象,object对象
比较方法 && 是 and意思
||表示是or意思
! 描述not
== 不需要判断类型,直接判断值是否一样
=== 先判断数据类型是否一样,才有资格进行接下来的判断
 */
var dat = 10;
var old_data = 10;
var lst = ['我','爱','好','好','学','习'];
var value = 'hello ss';


//confirm使用的方法------
// document.getElementById('input_button').onclick = function () {
//     if (confirm('你确定要删除吗')){
//         alert('删除成功');
//
//     } else {
//         alert('取消删除');
//     }
//     console.log();
// };


// dat = toString(dat);
// dat = parseInt(dat); //从第一个字符开始转数字类型的   把字符串转换成数字
// dat = Number(dat); //转换成数字类型
//无论是否定义形参,参数都会包含在arguments里面

// typeof dat;  查看变量的类型

/*
switch (s = 'hello') {
    case s in value:
        console.log('hello 存在');
        break;
    case s in dat:
        console.log('不存在');
}

*/
/*  一.for循环
for(var value in lst){
    console.log(value)
}

for(var value=0;value < lst.length;value++){
    console.log('显示第',value,lst[value])
}
*/
/*
循环 for(语句1,语句2,语句三)
语句1开始要执行的,var一个对象之类的
语句2要执行的判断
语句三要完成的事情

for(;dat < 20;){
    console.log(dat)
    dat++
}

类似,是一样的方法,重点dat
for(var dat=0;dat < 20;dat++){
    consolo.log(dat)
}
 */


/* 二. if判断,swtich
if (dat === old_data) {
    console.log('正确');
}   else {
    console.log('不正确');
};



 */





